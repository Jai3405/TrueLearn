-- True Learn AI -- slice 1 schema.
-- Implements docs/04-design/01-lld.md section 1.
--
-- Two properties here are enforced by the database rather than by application code,
-- because in the application one forgotten clause re-identifies a child:
--   * tenant isolation  -> row-level security, not WHERE school_id = ?
--   * k-anonymity       -> a CHECK constraint, not a query filter
--
-- Postgres 13+ (gen_random_uuid is built in).

begin;

-- ---------------------------------------------------------------------------------------
-- Roles. The application NEVER connects as the owner or as a superuser: both bypass RLS,
-- and an isolation test run as either proves nothing at all.
-- ---------------------------------------------------------------------------------------

do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'app_user') then
    create role app_user login password 'app_user_dev_only';
  end if;
end
$$;

-- ---------------------------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------------------------

create table schools (
  id            uuid primary key default gen_random_uuid(),
  name          text not null,
  board         text not null check (board in ('CBSE','AP_STATE','TS_STATE')),
  created_at    timestamptz not null default now()
);

create table students (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid not null references schools(id),
  external_ref  text not null,                       -- the school's own roll number
  grade         smallint not null check (grade between 10 and 12),
  section       text not null,
  status        text not null default 'pending_consent'
                check (status in ('pending_consent','active','withdrawn')),
  created_at    timestamptz not null default now(),
  unique (school_id, external_ref)
);

-- Consent is a row, not a flag. FR-015: no session without one.
create table consents (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid not null references schools(id),
  student_id    uuid not null references students(id),
  granted_by    text not null,                       -- parent/guardian identifier
  method        text not null,                       -- how it was verified
  scope         text[] not null,
  granted_at    timestamptz not null default now(),
  withdrawn_at  timestamptz                          -- null = active
);
create unique index consents_one_active
  on consents (student_id) where withdrawn_at is null;

create table sessions (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid not null references schools(id),
  student_id    uuid not null references students(id),
  topic_node    text,
  started_at    timestamptz not null default now(),
  ended_at      timestamptz,
  -- 'safeguarding' = ended while in SupportMode, NOT halted by us. ADR-011 v0.2.0
  end_reason    text check (end_reason in ('completed','abandoned','safeguarding','error'))
);

create table turns (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid not null references schools(id),
  session_id    uuid not null references sessions(id),
  seq           smallint not null,
  student_text  text,
  image_key     text,                                -- object store, 30-day TTL
  transcription jsonb,                               -- steps read, pre-confirmation
  confirmed     boolean,                             -- FR-026
  tutor_text    text,
  guard_action  text not null default 'clean'
                check (guard_action in ('clean','regenerated','blocked')),
  step_down_lvl smallint not null default 0,
  -- SPK-4: rules triage, model classifies. Recorded per turn so escalation rate (A-035)
  -- is measurable from day one -- it decides whether triage is a cost lever at all.
  escalated     boolean not null default false,
  created_at    timestamptz not null default now(),
  unique (session_id, seq)
);

-- The ONLY analytics table. No per-student profile exists anywhere. GD-07.
-- Anyone adding a student_profile table re-introduces the DPDP s.9(3) prohibited activity,
-- which has NO consent gateway. Do not add one.
create table section_topic_friction (
  school_id     uuid not null references schools(id),
  grade         smallint not null,
  section       text not null,
  topic_node    text not null,
  week_start    date not null,
  student_count smallint not null,                   -- k, for suppression
  friction      numeric(4,3) not null,
  primary key (school_id, grade, section, topic_node, week_start),
  constraint k_anonymity check (student_count >= 5)  -- FR-024, enforced by the DB
);

-- Append-only. Survives consent withdrawal. Retained >=180 days, in India (CERT-In).
-- In a POCSO s.21 prosecution this table is the evidence that a report was made, and when.
create table safeguarding_events (
  id                uuid primary key default gen_random_uuid(),
  school_id         uuid not null references schools(id),
  session_id        uuid not null references sessions(id),
  tier              smallint not null check (tier between 0 and 4),   -- ADR-011
  category          text not null check (category in
                      ('self_harm','abuse','threat_to_others','low_concern','other')),
  parent_implicated boolean not null default false,  -- forces Tier 3 routing
  detected_at       timestamptz not null default now(),
  reviewed_at       timestamptz,                     -- the 60-min SLA clock stops here
  reviewed_by       text,                            -- the NAMED human. POCSO s.19
  notified_at       timestamptz,
  notified_who      text,
  excerpt           text not null,
  -- ADR-011: a parent-implicated disclosure is Tier 3, always. Not a convention.
  constraint parent_implicated_is_tier3
    check (not parent_implicated or tier = 3)
);

-- ---------------------------------------------------------------------------------------
-- Row-level security.
--
-- FORCE is not optional. Without it the table OWNER bypasses every policy below, so an
-- isolation test run as the owner passes while production leaks. This is the single most
-- common way RLS is got wrong.
--
-- current_setting(..., true) returns NULL when unset, and `school_id = NULL` matches no
-- rows. So a connection that forgets to set the tenant sees NOTHING rather than
-- EVERYTHING. Fail closed.
-- ---------------------------------------------------------------------------------------

create or replace function app_current_school() returns uuid
language sql stable as $$
  select nullif(current_setting('app.school_id', true), '')::uuid
$$;

do $$
declare t text;
begin
  foreach t in array array[
    'students','consents','sessions','turns','section_topic_friction','safeguarding_events'
  ]
  loop
    execute format('alter table %I enable row level security', t);
    execute format('alter table %I force row level security', t);
    execute format($p$
      create policy tenant_isolation on %I
        using (school_id = app_current_school())
        with check (school_id = app_current_school())
    $p$, t);
    execute format('grant select, insert, update, delete on %I to app_user', t);
  end loop;
end
$$;

-- schools is the tenant root: visible only as yourself.
alter table schools enable row level security;
alter table schools force row level security;
create policy tenant_isolation on schools
  using (id = app_current_school())
  with check (id = app_current_school());
grant select, insert, update, delete on schools to app_user;

-- Append-only, ADR-011. Revoked from app_user specifically, not just from PUBLIC --
-- revoking from PUBLIC alone does nothing once the role holds explicit grants.
revoke update, delete on safeguarding_events from app_user;
revoke update, delete on safeguarding_events from public;

commit;
