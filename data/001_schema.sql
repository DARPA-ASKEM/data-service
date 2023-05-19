--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: extractedtype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.extractedtype AS ENUM (
    'equation',
    'figure',
    'table'
);


ALTER TYPE public.extractedtype OWNER TO dev;

--
-- Name: intermediateformat; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.intermediateformat AS ENUM (
    'bilayer',
    'gromet',
    'other',
    'sbml'
);


ALTER TYPE public.intermediateformat OWNER TO dev;

--
-- Name: intermediatesource; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.intermediatesource AS ENUM (
    'mrepresentationa',
    'skema'
);


ALTER TYPE public.intermediatesource OWNER TO dev;

--
-- Name: ontologicalfield; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.ontologicalfield AS ENUM (
    'obj',
    'unit'
);


ALTER TYPE public.ontologicalfield OWNER TO dev;

--
-- Name: provenancetype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.provenancetype AS ENUM (
    'Concept',
    'Dataset',
    'Intermediate',
    'Model',
    'ModelParameter',
    'ModelRevision',
    'Plan',
    'PlanParameter',
    'Project',
    'Publication',
    'SimulationRun'
);


ALTER TYPE public.provenancetype OWNER TO dev;

--
-- Name: relationtype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.relationtype AS ENUM (
    'BEGINS_AT',
    'CITES',
    'COMBINED_FROM',
    'CONTAINS',
    'COPIED_FROM',
    'DECOMPOSED_FROM',
    'DERIVED_FROM',
    'EDITED_FROM',
    'EQUIVALENT_OF',
    'EXTRACTED_FROM',
    'GENERATED_BY',
    'GLUED_FROM',
    'IS_CONCEPT_OF',
    'PARAMETER_OF',
    'REINTERPRETS',
    'STRATIFIED_FROM',
    'USES'
);


ALTER TYPE public.relationtype OWNER TO dev;

--
-- Name: resourcetype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.resourcetype AS ENUM (
    'datasets',
    'intermediates',
    'models',
    'plans',
    'publications',
    'simulation_runs'
);


ALTER TYPE public.resourcetype OWNER TO dev;

--
-- Name: role; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.role AS ENUM (
    'author',
    'contributor',
    'maintainer',
    'other'
);


ALTER TYPE public.role OWNER TO dev;

--
-- Name: taggabletype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.taggabletype AS ENUM (
    'datasets',
    'features',
    'intermediates',
    'model_parameters',
    'models',
    'projects',
    'publications',
    'qualifiers',
    'simulation_parameters',
    'simulation_plans',
    'simulation_runs'
);


ALTER TYPE public.taggabletype OWNER TO dev;

--
-- Name: valuetype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.valuetype AS ENUM (
    'binary',
    'bool',
    'float',
    'int',
    'str'
);


ALTER TYPE public.valuetype OWNER TO dev;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: active_concept; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.active_concept (
    curie character varying NOT NULL,
    name character varying
);


ALTER TABLE public.active_concept OWNER TO dev;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO dev;

--
-- Name: association; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.association (
    id integer NOT NULL,
    person_id integer NOT NULL,
    resource_id integer NOT NULL,
    resource_type public.resourcetype,
    role public.role
);


ALTER TABLE public.association OWNER TO dev;

--
-- Name: association_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.association_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.association_id_seq OWNER TO dev;

--
-- Name: association_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.association_id_seq OWNED BY public.association.id;


--
-- Name: dataset; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.dataset (
    id integer NOT NULL,
    name character varying NOT NULL,
    url character varying NOT NULL,
    description text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    deprecated boolean DEFAULT false,
    sensitivity text,
    quality text,
    temporal_resolution character varying,
    geospatial_resolution character varying,
    annotations json,
    data_path character varying,
    maintainer integer,
    simulation_run boolean DEFAULT false
);


ALTER TABLE public.dataset OWNER TO dev;

--
-- Name: dataset_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.dataset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dataset_id_seq OWNER TO dev;

--
-- Name: dataset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.dataset_id_seq OWNED BY public.dataset.id;


