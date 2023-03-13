-- One-time script to setup alembic and "fake" the first migration to match the existing database state

CREATE TABLE IF NOT EXISTS public.alembic_version (
    version_num character varying(32) NOT NULL
);
ALTER TABLE public.alembic_version OWNER TO dev;
ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);

INSERT INTO alembic_version (version_num)
VALUES ('1f5853959c65');
