-- M0 exit test. Implements docs/06-implementation/00-implementation-plan.md M0.
--
-- The headline assertion: a connection authenticated for school A that asks for school B's
-- rows gets ZERO ROWS BACK, NOT AN ERROR. An error would mean the application is filtering;
-- zero rows means the database is. F6 is the failure that ends the company quietly, so it
-- is tested by the database rather than trusted to a code review.
--
-- Everything here runs as app_user, never as the owner or a superuser. Both bypass RLS,
-- and a green test run as either proves precisely nothing.

\set ON_ERROR_STOP on

create or replace function assert(cond boolean, msg text) returns void
language plpgsql as $$
begin
  if not cond then
    raise exception 'ASSERTION FAILED: %', msg;
  end if;
  raise notice '  ok  %', msg;
end
$$;

create or replace function assert_raises(stmt text, msg text) returns void
language plpgsql as $$
begin
  begin
    execute stmt;
  exception when others then
    raise notice '  ok  % [rejected: %]', msg, sqlerrm;
    return;
  end;
  raise exception 'ASSERTION FAILED: % -- statement was ALLOWED but must be rejected', msg;
end
$$;

-- ---------------------------------------------------------------------------------------
-- Fixtures, seeded as superuser (bypasses RLS). Two tenants.
-- ---------------------------------------------------------------------------------------

insert into schools (id, name, board) values
  ('11111111-1111-1111-1111-111111111111', 'School A', 'TS_STATE'),
  ('22222222-2222-2222-2222-222222222222', 'School B', 'CBSE');

insert into students (id, school_id, external_ref, grade, section) values
  ('aaaaaaaa-0000-0000-0000-000000000001',
   '11111111-1111-1111-1111-111111111111', 'A-001', 11, 'A'),
  ('aaaaaaaa-0000-0000-0000-000000000002',
   '11111111-1111-1111-1111-111111111111', 'A-002', 11, 'A'),
  ('bbbbbbbb-0000-0000-0000-000000000001',
   '22222222-2222-2222-2222-222222222222', 'B-001', 12, 'C');

insert into sessions (id, school_id, student_id) values
  ('a5e55101-0000-0000-0000-000000000001',
   '11111111-1111-1111-1111-111111111111', 'aaaaaaaa-0000-0000-0000-000000000001'),
  ('b5e55101-0000-0000-0000-000000000001',
   '22222222-2222-2222-2222-222222222222', 'bbbbbbbb-0000-0000-0000-000000000001');

insert into safeguarding_events (school_id, session_id, tier, category, excerpt) values
  ('11111111-1111-1111-1111-111111111111',
   'a5e55101-0000-0000-0000-000000000001', 2, 'self_harm', 'fixture A');

\echo ''
\echo '=== 1. Tenant isolation (F6) ==================================================='

set role app_user;

set app.school_id = '11111111-1111-1111-1111-111111111111';
select assert((select count(*) from students) = 2, 'school A sees its own 2 students');
select assert((select count(*) from schools)  = 1, 'school A sees exactly 1 school row');

-- The headline: ask directly for B's rows, as A.
select assert(
  (select count(*) from students
    where school_id = '22222222-2222-2222-2222-222222222222') = 0,
  'school A querying school B by id gets ZERO ROWS, not an error');

select assert(
  (select count(*) from students where external_ref = 'B-001') = 0,
  'school A cannot reach B''s student even via a non-tenant column');

set app.school_id = '22222222-2222-2222-2222-222222222222';
select assert((select count(*) from students) = 1, 'school B sees its own 1 student');
select assert((select count(*) from sessions) = 1, 'school B sees only its own session');
select assert((select count(*) from safeguarding_events) = 0,
              'school B cannot see school A''s safeguarding event');

\echo ''
\echo '=== 2. Fail closed when the tenant is unset ===================================='

reset app.school_id;
select assert((select count(*) from students) = 0,
              'no app.school_id set -> ZERO rows, not every row');
select assert((select count(*) from safeguarding_events) = 0,
              'no app.school_id set -> no safeguarding events');

set app.school_id = '';
select assert((select count(*) from students) = 0, 'empty app.school_id -> zero rows');

\echo ''
\echo '=== 3. Writes cannot cross the boundary ========================================'

set app.school_id = '11111111-1111-1111-1111-111111111111';
select assert_raises(
  $$insert into students (school_id, external_ref, grade, section)
    values ('22222222-2222-2222-2222-222222222222','X-999',11,'A')$$,
  'school A cannot INSERT a row belonging to school B');

select assert_raises(
  $$update students set section = 'HACKED' where external_ref = 'B-001'$$,
  'school A cannot UPDATE school B''s student');

\echo ''
\echo '=== 4. k-anonymity is a constraint, not a convention (FR-024) =================='

select assert_raises(
  $$insert into section_topic_friction
      (school_id, grade, section, topic_node, week_start, student_count, friction)
    values ('11111111-1111-1111-1111-111111111111',11,'A','quadratics','2027-06-07',4,0.5)$$,
  'aggregate covering 4 students is REJECTED BY THE DATABASE');

insert into section_topic_friction
  (school_id, grade, section, topic_node, week_start, student_count, friction)
  values ('11111111-1111-1111-1111-111111111111',11,'A','quadratics','2027-06-07',5,0.5);
select assert((select count(*) from section_topic_friction) = 1,
              'aggregate covering 5 students is accepted');

\echo ''
\echo '=== 5. Consent is structural (FR-015) =========================================='

insert into consents (school_id, student_id, granted_by, method, scope)
  values ('11111111-1111-1111-1111-111111111111',
          'aaaaaaaa-0000-0000-0000-000000000001','parent@example.test','otp','{tutoring}');

select assert_raises(
  $$insert into consents (school_id, student_id, granted_by, method, scope)
    values ('11111111-1111-1111-1111-111111111111',
            'aaaaaaaa-0000-0000-0000-000000000001','other@example.test','otp','{tutoring}')$$,
  'a second ACTIVE consent for the same student is rejected');

update consents set withdrawn_at = now()
  where student_id = 'aaaaaaaa-0000-0000-0000-000000000001';
insert into consents (school_id, student_id, granted_by, method, scope)
  values ('11111111-1111-1111-1111-111111111111',
          'aaaaaaaa-0000-0000-0000-000000000001','parent@example.test','otp','{tutoring}');
select assert((select count(*) from consents) = 2,
              'a new consent is allowed once the previous is withdrawn');

\echo ''
\echo '=== 6. Safeguarding log is append-only (ADR-011) ==============================='

select assert_raises(
  $$update safeguarding_events set excerpt = 'tampered'$$,
  'UPDATE on safeguarding_events is denied to the application role');

select assert_raises(
  $$delete from safeguarding_events$$,
  'DELETE on safeguarding_events is denied to the application role');

select assert_raises(
  $$insert into safeguarding_events
      (school_id, session_id, tier, category, parent_implicated, excerpt)
    values ('11111111-1111-1111-1111-111111111111',
            'a5e55101-0000-0000-0000-000000000001', 2, 'abuse', true, 'x')$$,
  'parent_implicated at tier 2 is rejected -- it must route as Tier 3');

reset role;

\echo ''
\echo '================================================================================'
\echo '  ALL ISOLATION TESTS PASSED'
\echo '  F6 closed: cross-tenant reads return zero rows, enforced by RLS in the DB.'
\echo '================================================================================'