--
-- Name: extraction; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.extraction (
    id integer NOT NULL,
    publication_id integer NOT NULL,
    type public.extractedtype NOT NULL,
    data bytea NOT NULL,
    img bytea NOT NULL
);


ALTER TABLE public.extraction OWNER TO dev;

--
-- Name: extraction_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.extraction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraction_id_seq OWNER TO dev;

--
-- Name: extraction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.extraction_id_seq OWNED BY public.extraction.id;


--
-- Name: feature; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.feature (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    description text,
    display_name character varying,
    name character varying NOT NULL,
    value_type public.valuetype NOT NULL
);


ALTER TABLE public.feature OWNER TO dev;

--
-- Name: feature_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.feature_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feature_id_seq OWNER TO dev;

--
-- Name: feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.feature_id_seq OWNED BY public.feature.id;


--
-- Name: intermediate; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.intermediate (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    source public.intermediatesource NOT NULL,
    type public.intermediateformat NOT NULL,
    content bytea NOT NULL
);


ALTER TABLE public.intermediate OWNER TO dev;

--
-- Name: intermediate_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.intermediate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.intermediate_id_seq OWNER TO dev;

--
-- Name: intermediate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.intermediate_id_seq OWNED BY public.intermediate.id;


--
-- Name: model_description; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_description (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    framework character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    state_id integer NOT NULL
);


ALTER TABLE public.model_description OWNER TO dev;

--
-- Name: model_description_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.model_description_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_description_id_seq OWNER TO dev;

--
-- Name: model_description_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.model_description_id_seq OWNED BY public.model_description.id;


--
-- Name: model_framework; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_framework (
    name character varying NOT NULL,
    version character varying NOT NULL,
    semantics character varying NOT NULL,
    schema_url character varying NOT NULL
);


ALTER TABLE public.model_framework OWNER TO dev;

--
-- Name: model_parameter; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_parameter (
    id integer NOT NULL,
    model_id integer,
    name character varying NOT NULL,
    type public.valuetype NOT NULL,
    default_value character varying,
    state_variable boolean NOT NULL
);


ALTER TABLE public.model_parameter OWNER TO dev;

--
-- Name: model_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.model_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_parameter_id_seq OWNER TO dev;

--
-- Name: model_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.model_parameter_id_seq OWNED BY public.model_parameter.id;


--
-- Name: model_runtime; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_runtime (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    name character varying NOT NULL,
    "left" character varying NOT NULL,
    "right" character varying NOT NULL
);


ALTER TABLE public.model_runtime OWNER TO dev;

--
-- Name: model_runtime_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.model_runtime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_runtime_id_seq OWNER TO dev;

--
-- Name: model_runtime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.model_runtime_id_seq OWNED BY public.model_runtime.id;


--
-- Name: model_state; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_state (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    content json
);


ALTER TABLE public.model_state OWNER TO dev;

--
-- Name: model_state_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.model_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_state_id_seq OWNER TO dev;

--
-- Name: model_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.model_state_id_seq OWNED BY public.model_state.id;


--
-- Name: ontology_concept; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.ontology_concept (
    id integer NOT NULL,
    curie character varying NOT NULL,
    type public.taggabletype NOT NULL,
    object_id integer NOT NULL,
    status public.ontologicalfield NOT NULL
);


ALTER TABLE public.ontology_concept OWNER TO dev;

--
-- Name: ontology_concept_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.ontology_concept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ontology_concept_id_seq OWNER TO dev;

--
-- Name: ontology_concept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.ontology_concept_id_seq OWNED BY public.ontology_concept.id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.person (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    org character varying,
    website character varying,
    is_registered boolean NOT NULL
);


ALTER TABLE public.person OWNER TO dev;

--
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_id_seq OWNER TO dev;

--
-- Name: person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.person_id_seq OWNED BY public.person.id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.project (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now(),
    active boolean NOT NULL,
    username character varying
);


ALTER TABLE public.project OWNER TO dev;

--
-- Name: project_asset; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.project_asset (
    id integer NOT NULL,
    project_id integer NOT NULL,
    resource_id integer NOT NULL,
    resource_type public.resourcetype NOT NULL,
    external_ref character varying
);


