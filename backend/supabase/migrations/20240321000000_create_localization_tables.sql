-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. projects table
CREATE TABLE IF NOT EXISTS projects (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  slug        TEXT NOT NULL UNIQUE,
  description TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. languages table
CREATE TABLE IF NOT EXISTS languages (
  code       TEXT PRIMARY KEY,
  name       TEXT NOT NULL
);

-- 3. translation_keys table
CREATE TABLE IF NOT EXISTS translation_keys (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  key         TEXT NOT NULL,
  category    TEXT,
  description TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(project_id, key)
);

-- 4. translations table
CREATE TABLE IF NOT EXISTS translations (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  translation_key_id  UUID NOT NULL REFERENCES translation_keys(id) ON DELETE CASCADE,
  language_code       TEXT NOT NULL REFERENCES languages(code),
  value               TEXT NOT NULL,
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_by          TEXT,
  UNIQUE(translation_key_id, language_code)
);

-- Optional 5. translation_history table for auditing
CREATE TABLE IF NOT EXISTS translation_history (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  translation_id UUID NOT NULL REFERENCES translations(id),
  old_value      TEXT NOT NULL,
  new_value      TEXT NOT NULL,
  changed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  changed_by     TEXT
); 