ALTER TABLE public.project_asset OWNER TO dev;

--
-- Name: project_asset_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.project_asset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_asset_id_seq OWNER TO dev;

--
-- Name: project_asset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.project_asset_id_seq OWNED BY public.project_asset.id;


--
-- Name: project_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_id_seq OWNER TO dev;

--
-- Name: project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.project_id_seq OWNED BY public.project.id;


--
-- Name: provenance; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.provenance (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    relation_type public.relationtype NOT NULL,
    "left" integer NOT NULL,
    left_type public.provenancetype NOT NULL,
    "right" integer NOT NULL,
    right_type public.provenancetype NOT NULL,
    user_id integer,
    concept character varying
);


ALTER TABLE public.provenance OWNER TO dev;

--
-- Name: provenance_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.provenance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.provenance_id_seq OWNER TO dev;

--
-- Name: provenance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.provenance_id_seq OWNED BY public.provenance.id;


--
-- Name: publication; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.publication (
    id integer NOT NULL,
    xdd_uri character varying NOT NULL,
    title character varying NOT NULL
);


ALTER TABLE public.publication OWNER TO dev;

--
-- Name: publication_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.publication_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.publication_id_seq OWNER TO dev;

--
-- Name: publication_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.publication_id_seq OWNED BY public.publication.id;


--
-- Name: qualifier; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.qualifier (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    description text,
    name character varying NOT NULL,
    value_type public.valuetype NOT NULL
);


ALTER TABLE public.qualifier OWNER TO dev;

--
-- Name: qualifier_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.qualifier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qualifier_id_seq OWNER TO dev;

--
-- Name: qualifier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.qualifier_id_seq OWNED BY public.qualifier.id;


--
-- Name: qualifier_xref; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.qualifier_xref (
    id integer NOT NULL,
    qualifier_id integer NOT NULL,
    feature_id integer NOT NULL
);


ALTER TABLE public.qualifier_xref OWNER TO dev;

--
-- Name: qualifier_xref_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.qualifier_xref_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qualifier_xref_id_seq OWNER TO dev;

--
-- Name: qualifier_xref_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.qualifier_xref_id_seq OWNED BY public.qualifier_xref.id;


--
-- Name: simulation_parameter; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.simulation_parameter (
    id integer NOT NULL,
    run_id integer NOT NULL,
    name character varying NOT NULL,
    value character varying NOT NULL,
    type public.valuetype NOT NULL
);


ALTER TABLE public.simulation_parameter OWNER TO dev;

--
-- Name: simulation_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.simulation_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simulation_parameter_id_seq OWNER TO dev;

--
-- Name: simulation_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.simulation_parameter_id_seq OWNED BY public.simulation_parameter.id;


--
-- Name: simulation_plan; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.simulation_plan (
    id integer NOT NULL,
    model_id integer NOT NULL,
    simulator character varying NOT NULL,
    query character varying NOT NULL,
    content json NOT NULL
);


ALTER TABLE public.simulation_plan OWNER TO dev;

--
-- Name: simulation_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.simulation_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simulation_plan_id_seq OWNER TO dev;

--
-- Name: simulation_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.simulation_plan_id_seq OWNED BY public.simulation_plan.id;


--
-- Name: simulation_run; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.simulation_run (
    id integer NOT NULL,
    simulator_id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    completed_at timestamp without time zone,
    success boolean,
    dataset_id integer,
    description text,
    response bytea
);


ALTER TABLE public.simulation_run OWNER TO dev;

--
-- Name: simulation_run_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.simulation_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simulation_run_id_seq OWNER TO dev;

--
-- Name: simulation_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.simulation_run_id_seq OWNED BY public.simulation_run.id;


--
-- Name: software; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.software (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    source character varying NOT NULL,
    storage_uri character varying NOT NULL
);


ALTER TABLE public.software OWNER TO dev;

--
-- Name: software_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.software_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.software_id_seq OWNER TO dev;

--
-- Name: software_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.software_id_seq OWNED BY public.software.id;


--
-- Name: association id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.association ALTER COLUMN id SET DEFAULT nextval('public.association_id_seq'::regclass);


--
-- Name: dataset id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.dataset ALTER COLUMN id SET DEFAULT nextval('public.dataset_id_seq'::regclass);


--
-- Name: extraction id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.extraction ALTER COLUMN id SET DEFAULT nextval('public.extraction_id_seq'::regclass);


--
-- Name: feature id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.feature ALTER COLUMN id SET DEFAULT nextval('public.feature_id_seq'::regclass);


--
-- Name: intermediate id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.intermediate ALTER COLUMN id SET DEFAULT nextval('public.intermediate_id_seq'::regclass);


--
-- Name: model_description id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_description ALTER COLUMN id SET DEFAULT nextval('public.model_description_id_seq'::regclass);


--
-- Name: model_parameter id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_parameter ALTER COLUMN id SET DEFAULT nextval('public.model_parameter_id_seq'::regclass);


--
-- Name: model_runtime id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime ALTER COLUMN id SET DEFAULT nextval('public.model_runtime_id_seq'::regclass);


--
-- Name: model_state id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_state ALTER COLUMN id SET DEFAULT nextval('public.model_state_id_seq'::regclass);


--
-- Name: ontology_concept id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.ontology_concept ALTER COLUMN id SET DEFAULT nextval('public.ontology_concept_id_seq'::regclass);


--
-- Name: person id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.person ALTER COLUMN id SET DEFAULT nextval('public.person_id_seq'::regclass);


--
-- Name: project id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.project ALTER COLUMN id SET DEFAULT nextval('public.project_id_seq'::regclass);


--
-- Name: project_asset id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.project_asset ALTER COLUMN id SET DEFAULT nextval('public.project_asset_id_seq'::regclass);


--
-- Name: provenance id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.provenance ALTER COLUMN id SET DEFAULT nextval('public.provenance_id_seq'::regclass);


--
-- Name: publication id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.publication ALTER COLUMN id SET DEFAULT nextval('public.publication_id_seq'::regclass);


--
-- Name: qualifier id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier ALTER COLUMN id SET DEFAULT nextval('public.qualifier_id_seq'::regclass);


--
-- Name: qualifier_xref id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier_xref ALTER COLUMN id SET DEFAULT nextval('public.qualifier_xref_id_seq'::regclass);


--
-- Name: simulation_parameter id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_parameter ALTER COLUMN id SET DEFAULT nextval('public.simulation_parameter_id_seq'::regclass);


--
-- Name: simulation_plan id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_plan ALTER COLUMN id SET DEFAULT nextval('public.simulation_plan_id_seq'::regclass);


--
-- Name: simulation_run id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_run ALTER COLUMN id SET DEFAULT nextval('public.simulation_run_id_seq'::regclass);


--
-- Name: software id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.software ALTER COLUMN id SET DEFAULT nextval('public.software_id_seq'::regclass);


--
-- Name: active_concept active_concept_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.active_concept
    ADD CONSTRAINT active_concept_pkey PRIMARY KEY (curie);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: association association_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_pkey PRIMARY KEY (id);


--
-- Name: dataset dataset_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.dataset
    ADD CONSTRAINT dataset_pkey PRIMARY KEY (id);


--
-- Name: extraction extraction_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.extraction
    ADD CONSTRAINT extraction_pkey PRIMARY KEY (id);


--
-- Name: feature feature_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.feature
    ADD CONSTRAINT feature_pkey PRIMARY KEY (id);


--
-- Name: intermediate intermediate_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.intermediate
    ADD CONSTRAINT intermediate_pkey PRIMARY KEY (id);


--
-- Name: model_description model_description_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_description
    ADD CONSTRAINT model_description_pkey PRIMARY KEY (id);


--
-- Name: model_framework model_framework_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_framework
    ADD CONSTRAINT model_framework_pkey PRIMARY KEY (name);


--
-- Name: model_parameter model_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_parameter
    ADD CONSTRAINT model_parameter_pkey PRIMARY KEY (id);


--
-- Name: model_runtime model_runtime_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_pkey PRIMARY KEY (id);


--
-- Name: model_state model_state_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_state
    ADD CONSTRAINT model_state_pkey PRIMARY KEY (id);


--
-- Name: ontology_concept ontology_concept_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.ontology_concept
    ADD CONSTRAINT ontology_concept_pkey PRIMARY KEY (id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: project_asset project_asset_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.project_asset
    ADD CONSTRAINT project_asset_pkey PRIMARY KEY (id);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- Name: provenance provenance_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.provenance
    ADD CONSTRAINT provenance_pkey PRIMARY KEY (id);


--
-- Name: publication publication_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.publication
    ADD CONSTRAINT publication_pkey PRIMARY KEY (id);


--
-- Name: qualifier qualifier_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier
    ADD CONSTRAINT qualifier_pkey PRIMARY KEY (id);


--
-- Name: qualifier_xref qualifier_xref_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_pkey PRIMARY KEY (id);


--
-- Name: simulation_parameter simulation_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_parameter
    ADD CONSTRAINT simulation_parameter_pkey PRIMARY KEY (id);


--
-- Name: simulation_plan simulation_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_plan
    ADD CONSTRAINT simulation_plan_pkey PRIMARY KEY (id);


--
-- Name: simulation_run simulation_run_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_run
    ADD CONSTRAINT simulation_run_pkey PRIMARY KEY (id);


--
-- Name: software software_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.software
    ADD CONSTRAINT software_pkey PRIMARY KEY (id);


--
-- Name: association association_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.person(id);


--
-- Name: dataset dataset_maintainer_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.dataset
    ADD CONSTRAINT dataset_maintainer_fkey FOREIGN KEY (maintainer) REFERENCES public.person(id);


--
-- Name: extraction extraction_publication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.extraction
    ADD CONSTRAINT extraction_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES public.publication(id);


--
-- Name: feature feature_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.feature
    ADD CONSTRAINT feature_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id);


--
-- Name: model_description model_description_framework_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_description
    ADD CONSTRAINT model_description_framework_fkey FOREIGN KEY (framework) REFERENCES public.model_framework(name);


--
-- Name: model_description model_description_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_description
    ADD CONSTRAINT model_description_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.model_state(id);


--
-- Name: model_parameter model_parameter_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_parameter
    ADD CONSTRAINT model_parameter_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model_description(id);


--
-- Name: model_runtime model_runtime_left_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_left_fkey FOREIGN KEY ("left") REFERENCES public.model_framework(name);


--
-- Name: model_runtime model_runtime_right_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_right_fkey FOREIGN KEY ("right") REFERENCES public.model_framework(name);


--
-- Name: ontology_concept ontology_concept_curie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.ontology_concept
    ADD CONSTRAINT ontology_concept_curie_fkey FOREIGN KEY (curie) REFERENCES public.active_concept(curie);


--
-- Name: project_asset project_asset_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.project_asset
    ADD CONSTRAINT project_asset_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: provenance provenance_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.provenance
    ADD CONSTRAINT provenance_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.person(id);


--
-- Name: qualifier qualifier_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier
    ADD CONSTRAINT qualifier_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id);


--
-- Name: qualifier_xref qualifier_xref_feature_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_feature_id_fkey FOREIGN KEY (feature_id) REFERENCES public.feature(id);


--
-- Name: qualifier_xref qualifier_xref_qualifier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_qualifier_id_fkey FOREIGN KEY (qualifier_id) REFERENCES public.qualifier(id);


--
-- Name: simulation_parameter simulation_parameter_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_parameter
    ADD CONSTRAINT simulation_parameter_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.simulation_run(id);


--
-- Name: simulation_plan simulation_plan_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_plan
    ADD CONSTRAINT simulation_plan_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model_description(id);


--
-- Name: simulation_run simulation_run_simulator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_run
    ADD CONSTRAINT simulation_run_simulator_id_fkey FOREIGN KEY (simulator_id) REFERENCES public.simulation_plan(id);


--
-- PostgreSQL database dump complete
--

