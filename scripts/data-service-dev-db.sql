toc.dat                                                                                             0000600 0004000 0002000 00000143320 14341155237 0014447 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP           :    
        
    z            askem    15.1 (Debian 15.1-1.pgdg110+1)    15.1 (Homebrew) �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         �           1262    16384    askem    DATABASE     p   CREATE DATABASE askem WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE askem;
                dev    false         p           1247    16398    extractedtype    TYPE     X   CREATE TYPE public.extractedtype AS ENUM (
    'equation',
    'figure',
    'table'
);
     DROP TYPE public.extractedtype;
       public          dev    false                    1247    16452    intermediateformat    TYPE     h   CREATE TYPE public.intermediateformat AS ENUM (
    'bilayer',
    'gromet',
    'other',
    'sbml'
);
 %   DROP TYPE public.intermediateformat;
       public          dev    false         |           1247    16446    intermediatesource    TYPE     W   CREATE TYPE public.intermediatesource AS ENUM (
    'mrepresentationa',
    'skema'
);
 %   DROP TYPE public.intermediatesource;
       public          dev    false         �           1247    16486    ontologicalfield    TYPE     G   CREATE TYPE public.ontologicalfield AS ENUM (
    'obj',
    'unit'
);
 #   DROP TYPE public.ontologicalfield;
       public          dev    false         v           1247    16422    relationtype    TYPE     �   CREATE TYPE public.relationtype AS ENUM (
    'cites',
    'copiedfrom',
    'derivedfrom',
    'editedFrom',
    'gluedFrom',
    'stratifiedFrom'
);
    DROP TYPE public.relationtype;
       public          dev    false         s           1247    16406    resourcetype    TYPE     �   CREATE TYPE public.resourcetype AS ENUM (
    'datasets',
    'extractions',
    'intermediates',
    'models',
    'plans',
    'publications',
    'simulation_runs'
);
    DROP TYPE public.resourcetype;
       public          dev    false         y           1247    16436    role    TYPE     d   CREATE TYPE public.role AS ENUM (
    'author',
    'contributor',
    'maintainer',
    'other'
);
    DROP TYPE public.role;
       public          dev    false         �           1247    16462    taggabletype    TYPE     	  CREATE TYPE public.taggabletype AS ENUM (
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
    DROP TYPE public.taggabletype;
       public          dev    false         m           1247    16386 	   valuetype    TYPE     f   CREATE TYPE public.valuetype AS ENUM (
    'binary',
    'bool',
    'float',
    'int',
    'str'
);
    DROP TYPE public.valuetype;
       public          dev    false         �            1259    16647    association    TABLE     �   CREATE TABLE public.association (
    id integer NOT NULL,
    person_id integer NOT NULL,
    resource_id integer NOT NULL,
    resource_type public.resourcetype,
    role public.role
);
    DROP TABLE public.association;
       public         heap    dev    false    883    889         �            1259    16646    association_id_seq    SEQUENCE     �   CREATE SEQUENCE public.association_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.association_id_seq;
       public          dev    false    240         �           0    0    association_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.association_id_seq OWNED BY public.association.id;
          public          dev    false    239         �            1259    16576    dataset    TABLE     �  CREATE TABLE public.dataset (
    id integer NOT NULL,
    name character varying NOT NULL,
    url character varying NOT NULL,
    description text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    deprecated boolean,
    sensitivity text,
    quality text,
    temporal_resolution character varying,
    geospatial_resolution character varying,
    annotations json,
    maintainer integer NOT NULL
);
    DROP TABLE public.dataset;
       public         heap    dev    false         �            1259    16575    dataset_id_seq    SEQUENCE     �   CREATE SEQUENCE public.dataset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.dataset_id_seq;
       public          dev    false    230         �           0    0    dataset_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.dataset_id_seq OWNED BY public.dataset.id;
          public          dev    false    229         �            1259    16606 
   extraction    TABLE     �   CREATE TABLE public.extraction (
    id integer NOT NULL,
    publication_id integer NOT NULL,
    type public.extractedtype NOT NULL,
    data bytea NOT NULL,
    img bytea NOT NULL
);
    DROP TABLE public.extraction;
       public         heap    dev    false    880         �            1259    16605    extraction_id_seq    SEQUENCE     �   CREATE SEQUENCE public.extraction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.extraction_id_seq;
       public          dev    false    234         �           0    0    extraction_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.extraction_id_seq OWNED BY public.extraction.id;
          public          dev    false    233         �            1259    16659    feature    TABLE     �   CREATE TABLE public.feature (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    description text,
    display_name character varying,
    name character varying NOT NULL,
    value_type public.valuetype NOT NULL
);
    DROP TABLE public.feature;
       public         heap    dev    false    877         �            1259    16658    feature_id_seq    SEQUENCE     �   CREATE SEQUENCE public.feature_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.feature_id_seq;
       public          dev    false    242         �           0    0    feature_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.feature_id_seq OWNED BY public.feature.id;
          public          dev    false    241         �            1259    16499    intermediate    TABLE     �   CREATE TABLE public.intermediate (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    source public.intermediatesource NOT NULL,
    type public.intermediateformat NOT NULL,
    content bytea NOT NULL
);
     DROP TABLE public.intermediate;
       public         heap    dev    false    892    895         �            1259    16498    intermediate_id_seq    SEQUENCE     �   CREATE SEQUENCE public.intermediate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.intermediate_id_seq;
       public          dev    false    216         �           0    0    intermediate_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.intermediate_id_seq OWNED BY public.intermediate.id;
          public          dev    false    215         �            1259    16591    model    TABLE     �   CREATE TABLE public.model (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    framework character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    content json
);
    DROP TABLE public.model;
       public         heap    dev    false         �            1259    16491    model_framework    TABLE     �   CREATE TABLE public.model_framework (
    name character varying NOT NULL,
    version character varying NOT NULL,
    semantics character varying NOT NULL
);
 #   DROP TABLE public.model_framework;
       public         heap    dev    false         �            1259    16590    model_id_seq    SEQUENCE     �   CREATE SEQUENCE public.model_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.model_id_seq;
       public          dev    false    232         �           0    0    model_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.model_id_seq OWNED BY public.model.id;
          public          dev    false    231         �            1259    16701    model_parameter    TABLE     �   CREATE TABLE public.model_parameter (
    id integer NOT NULL,
    model_id integer NOT NULL,
    name character varying NOT NULL,
    type public.valuetype NOT NULL,
    default_value character varying
);
 #   DROP TABLE public.model_parameter;
       public         heap    dev    false    877         �            1259    16700    model_parameter_id_seq    SEQUENCE     �   CREATE SEQUENCE public.model_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.model_parameter_id_seq;
       public          dev    false    248         �           0    0    model_parameter_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.model_parameter_id_seq OWNED BY public.model_parameter.id;
          public          dev    false    247         �            1259    16556    model_runtime    TABLE     �   CREATE TABLE public.model_runtime (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    name character varying NOT NULL,
    "left" character varying NOT NULL,
    "right" character varying NOT NULL
);
 !   DROP TABLE public.model_runtime;
       public         heap    dev    false         �            1259    16555    model_runtime_id_seq    SEQUENCE     �   CREATE SEQUENCE public.model_runtime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.model_runtime_id_seq;
       public          dev    false    228                     0    0    model_runtime_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.model_runtime_id_seq OWNED BY public.model_runtime.id;
          public          dev    false    227         �            1259    16538    ontology_concept    TABLE     �   CREATE TABLE public.ontology_concept (
    id integer NOT NULL,
    curie character varying NOT NULL,
    type public.taggabletype NOT NULL,
    object_id integer NOT NULL,
    status public.ontologicalfield NOT NULL
);
 $   DROP TABLE public.ontology_concept;
       public         heap    dev    false    901    898         �            1259    16537    ontology_concept_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ontology_concept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.ontology_concept_id_seq;
       public          dev    false    224                    0    0    ontology_concept_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.ontology_concept_id_seq OWNED BY public.ontology_concept.id;
          public          dev    false    223         �            1259    16547    person    TABLE     �   CREATE TABLE public.person (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    org character varying,
    website character varying,
    is_registered boolean NOT NULL
);
    DROP TABLE public.person;
       public         heap    dev    false         �            1259    16546    person_id_seq    SEQUENCE     �   CREATE SEQUENCE public.person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.person_id_seq;
       public          dev    false    226                    0    0    person_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.person_id_seq OWNED BY public.person.id;
          public          dev    false    225         �            1259    16528    project    TABLE     �   CREATE TABLE public.project (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now(),
    active boolean NOT NULL
);
    DROP TABLE public.project;
       public         heap    dev    false         �            1259    16620    project_asset    TABLE     �   CREATE TABLE public.project_asset (
    id integer NOT NULL,
    project_id integer NOT NULL,
    resource_id integer NOT NULL,
    resource_type public.resourcetype NOT NULL,
    external_ref character varying
);
 !   DROP TABLE public.project_asset;
       public         heap    dev    false    883         �            1259    16619    project_asset_id_seq    SEQUENCE     �   CREATE SEQUENCE public.project_asset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.project_asset_id_seq;
       public          dev    false    236                    0    0    project_asset_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.project_asset_id_seq OWNED BY public.project_asset.id;
          public          dev    false    235         �            1259    16527    project_id_seq    SEQUENCE     �   CREATE SEQUENCE public.project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.project_id_seq;
       public          dev    false    222                    0    0    project_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.project_id_seq OWNED BY public.project.id;
          public          dev    false    221         �            1259    16634 
   provenance    TABLE     Y  CREATE TABLE public.provenance (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    relation_type public.relationtype NOT NULL,
    "left" integer NOT NULL,
    left_type public.resourcetype NOT NULL,
    "right" integer NOT NULL,
    right_type public.resourcetype NOT NULL,
    user_id integer
);
    DROP TABLE public.provenance;
       public         heap    dev    false    886    883    883         �            1259    16633    provenance_id_seq    SEQUENCE     �   CREATE SEQUENCE public.provenance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.provenance_id_seq;
       public          dev    false    238                    0    0    provenance_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.provenance_id_seq OWNED BY public.provenance.id;
          public          dev    false    237         �            1259    16519    publication    TABLE     e   CREATE TABLE public.publication (
    id integer NOT NULL,
    xdd_uri character varying NOT NULL
);
    DROP TABLE public.publication;
       public         heap    dev    false         �            1259    16518    publication_id_seq    SEQUENCE     �   CREATE SEQUENCE public.publication_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.publication_id_seq;
       public          dev    false    220                    0    0    publication_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.publication_id_seq OWNED BY public.publication.id;
          public          dev    false    219         �            1259    16673 	   qualifier    TABLE     �   CREATE TABLE public.qualifier (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    description text,
    name character varying NOT NULL,
    value_type public.valuetype NOT NULL
);
    DROP TABLE public.qualifier;
       public         heap    dev    false    877         �            1259    16672    qualifier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.qualifier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.qualifier_id_seq;
       public          dev    false    244                    0    0    qualifier_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.qualifier_id_seq OWNED BY public.qualifier.id;
          public          dev    false    243         �            1259    16715    qualifier_xref    TABLE     �   CREATE TABLE public.qualifier_xref (
    id integer NOT NULL,
    qualifier_id integer NOT NULL,
    feature_id integer NOT NULL
);
 "   DROP TABLE public.qualifier_xref;
       public         heap    dev    false         �            1259    16714    qualifier_xref_id_seq    SEQUENCE     �   CREATE SEQUENCE public.qualifier_xref_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.qualifier_xref_id_seq;
       public          dev    false    250                    0    0    qualifier_xref_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.qualifier_xref_id_seq OWNED BY public.qualifier_xref.id;
          public          dev    false    249         �            1259    16747    simulation_parameter    TABLE     �   CREATE TABLE public.simulation_parameter (
    id integer NOT NULL,
    run_id integer NOT NULL,
    name character varying NOT NULL,
    value character varying NOT NULL,
    type public.valuetype NOT NULL
);
 (   DROP TABLE public.simulation_parameter;
       public         heap    dev    false    877         �            1259    16746    simulation_parameter_id_seq    SEQUENCE     �   CREATE SEQUENCE public.simulation_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.simulation_parameter_id_seq;
       public          dev    false    254         	           0    0    simulation_parameter_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.simulation_parameter_id_seq OWNED BY public.simulation_parameter.id;
          public          dev    false    253         �            1259    16687    simulation_plan    TABLE     �   CREATE TABLE public.simulation_plan (
    id integer NOT NULL,
    model_id integer NOT NULL,
    simulator character varying NOT NULL,
    query character varying NOT NULL,
    content json NOT NULL
);
 #   DROP TABLE public.simulation_plan;
       public         heap    dev    false         �            1259    16686    simulation_plan_id_seq    SEQUENCE     �   CREATE SEQUENCE public.simulation_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.simulation_plan_id_seq;
       public          dev    false    246         
           0    0    simulation_plan_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.simulation_plan_id_seq OWNED BY public.simulation_plan.id;
          public          dev    false    245         �            1259    16732    simulation_run    TABLE     �   CREATE TABLE public.simulation_run (
    id integer NOT NULL,
    simulator_id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    completed_at timestamp without time zone,
    success boolean,
    response bytea
);
 "   DROP TABLE public.simulation_run;
       public         heap    dev    false         �            1259    16731    simulation_run_id_seq    SEQUENCE     �   CREATE SEQUENCE public.simulation_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.simulation_run_id_seq;
       public          dev    false    252                    0    0    simulation_run_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.simulation_run_id_seq OWNED BY public.simulation_run.id;
          public          dev    false    251         �            1259    16509    software    TABLE     �   CREATE TABLE public.software (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    source character varying NOT NULL,
    storage_uri character varying NOT NULL
);
    DROP TABLE public.software;
       public         heap    dev    false         �            1259    16508    software_id_seq    SEQUENCE     �   CREATE SEQUENCE public.software_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.software_id_seq;
       public          dev    false    218                    0    0    software_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.software_id_seq OWNED BY public.software.id;
          public          dev    false    217         �           2604    16650    association id    DEFAULT     p   ALTER TABLE ONLY public.association ALTER COLUMN id SET DEFAULT nextval('public.association_id_seq'::regclass);
 =   ALTER TABLE public.association ALTER COLUMN id DROP DEFAULT;
       public          dev    false    240    239    240         �           2604    16579 
   dataset id    DEFAULT     h   ALTER TABLE ONLY public.dataset ALTER COLUMN id SET DEFAULT nextval('public.dataset_id_seq'::regclass);
 9   ALTER TABLE public.dataset ALTER COLUMN id DROP DEFAULT;
       public          dev    false    229    230    230         �           2604    16609    extraction id    DEFAULT     n   ALTER TABLE ONLY public.extraction ALTER COLUMN id SET DEFAULT nextval('public.extraction_id_seq'::regclass);
 <   ALTER TABLE public.extraction ALTER COLUMN id DROP DEFAULT;
       public          dev    false    234    233    234         �           2604    16662 
   feature id    DEFAULT     h   ALTER TABLE ONLY public.feature ALTER COLUMN id SET DEFAULT nextval('public.feature_id_seq'::regclass);
 9   ALTER TABLE public.feature ALTER COLUMN id DROP DEFAULT;
       public          dev    false    242    241    242         �           2604    16502    intermediate id    DEFAULT     r   ALTER TABLE ONLY public.intermediate ALTER COLUMN id SET DEFAULT nextval('public.intermediate_id_seq'::regclass);
 >   ALTER TABLE public.intermediate ALTER COLUMN id DROP DEFAULT;
       public          dev    false    215    216    216         �           2604    16594    model id    DEFAULT     d   ALTER TABLE ONLY public.model ALTER COLUMN id SET DEFAULT nextval('public.model_id_seq'::regclass);
 7   ALTER TABLE public.model ALTER COLUMN id DROP DEFAULT;
       public          dev    false    232    231    232         �           2604    16704    model_parameter id    DEFAULT     x   ALTER TABLE ONLY public.model_parameter ALTER COLUMN id SET DEFAULT nextval('public.model_parameter_id_seq'::regclass);
 A   ALTER TABLE public.model_parameter ALTER COLUMN id DROP DEFAULT;
       public          dev    false    247    248    248         �           2604    16559    model_runtime id    DEFAULT     t   ALTER TABLE ONLY public.model_runtime ALTER COLUMN id SET DEFAULT nextval('public.model_runtime_id_seq'::regclass);
 ?   ALTER TABLE public.model_runtime ALTER COLUMN id DROP DEFAULT;
       public          dev    false    228    227    228         �           2604    16541    ontology_concept id    DEFAULT     z   ALTER TABLE ONLY public.ontology_concept ALTER COLUMN id SET DEFAULT nextval('public.ontology_concept_id_seq'::regclass);
 B   ALTER TABLE public.ontology_concept ALTER COLUMN id DROP DEFAULT;
       public          dev    false    224    223    224         �           2604    16550 	   person id    DEFAULT     f   ALTER TABLE ONLY public.person ALTER COLUMN id SET DEFAULT nextval('public.person_id_seq'::regclass);
 8   ALTER TABLE public.person ALTER COLUMN id DROP DEFAULT;
       public          dev    false    225    226    226         �           2604    16531 
   project id    DEFAULT     h   ALTER TABLE ONLY public.project ALTER COLUMN id SET DEFAULT nextval('public.project_id_seq'::regclass);
 9   ALTER TABLE public.project ALTER COLUMN id DROP DEFAULT;
       public          dev    false    222    221    222         �           2604    16623    project_asset id    DEFAULT     t   ALTER TABLE ONLY public.project_asset ALTER COLUMN id SET DEFAULT nextval('public.project_asset_id_seq'::regclass);
 ?   ALTER TABLE public.project_asset ALTER COLUMN id DROP DEFAULT;
       public          dev    false    236    235    236         �           2604    16637    provenance id    DEFAULT     n   ALTER TABLE ONLY public.provenance ALTER COLUMN id SET DEFAULT nextval('public.provenance_id_seq'::regclass);
 <   ALTER TABLE public.provenance ALTER COLUMN id DROP DEFAULT;
       public          dev    false    237    238    238         �           2604    16522    publication id    DEFAULT     p   ALTER TABLE ONLY public.publication ALTER COLUMN id SET DEFAULT nextval('public.publication_id_seq'::regclass);
 =   ALTER TABLE public.publication ALTER COLUMN id DROP DEFAULT;
       public          dev    false    219    220    220         �           2604    16676    qualifier id    DEFAULT     l   ALTER TABLE ONLY public.qualifier ALTER COLUMN id SET DEFAULT nextval('public.qualifier_id_seq'::regclass);
 ;   ALTER TABLE public.qualifier ALTER COLUMN id DROP DEFAULT;
       public          dev    false    244    243    244         �           2604    16718    qualifier_xref id    DEFAULT     v   ALTER TABLE ONLY public.qualifier_xref ALTER COLUMN id SET DEFAULT nextval('public.qualifier_xref_id_seq'::regclass);
 @   ALTER TABLE public.qualifier_xref ALTER COLUMN id DROP DEFAULT;
       public          dev    false    249    250    250                    2604    16750    simulation_parameter id    DEFAULT     �   ALTER TABLE ONLY public.simulation_parameter ALTER COLUMN id SET DEFAULT nextval('public.simulation_parameter_id_seq'::regclass);
 F   ALTER TABLE public.simulation_parameter ALTER COLUMN id DROP DEFAULT;
       public          dev    false    254    253    254         �           2604    16690    simulation_plan id    DEFAULT     x   ALTER TABLE ONLY public.simulation_plan ALTER COLUMN id SET DEFAULT nextval('public.simulation_plan_id_seq'::regclass);
 A   ALTER TABLE public.simulation_plan ALTER COLUMN id DROP DEFAULT;
       public          dev    false    246    245    246         �           2604    16735    simulation_run id    DEFAULT     v   ALTER TABLE ONLY public.simulation_run ALTER COLUMN id SET DEFAULT nextval('public.simulation_run_id_seq'::regclass);
 @   ALTER TABLE public.simulation_run ALTER COLUMN id DROP DEFAULT;
       public          dev    false    252    251    252         �           2604    16512    software id    DEFAULT     j   ALTER TABLE ONLY public.software ALTER COLUMN id SET DEFAULT nextval('public.software_id_seq'::regclass);
 :   ALTER TABLE public.software ALTER COLUMN id DROP DEFAULT;
       public          dev    false    217    218    218         �          0    16647    association 
   TABLE DATA           V   COPY public.association (id, person_id, resource_id, resource_type, role) FROM stdin;
    public          dev    false    240       3556.dat �          0    16576    dataset 
   TABLE DATA           �   COPY public.dataset (id, name, url, description, "timestamp", deprecated, sensitivity, quality, temporal_resolution, geospatial_resolution, annotations, maintainer) FROM stdin;
    public          dev    false    230       3546.dat �          0    16606 
   extraction 
   TABLE DATA           I   COPY public.extraction (id, publication_id, type, data, img) FROM stdin;
    public          dev    false    234       3550.dat �          0    16659    feature 
   TABLE DATA           ^   COPY public.feature (id, dataset_id, description, display_name, name, value_type) FROM stdin;
    public          dev    false    242       3558.dat �          0    16499    intermediate 
   TABLE DATA           N   COPY public.intermediate (id, "timestamp", source, type, content) FROM stdin;
    public          dev    false    216       3532.dat �          0    16591    model 
   TABLE DATA           W   COPY public.model (id, name, description, framework, "timestamp", content) FROM stdin;
    public          dev    false    232       3548.dat �          0    16491    model_framework 
   TABLE DATA           C   COPY public.model_framework (name, version, semantics) FROM stdin;
    public          dev    false    214       3530.dat �          0    16701    model_parameter 
   TABLE DATA           R   COPY public.model_parameter (id, model_id, name, type, default_value) FROM stdin;
    public          dev    false    248       3564.dat �          0    16556    model_runtime 
   TABLE DATA           O   COPY public.model_runtime (id, "timestamp", name, "left", "right") FROM stdin;
    public          dev    false    228       3544.dat �          0    16538    ontology_concept 
   TABLE DATA           N   COPY public.ontology_concept (id, curie, type, object_id, status) FROM stdin;
    public          dev    false    224       3540.dat �          0    16547    person 
   TABLE DATA           N   COPY public.person (id, name, email, org, website, is_registered) FROM stdin;
    public          dev    false    226       3542.dat �          0    16528    project 
   TABLE DATA           M   COPY public.project (id, name, description, "timestamp", active) FROM stdin;
    public          dev    false    222       3538.dat �          0    16620    project_asset 
   TABLE DATA           a   COPY public.project_asset (id, project_id, resource_id, resource_type, external_ref) FROM stdin;
    public          dev    false    236       3552.dat �          0    16634 
   provenance 
   TABLE DATA           u   COPY public.provenance (id, "timestamp", relation_type, "left", left_type, "right", right_type, user_id) FROM stdin;
    public          dev    false    238       3554.dat �          0    16519    publication 
   TABLE DATA           2   COPY public.publication (id, xdd_uri) FROM stdin;
    public          dev    false    220       3536.dat �          0    16673 	   qualifier 
   TABLE DATA           R   COPY public.qualifier (id, dataset_id, description, name, value_type) FROM stdin;
    public          dev    false    244       3560.dat �          0    16715    qualifier_xref 
   TABLE DATA           F   COPY public.qualifier_xref (id, qualifier_id, feature_id) FROM stdin;
    public          dev    false    250       3566.dat �          0    16747    simulation_parameter 
   TABLE DATA           M   COPY public.simulation_parameter (id, run_id, name, value, type) FROM stdin;
    public          dev    false    254       3570.dat �          0    16687    simulation_plan 
   TABLE DATA           R   COPY public.simulation_plan (id, model_id, simulator, query, content) FROM stdin;
    public          dev    false    246       3562.dat �          0    16732    simulation_run 
   TABLE DATA           h   COPY public.simulation_run (id, simulator_id, "timestamp", completed_at, success, response) FROM stdin;
    public          dev    false    252       3568.dat �          0    16509    software 
   TABLE DATA           H   COPY public.software (id, "timestamp", source, storage_uri) FROM stdin;
    public          dev    false    218       3534.dat            0    0    association_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.association_id_seq', 1, false);
          public          dev    false    239                    0    0    dataset_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.dataset_id_seq', 23, true);
          public          dev    false    229                    0    0    extraction_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.extraction_id_seq', 1, false);
          public          dev    false    233                    0    0    feature_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.feature_id_seq', 161, true);
          public          dev    false    241                    0    0    intermediate_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.intermediate_id_seq', 24, true);
          public          dev    false    215                    0    0    model_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.model_id_seq', 1, false);
          public          dev    false    231                    0    0    model_parameter_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.model_parameter_id_seq', 1, false);
          public          dev    false    247                    0    0    model_runtime_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.model_runtime_id_seq', 1, false);
          public          dev    false    227                    0    0    ontology_concept_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.ontology_concept_id_seq', 48, true);
          public          dev    false    223                    0    0    person_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.person_id_seq', 1, true);
          public          dev    false    225                    0    0    project_asset_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.project_asset_id_seq', 71, true);
          public          dev    false    235                    0    0    project_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.project_id_seq', 1, true);
          public          dev    false    221                    0    0    provenance_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.provenance_id_seq', 24, true);
          public          dev    false    237                    0    0    publication_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.publication_id_seq', 24, true);
          public          dev    false    219                    0    0    qualifier_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.qualifier_id_seq', 23, true);
          public          dev    false    243                    0    0    qualifier_xref_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.qualifier_xref_id_seq', 161, true);
          public          dev    false    249                    0    0    simulation_parameter_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.simulation_parameter_id_seq', 1, false);
          public          dev    false    253                    0    0    simulation_plan_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.simulation_plan_id_seq', 1, false);
          public          dev    false    245                    0    0    simulation_run_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.simulation_run_id_seq', 1, false);
          public          dev    false    251                     0    0    software_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.software_id_seq', 1, false);
          public          dev    false    217                    2606    16652    association association_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.association DROP CONSTRAINT association_pkey;
       public            dev    false    240                    2606    16584    dataset dataset_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.dataset
    ADD CONSTRAINT dataset_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.dataset DROP CONSTRAINT dataset_pkey;
       public            dev    false    230                    2606    16613    extraction extraction_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.extraction
    ADD CONSTRAINT extraction_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.extraction DROP CONSTRAINT extraction_pkey;
       public            dev    false    234                    2606    16666    feature feature_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.feature
    ADD CONSTRAINT feature_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.feature DROP CONSTRAINT feature_pkey;
       public            dev    false    242                    2606    16507    intermediate intermediate_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.intermediate
    ADD CONSTRAINT intermediate_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.intermediate DROP CONSTRAINT intermediate_pkey;
       public            dev    false    216                    2606    16497 $   model_framework model_framework_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.model_framework
    ADD CONSTRAINT model_framework_pkey PRIMARY KEY (name);
 N   ALTER TABLE ONLY public.model_framework DROP CONSTRAINT model_framework_pkey;
       public            dev    false    214         %           2606    16708 $   model_parameter model_parameter_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.model_parameter
    ADD CONSTRAINT model_parameter_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.model_parameter DROP CONSTRAINT model_parameter_pkey;
       public            dev    false    248                    2606    16599    model model_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.model DROP CONSTRAINT model_pkey;
       public            dev    false    232                    2606    16564     model_runtime model_runtime_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.model_runtime DROP CONSTRAINT model_runtime_pkey;
       public            dev    false    228                    2606    16545 &   ontology_concept ontology_concept_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.ontology_concept
    ADD CONSTRAINT ontology_concept_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.ontology_concept DROP CONSTRAINT ontology_concept_pkey;
       public            dev    false    224                    2606    16554    person person_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.person DROP CONSTRAINT person_pkey;
       public            dev    false    226                    2606    16627     project_asset project_asset_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.project_asset
    ADD CONSTRAINT project_asset_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.project_asset DROP CONSTRAINT project_asset_pkey;
       public            dev    false    236                    2606    16536    project project_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.project DROP CONSTRAINT project_pkey;
       public            dev    false    222                    2606    16640    provenance provenance_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.provenance
    ADD CONSTRAINT provenance_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.provenance DROP CONSTRAINT provenance_pkey;
       public            dev    false    238         	           2606    16526    publication publication_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.publication
    ADD CONSTRAINT publication_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.publication DROP CONSTRAINT publication_pkey;
       public            dev    false    220         !           2606    16680    qualifier qualifier_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.qualifier
    ADD CONSTRAINT qualifier_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.qualifier DROP CONSTRAINT qualifier_pkey;
       public            dev    false    244         '           2606    16720 "   qualifier_xref qualifier_xref_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.qualifier_xref DROP CONSTRAINT qualifier_xref_pkey;
       public            dev    false    250         +           2606    16754 .   simulation_parameter simulation_parameter_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.simulation_parameter
    ADD CONSTRAINT simulation_parameter_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.simulation_parameter DROP CONSTRAINT simulation_parameter_pkey;
       public            dev    false    254         #           2606    16694 $   simulation_plan simulation_plan_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.simulation_plan
    ADD CONSTRAINT simulation_plan_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.simulation_plan DROP CONSTRAINT simulation_plan_pkey;
       public            dev    false    246         )           2606    16740 "   simulation_run simulation_run_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.simulation_run
    ADD CONSTRAINT simulation_run_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.simulation_run DROP CONSTRAINT simulation_run_pkey;
       public            dev    false    252                    2606    16517    software software_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.software
    ADD CONSTRAINT software_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.software DROP CONSTRAINT software_pkey;
       public            dev    false    218         3           2606    16653 &   association association_person_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.association
    ADD CONSTRAINT association_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.person(id);
 P   ALTER TABLE ONLY public.association DROP CONSTRAINT association_person_id_fkey;
       public          dev    false    240    3343    226         .           2606    16585    dataset dataset_maintainer_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dataset
    ADD CONSTRAINT dataset_maintainer_fkey FOREIGN KEY (maintainer) REFERENCES public.person(id);
 I   ALTER TABLE ONLY public.dataset DROP CONSTRAINT dataset_maintainer_fkey;
       public          dev    false    3343    226    230         0           2606    16614 )   extraction extraction_publication_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.extraction
    ADD CONSTRAINT extraction_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES public.publication(id);
 S   ALTER TABLE ONLY public.extraction DROP CONSTRAINT extraction_publication_id_fkey;
       public          dev    false    220    3337    234         4           2606    16667    feature feature_dataset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.feature
    ADD CONSTRAINT feature_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id);
 I   ALTER TABLE ONLY public.feature DROP CONSTRAINT feature_dataset_id_fkey;
       public          dev    false    242    230    3347         /           2606    16600    model model_framework_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_framework_fkey FOREIGN KEY (framework) REFERENCES public.model_framework(name);
 D   ALTER TABLE ONLY public.model DROP CONSTRAINT model_framework_fkey;
       public          dev    false    214    232    3331         7           2606    16709 -   model_parameter model_parameter_model_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.model_parameter
    ADD CONSTRAINT model_parameter_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model(id);
 W   ALTER TABLE ONLY public.model_parameter DROP CONSTRAINT model_parameter_model_id_fkey;
       public          dev    false    248    3349    232         ,           2606    16565 %   model_runtime model_runtime_left_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_left_fkey FOREIGN KEY ("left") REFERENCES public.model_framework(name);
 O   ALTER TABLE ONLY public.model_runtime DROP CONSTRAINT model_runtime_left_fkey;
       public          dev    false    3331    228    214         -           2606    16570 &   model_runtime model_runtime_right_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_right_fkey FOREIGN KEY ("right") REFERENCES public.model_framework(name);
 P   ALTER TABLE ONLY public.model_runtime DROP CONSTRAINT model_runtime_right_fkey;
       public          dev    false    228    214    3331         1           2606    16628 +   project_asset project_asset_project_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.project_asset
    ADD CONSTRAINT project_asset_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);
 U   ALTER TABLE ONLY public.project_asset DROP CONSTRAINT project_asset_project_id_fkey;
       public          dev    false    3339    222    236         2           2606    16641 "   provenance provenance_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.provenance
    ADD CONSTRAINT provenance_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.person(id);
 L   ALTER TABLE ONLY public.provenance DROP CONSTRAINT provenance_user_id_fkey;
       public          dev    false    238    226    3343         5           2606    16681 #   qualifier qualifier_dataset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.qualifier
    ADD CONSTRAINT qualifier_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id);
 M   ALTER TABLE ONLY public.qualifier DROP CONSTRAINT qualifier_dataset_id_fkey;
       public          dev    false    244    3347    230         8           2606    16726 -   qualifier_xref qualifier_xref_feature_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_feature_id_fkey FOREIGN KEY (feature_id) REFERENCES public.feature(id);
 W   ALTER TABLE ONLY public.qualifier_xref DROP CONSTRAINT qualifier_xref_feature_id_fkey;
       public          dev    false    242    250    3359         9           2606    16721 /   qualifier_xref qualifier_xref_qualifier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.qualifier_xref
    ADD CONSTRAINT qualifier_xref_qualifier_id_fkey FOREIGN KEY (qualifier_id) REFERENCES public.qualifier(id);
 Y   ALTER TABLE ONLY public.qualifier_xref DROP CONSTRAINT qualifier_xref_qualifier_id_fkey;
       public          dev    false    244    3361    250         ;           2606    16755 5   simulation_parameter simulation_parameter_run_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.simulation_parameter
    ADD CONSTRAINT simulation_parameter_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.simulation_run(id);
 _   ALTER TABLE ONLY public.simulation_parameter DROP CONSTRAINT simulation_parameter_run_id_fkey;
       public          dev    false    3369    254    252         6           2606    16695 -   simulation_plan simulation_plan_model_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.simulation_plan
    ADD CONSTRAINT simulation_plan_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model(id);
 W   ALTER TABLE ONLY public.simulation_plan DROP CONSTRAINT simulation_plan_model_id_fkey;
       public          dev    false    246    3349    232         :           2606    16741 /   simulation_run simulation_run_simulator_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.simulation_run
    ADD CONSTRAINT simulation_run_simulator_id_fkey FOREIGN KEY (simulator_id) REFERENCES public.simulation_plan(id);
 Y   ALTER TABLE ONLY public.simulation_run DROP CONSTRAINT simulation_run_simulator_id_fkey;
       public          dev    false    252    246    3363                                                                                                                                                                                                                                                                                                                        3556.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014254 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3546.dat                                                                                            0000600 0004000 0002000 00000206026 14341155237 0014266 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	Biomodel simulation output 1		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/1/sim_output.csv"]}	1
2	Biomodel simulation output 2		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/2/sim_output.csv"]}	1
3	Biomodel simulation output 3		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/3/sim_output.csv"]}	1
4	Biomodel simulation output 4		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/4/sim_output.csv"]}	1
5	Biomodel simulation output 5		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/5/sim_output.csv"]}	1
6	Biomodel simulation output 6		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/6/sim_output.csv"]}	1
7	Biomodel simulation output 7		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/7/sim_output.csv"]}	1
8	Biomodel simulation output 8		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/8/sim_output.csv"]}	1
9	Biomodel simulation output 9		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/9/sim_output.csv"]}	1
10	Biomodel simulation output 10		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/10/sim_output.csv"]}	1
12	Biomodel simulation output 12		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/12/sim_output.csv"]}	1
14	Biomodel simulation output 14		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/14/sim_output.csv"]}	1
16	Biomodel simulation output 16		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/16/sim_output.csv"]}	1
18	Biomodel simulation output 18		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/18/sim_output.csv"]}	1
20	Biomodel simulation output 20		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/20/sim_output.csv"]}	1
22	Biomodel simulation output 22		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_8", "display_name": "", "description": "state feature 8", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_9", "display_name": "", "description": "state feature 9", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_10", "display_name": "", "description": "state feature 10", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7", "state_8", "state_9", "state_10"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/22/sim_output.csv"]}	1
11	Biomodel simulation output 11		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/11/sim_output.csv"]}	1
13	Biomodel simulation output 13		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/13/sim_output.csv"]}	1
15	Biomodel simulation output 15		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_8", "display_name": "", "description": "state feature 8", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_9", "display_name": "", "description": "state feature 9", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_10", "display_name": "", "description": "state feature 10", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_11", "display_name": "", "description": "state feature 11", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_12", "display_name": "", "description": "state feature 12", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_13", "display_name": "", "description": "state feature 13", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_14", "display_name": "", "description": "state feature 14", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_15", "display_name": "", "description": "state feature 15", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_16", "display_name": "", "description": "state feature 16", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_17", "display_name": "", "description": "state feature 17", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_18", "display_name": "", "description": "state feature 18", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_19", "display_name": "", "description": "state feature 19", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_20", "display_name": "", "description": "state feature 20", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_21", "display_name": "", "description": "state feature 21", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_22", "display_name": "", "description": "state feature 22", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_23", "display_name": "", "description": "state feature 23", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_24", "display_name": "", "description": "state feature 24", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_25", "display_name": "", "description": "state feature 25", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_26", "display_name": "", "description": "state feature 26", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_27", "display_name": "", "description": "state feature 27", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7", "state_8", "state_9", "state_10", "state_11", "state_12", "state_13", "state_14", "state_15", "state_16", "state_17", "state_18", "state_19", "state_20", "state_21", "state_22", "state_23", "state_24", "state_25", "state_26", "state_27"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/15/sim_output.csv"]}	1
17	Biomodel simulation output 17		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/17/sim_output.csv"]}	1
19	Biomodel simulation output 19		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/19/sim_output.csv"]}	1
21	Biomodel simulation output 21		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/21/sim_output.csv"]}	1
23	Biomodel simulation output 23		Biomodel simulation output registered as a dataset	2022-11-28 15:41:02.986569	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "state_0", "display_name": "", "description": "state feature 0", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_1", "display_name": "", "description": "state feature 1", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_2", "display_name": "", "description": "state feature 2", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_3", "display_name": "", "description": "state feature 3", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_4", "display_name": "", "description": "state feature 4", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_5", "display_name": "", "description": "state feature 5", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_6", "display_name": "", "description": "state feature 6", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_7", "display_name": "", "description": "state feature 7", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_8", "display_name": "", "description": "state feature 8", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_9", "display_name": "", "description": "state feature 9", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_10", "display_name": "", "description": "state feature 10", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_11", "display_name": "", "description": "state feature 11", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "state_12", "display_name": "", "description": "state feature 12", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7", "state_8", "state_9", "state_10", "state_11", "state_12"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["file:///datasets/23/sim_output.csv"]}	1
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          3550.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014246 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3558.dat                                                                                            0000600 0004000 0002000 00000015767 14341155237 0014303 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	State Feature 0	state_0	state_0	float
2	1	State Feature 1	state_1	state_1	float
3	1	State Feature 2	state_2	state_2	float
4	1	State Feature 3	state_3	state_3	float
5	2	State Feature 0	state_0	state_0	float
6	2	State Feature 1	state_1	state_1	float
7	2	State Feature 2	state_2	state_2	float
8	2	State Feature 3	state_3	state_3	float
9	2	State Feature 4	state_4	state_4	float
10	2	State Feature 5	state_5	state_5	float
11	2	State Feature 6	state_6	state_6	float
12	3	State Feature 0	state_0	state_0	float
13	3	State Feature 1	state_1	state_1	float
14	3	State Feature 2	state_2	state_2	float
15	3	State Feature 3	state_3	state_3	float
16	3	State Feature 4	state_4	state_4	float
17	3	State Feature 5	state_5	state_5	float
18	3	State Feature 6	state_6	state_6	float
19	3	State Feature 7	state_7	state_7	float
20	4	State Feature 0	state_0	state_0	float
21	4	State Feature 1	state_1	state_1	float
22	4	State Feature 2	state_2	state_2	float
23	4	State Feature 3	state_3	state_3	float
24	4	State Feature 4	state_4	state_4	float
25	4	State Feature 5	state_5	state_5	float
26	5	State Feature 0	state_0	state_0	float
27	5	State Feature 1	state_1	state_1	float
28	5	State Feature 2	state_2	state_2	float
29	6	State Feature 0	state_0	state_0	float
30	6	State Feature 1	state_1	state_1	float
31	6	State Feature 2	state_2	state_2	float
32	6	State Feature 3	state_3	state_3	float
33	6	State Feature 4	state_4	state_4	float
34	7	State Feature 0	state_0	state_0	float
35	7	State Feature 1	state_1	state_1	float
36	7	State Feature 2	state_2	state_2	float
37	7	State Feature 3	state_3	state_3	float
38	7	State Feature 4	state_4	state_4	float
39	8	State Feature 0	state_0	state_0	float
40	8	State Feature 1	state_1	state_1	float
41	8	State Feature 2	state_2	state_2	float
42	8	State Feature 3	state_3	state_3	float
43	8	State Feature 4	state_4	state_4	float
44	9	State Feature 0	state_0	state_0	float
45	9	State Feature 1	state_1	state_1	float
46	9	State Feature 2	state_2	state_2	float
47	9	State Feature 3	state_3	state_3	float
48	9	State Feature 4	state_4	state_4	float
49	9	State Feature 5	state_5	state_5	float
50	10	State Feature 0	state_0	state_0	float
51	10	State Feature 1	state_1	state_1	float
52	10	State Feature 2	state_2	state_2	float
53	10	State Feature 3	state_3	state_3	float
54	11	State Feature 0	state_0	state_0	float
55	11	State Feature 1	state_1	state_1	float
56	11	State Feature 2	state_2	state_2	float
57	12	State Feature 0	state_0	state_0	float
58	12	State Feature 1	state_1	state_1	float
59	12	State Feature 2	state_2	state_2	float
60	12	State Feature 3	state_3	state_3	float
61	12	State Feature 4	state_4	state_4	float
62	12	State Feature 5	state_5	state_5	float
63	12	State Feature 6	state_6	state_6	float
64	12	State Feature 7	state_7	state_7	float
65	13	State Feature 0	state_0	state_0	float
66	13	State Feature 1	state_1	state_1	float
67	13	State Feature 2	state_2	state_2	float
68	13	State Feature 3	state_3	state_3	float
69	14	State Feature 0	state_0	state_0	float
70	14	State Feature 1	state_1	state_1	float
71	14	State Feature 2	state_2	state_2	float
72	14	State Feature 3	state_3	state_3	float
73	15	State Feature 0	state_0	state_0	float
74	15	State Feature 1	state_1	state_1	float
75	15	State Feature 2	state_2	state_2	float
76	15	State Feature 3	state_3	state_3	float
77	15	State Feature 4	state_4	state_4	float
78	15	State Feature 5	state_5	state_5	float
79	15	State Feature 6	state_6	state_6	float
80	15	State Feature 7	state_7	state_7	float
81	15	State Feature 8	state_8	state_8	float
82	15	State Feature 9	state_9	state_9	float
83	15	State Feature 10	state_10	state_10	float
84	15	State Feature 11	state_11	state_11	float
85	15	State Feature 12	state_12	state_12	float
86	15	State Feature 13	state_13	state_13	float
87	15	State Feature 14	state_14	state_14	float
88	15	State Feature 15	state_15	state_15	float
89	15	State Feature 16	state_16	state_16	float
90	15	State Feature 17	state_17	state_17	float
91	15	State Feature 18	state_18	state_18	float
92	15	State Feature 19	state_19	state_19	float
93	15	State Feature 20	state_20	state_20	float
94	15	State Feature 21	state_21	state_21	float
95	15	State Feature 22	state_22	state_22	float
96	15	State Feature 23	state_23	state_23	float
97	15	State Feature 24	state_24	state_24	float
98	15	State Feature 25	state_25	state_25	float
99	15	State Feature 26	state_26	state_26	float
100	15	State Feature 27	state_27	state_27	float
101	16	State Feature 0	state_0	state_0	float
102	16	State Feature 1	state_1	state_1	float
103	16	State Feature 2	state_2	state_2	float
104	17	State Feature 0	state_0	state_0	float
105	17	State Feature 1	state_1	state_1	float
106	17	State Feature 2	state_2	state_2	float
107	17	State Feature 3	state_3	state_3	float
108	17	State Feature 4	state_4	state_4	float
109	17	State Feature 5	state_5	state_5	float
110	17	State Feature 6	state_6	state_6	float
119	19	State Feature 0	state_0	state_0	float
120	19	State Feature 1	state_1	state_1	float
121	19	State Feature 2	state_2	state_2	float
122	19	State Feature 3	state_3	state_3	float
123	19	State Feature 4	state_4	state_4	float
130	21	State Feature 0	state_0	state_0	float
131	21	State Feature 1	state_1	state_1	float
132	21	State Feature 2	state_2	state_2	float
133	21	State Feature 3	state_3	state_3	float
134	21	State Feature 4	state_4	state_4	float
135	21	State Feature 5	state_5	state_5	float
136	21	State Feature 6	state_6	state_6	float
137	21	State Feature 7	state_7	state_7	float
149	23	State Feature 0	state_0	state_0	float
150	23	State Feature 1	state_1	state_1	float
151	23	State Feature 2	state_2	state_2	float
152	23	State Feature 3	state_3	state_3	float
153	23	State Feature 4	state_4	state_4	float
154	23	State Feature 5	state_5	state_5	float
155	23	State Feature 6	state_6	state_6	float
156	23	State Feature 7	state_7	state_7	float
157	23	State Feature 8	state_8	state_8	float
158	23	State Feature 9	state_9	state_9	float
159	23	State Feature 10	state_10	state_10	float
160	23	State Feature 11	state_11	state_11	float
161	23	State Feature 12	state_12	state_12	float
111	18	State Feature 0	state_0	state_0	float
112	18	State Feature 1	state_1	state_1	float
113	18	State Feature 2	state_2	state_2	float
114	18	State Feature 3	state_3	state_3	float
115	18	State Feature 4	state_4	state_4	float
116	18	State Feature 5	state_5	state_5	float
117	18	State Feature 6	state_6	state_6	float
118	18	State Feature 7	state_7	state_7	float
124	20	State Feature 0	state_0	state_0	float
125	20	State Feature 1	state_1	state_1	float
126	20	State Feature 2	state_2	state_2	float
127	20	State Feature 3	state_3	state_3	float
128	20	State Feature 4	state_4	state_4	float
129	20	State Feature 5	state_5	state_5	float
138	22	State Feature 0	state_0	state_0	float
139	22	State Feature 1	state_1	state_1	float
140	22	State Feature 2	state_2	state_2	float
141	22	State Feature 3	state_3	state_3	float
142	22	State Feature 4	state_4	state_4	float
143	22	State Feature 5	state_5	state_5	float
144	22	State Feature 6	state_6	state_6	float
145	22	State Feature 7	state_7	state_7	float
146	22	State Feature 8	state_8	state_8	float
147	22	State Feature 9	state_9	state_9	float
148	22	State Feature 10	state_10	state_10	float
\.


         3532.dat                                                                                            0000600 0004000 0002000 00000660340 14341155237 0014264 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a4d6f64656c56616c75655f362a4d6f64656c56616c75655f372a5375736365707469626c652a556e71756172616e74696e65645f496e6665637465642f284d6f64656c56616c75655f31332a4d6f64656c56616c75655f33202b204d6f64656c56616c75655f31342a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f31352a4d6f64656c56616c75655f3529222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022556e71756172616e74696e65645f496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a556e71756172616e74696e65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022556e71756172616e74696e65645f496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a556e71756172616e74696e65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a556e71756172616e74696e65645f496e6665637465642a284d6f64656c56616c75655f332a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3137202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f3230202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f323329202b204d6f64656c56616c75655f342a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3236202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f323929202b204d6f64656c56616c75655f352a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3332202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f33352929222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022556e71756172616e74696e65645f496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a556e71756172616e74696e65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202251756172616e74696e65645f496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a51756172616e74696e65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a51756172616e74696e65645f496e6665637465642a284d6f64656c56616c75655f38202b204d6f64656c56616c75655f392a2831202d204d6f64656c56616c75655f382929222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202251756172616e74696e65645f496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a51756172616e74696e65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022436f6e6669726d65645f496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936323a436f6e6669726d65645f496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
2	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a7375736365707469626c652a7472616e736d697373696f6e5f726174655f6566666563746976652a2831202d2064656c7461292a2831202d20657073292a28616c7068612a6173796d70746f6d61746963202b2073796d70746f6d61746963292f286173796d70746f6d61746963202b206578706f736564202b207265636f7665726564202b207375736365707469626c65202b2073796d70746f6d6174696329222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a20226173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c207b226e616d65223a20226578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c207b226e616d65223a20227265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a7265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c207b226e616d65223a202273796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a73796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353733227d7d5d2c20227375626a656374223a207b226e616d65223a20227375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a7375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20226578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a6578706f7365642a7369676d612a28312e30202d206e7529222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20226578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a202273796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a73796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353733227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a6578706f7365642a6e752a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20226578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a20226173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a67616d6d615f302a73796d70746f6d61746963222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a73796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353733227d7d2c20226f7574636f6d65223a207b226e616d65223a20227265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a7265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a6173796d70746f6d617469632a67616d6d615f61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20226173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c20226f7574636f6d65223a207b226e616d65223a20227265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a7265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a64657465637465642a67616d6d615f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20226465746563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6465746563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433136323130227d7d2c20226f7574636f6d65223a207b226e616d65223a20227265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a7265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a645f302a73796d70746f6d61746963222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a73796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353733227d7d2c20226f7574636f6d65223a207b226e616d65223a20226465636561736564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a645f442a6465746563746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20226465746563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6465746563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433136323130227d7d2c20226f7574636f6d65223a207b226e616d65223a20226465636561736564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303939313a6465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
3	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a2841696c696e672a67616d6d61202b20446961676e6f7365642a62657461202b20496e6665637465642a616c706861202b205265636f676e697a65642a64656c746129222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022446961676e6f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a446961676e6f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c207b226e616d65223a202241696c696e67222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a41696c696e67227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c207b226e616d65223a20225265636f676e697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5265636f676e697a6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353837227d7d2c207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a496e666563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5375736365707469626c65227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030343638227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a496e666563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a657073696c6f6e222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a496e666563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a2022446961676e6f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a446961676e6f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a7a657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a496e666563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a202241696c696e67222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a41696c696e67227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a58586c616d6264615858222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a496e666563746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a20224865616c6564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a4865616c6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a446961676e6f7365642a657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022446961676e6f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a446961676e6f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f676e697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5265636f676e697a6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a446961676e6f7365642a72686f222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022446961676e6f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a446961676e6f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c20226f7574636f6d65223a207b226e616d65223a20224865616c6564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a4865616c6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a41696c696e672a7468657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202241696c696e67222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a41696c696e67227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f676e697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5265636f676e697a6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a41696c696e672a6b61707061222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202241696c696e67222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a41696c696e67227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a20224865616c6564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a4865616c6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a41696c696e672a6d75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202241696c696e67222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a41696c696e67227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313133373235227d7d2c20226f7574636f6d65223a207b226e616d65223a2022546872656174656e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a546872656174656e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f676e697a65642a6e75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225265636f676e697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5265636f676e697a6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022546872656174656e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a546872656174656e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f676e697a65642a7869222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225265636f676e697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a5265636f676e697a6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353837227d7d2c20226f7574636f6d65223a207b226e616d65223a20224865616c6564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a4865616c6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a546872656174656e65642a746175222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022546872656174656e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a546872656174656e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c20226f7574636f6d65223a207b226e616d65223a2022457874696e6374222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a457874696e6374227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a546872656174656e65642a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022546872656174656e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353733222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a546872656174656e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433135323230227d7d2c20226f7574636f6d65223a207b226e616d65223a20224865616c6564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935353a4865616c6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
4	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a62222c202274797065223a20224e61747572616c50726f64756374696f6e222c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a707369222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574615f312f28312e302a616c7068615f31202b20312e3029202b205375736365707469626c652a626574615f322a28496e6665637465645f4173796d70746f6d61746963202b20496e6665637465645f53796d70746f6d61746963292f28616c7068615f322a28496e6665637465645f4173796d70746f6d61746963202b20496e6665637465645f53796d70746f6d6174696329202b20312e3029222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022506174686f67656e222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a506174686f67656e5f30227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f4173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a4333383333227d7d2c207b226e616d65223a2022496e6665637465645f53796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f53796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235323639227d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a6d75222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6d75222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a64656c74612a6f6d656761222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f53796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f53796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235323639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6f6d6567612a28312e30202d2064656c746129222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f4173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a4333383333227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f53796d70746f6d617469632a286d75202b207369676d6129222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f53796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f53796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235323639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f4173796d70746f6d617469632a286d75202b207369676d6129222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f4173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a4333383333227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f53796d70746f6d617469632a67616d6d615f53222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f53796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f53796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235323639227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f4173796d70746f6d617469632a67616d6d615f41222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f4173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a4333383333227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f76657265642a6d75222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a206e756c6c2c202274797065223a202247726f75706564436f6e74726f6c6c656450726f64756374696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f4173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a4333383333227d7d2c207b226e616d65223a2022496e6665637465645f53796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a496e6665637465645f53796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235323639227d7d5d2c20226f7574636f6d65223a207b226e616d65223a2022506174686f67656e222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a506174686f67656e5f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a6d755f70222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022506174686f67656e222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936343a506174686f67656e5f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
5	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574612f285265636f76657265642a616c706861202b20312e3029222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a496e666563746564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a6b31222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936333a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
6	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a525f66697865642a5375736365707469626c652a67616d6d612f546f74616c5f706f70756c6174696f6e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a496e666563746564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f76657265642a6f6d656761222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937393a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
7	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a284578706f7365642a5375736365707469626c652a626574615f322a725f32202b20496e6665637465642a5375736365707469626c652a626574615f312a725f31292f546f74616c5f506f70756c6174696f6e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022546f74616c5f506f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a546f74616c5f506f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a4578706f736564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a616c706861222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937303a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
8	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574615f6f2a6b2f546f74616c5f706f70756c6174696f6e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6f6d656761222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938343a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
9	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c655f636f6e66696e65642a282d6d5f745f70686173655f312a2831202d20657870282d612a282d7461755f31202b2074696d65292929202d206d5f745f70686173655f322a70202d206d5f745f70686173655f332a28622a282d7461755f33202b2074696d6529202b207029202b20312e3029222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f63227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353439227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f756e636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f75227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f756e636f6e66696e65642a286d5f745f70686173655f312a2831202d20657870282d612a282d7461755f31202b2074696d65292929202b206d5f745f70686173655f322a70202b206d5f745f70686173655f332a28622a282d7461755f33202b2074696d6529202b20702929222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f756e636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f75227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f63227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353439227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f756e636f6e66696e65642a626574612a28312e30202d207369676d61292a28496e6665637465645f7265706f727465642a6e202b20496e6665637465645f756e7265706f7274656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f7265706f72746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f72227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f756e7265706f72746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f75227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433433323334227d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f756e636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f75227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a45227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f756e636f6e66696e65642a626574612a7369676d612a28496e6665637465645f7265706f727465642a6e202b20496e6665637465645f756e7265706f7274656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f7265706f72746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f72227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f756e7265706f72746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f75227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433433323334227d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f756e636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f75227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a51227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a51756172616e74696e65642a58586c616d62646158582a7468657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a51227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f7265706f72746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f72227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a662a6d75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a45227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f7265706f72746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f72227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6d752a28312e30202d206629222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a45227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f756e7265706f72746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f75227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433433323334227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f7265706f727465642a6574615f72222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f7265706f72746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f72227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a52227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f756e7265706f727465642a6574615f75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f756e7265706f72746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a495f75227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433433323334227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a52227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a58586c616d62646158582a74686574612a28312e30202d2051756172616e74696e656429222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a51227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f756e636f6e66696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938333a535f75227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
10	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a657073696c6f6e5f732a72686f5f732a28312e30202d20626574615f73292f284173796d70746f6d61746963202b20496e666563746564202b20496e6665637465645f71756172616e74696e6564202b205265636f7665726564202b205375736365707469626c65202b205375736365707469626c655f71756172616e74696e656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a78695f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f71756172616e74696e65642a6d5f73222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f71756172616e74696e65642a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574615f732a657073696c6f6e5f732a28312e30202d2072686f5f73292f284173796d70746f6d61746963202b20496e666563746564202b20496e6665637465645f71756172616e74696e6564202b205265636f7665726564202b205375736365707469626c65202b205375736365707469626c655f71756172616e74696e656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574615f732a657073696c6f6e5f732a72686f5f732f284173796d70746f6d61746963202b20496e666563746564202b20496e6665637465645f71756172616e74696e6564202b205265636f7665726564202b205375736365707469626c65202b205375736365707469626c655f71756172616e74696e656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a67616d6d615f61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a78695f61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d615f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f71756172616e74696e65642a78695f71222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f71756172616e74696e65642a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f76657265642a64656c7461222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937373a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
11	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a616c7068612a7461752a28496e6665637465645f7374726f6e675f696d6d756e655f73797374656d202b20496e6665637465645f7765616b5f696d6d756e655f73797374656d29222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f7765616b5f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7765616b5f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f7374726f6e675f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7374726f6e675f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f7374726f6e675f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7374726f6e675f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a7461752a28312e30202d20616c706861292a28496e6665637465645f7374726f6e675f696d6d756e655f73797374656d202b20496e6665637465645f7765616b5f696d6d756e655f73797374656d29222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f7374726f6e675f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7374726f6e675f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f7765616b5f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7765616b5f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f7765616b5f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7765616b5f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f7374726f6e675f696d6d756e655f73797374656d2a67616d6d615f31222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f7374726f6e675f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7374726f6e675f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f7765616b5f696d6d756e655f73797374656d2a67616d6d615f32222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f7765616b5f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7765616b5f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f7765616b5f696d6d756e655f73797374656d2a6d75222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f7765616b5f696d6d756e655f73797374656d222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937363a496e6665637465645f7765616b5f696d6d756e655f73797374656d227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
12	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574615f302a28302e343337342a547269676765725f53746167655f31202b20302e333931342a547269676765725f53746167655f32202b20302e343034372a547269676765725f53746167655f33292a282d302e303738342a547269676765725f53746167655f31202d20302e3034352a547269676765725f53746167655f32202d20302e303436362a547269676765725f53746167655f33202b2031292a2a74696d652f28496e666563746564202b2052656d6f766564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202252656d6f766564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a52656d6f766564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a28302e3032352a547269676765725f53746167655f31202b20302e3034322a547269676765725f53746167655f32202b20302e30352a547269676765725f53746167655f3329222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202252656d6f766564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938323a52656d6f766564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
13	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574612a632a28312e30202d2071292a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a632a712a28312e30202d2062657461292a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b226e636974223a2022433731393032222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f71756172616e74696e65642a58586c616d6264615858222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b226e636974223a2022433731393032222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a72686f2a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7369676d612a28312e30202d2072686f29222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a64656c74615f49222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d615f49222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a67616d6d615f41222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a67616d6d615f48222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a616c706861222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a616c706861222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574612a632a712a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f7365645f71756172616e74696e6564222c20226964656e74696669657273223a207b226e636974223a2022433731393032222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365645f71756172616e74696e65642a64656c74615f71222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f7365645f71756172616e74696e6564222c20226964656e74696669657273223a207b226e636974223a2022433731393032222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
14	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574612a28312e30202d20657073696c6f6e292f4e222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353937222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353937222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937383a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
15	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a62657461222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a6d75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a72686f222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022436f6e6669726d6564222c20226964656e74696669657273223a207b226e636974223a2022433135323230222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935373a436f6e6669726d6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
16	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f616972706f7274732a5375736365707469626c655f436f756e746965735f776974685f616972706f7274732a58586c616d62646158585f436f756e746965735f776974685f616972706f7274732a657073696c6f6e2f284d657461626f6c6974655f30202b204d657461626f6c6974655f31202b204d657461626f6c6974655f32202b204d657461626f6c6974655f33202b204d657461626f6c6974655f34202b204d657461626f6c6974655f35202b204d657461626f6c6974655f3629222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5375736365707469626c655f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f616972706f7274732a6574615f436f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f616972706f7274732a707369222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f616972706f7274732a64656c7461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f76657265645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5265636f76657265645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f776974685f616972706f7274732a6f6d6567615f436f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224943555f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f776974685f616972706f7274732a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022446973636861726765645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313534343735222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a446973636861726765645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f776974685f616972706f7274732a7869222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f776974685f616972706f7274732a6d755f436f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a20225375736365707469626c655f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a28496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a58586c616d62646158585f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a657073696c6f6e2f284d657461626f6c6974655f3130202b204d657461626f6c6974655f3131202b204d657461626f6c6974655f3132202b204d657461626f6c6974655f3133202b204d657461626f6c6974655f37202b204d657461626f6c6974655f38202b204d657461626f6c6974655f3929202b20496e6665637465645f436f756e746965735f776974685f616972706f7274732a7068692f284d657461626f6c6974655f30202b204d657461626f6c6974655f31202b204d657461626f6c6974655f32202b204d657461626f6c6974655f33202b204d657461626f6c6974655f34202b204d657461626f6c6974655f35202b204d657461626f6c6974655f362929222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5375736365707469626c655f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a6574615f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a707369222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a64656c7461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f76657265645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5265636f76657265645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a6f6d6567615f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022446973636861726765645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313534343735222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a446973636861726765645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a7869222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a6d755f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a20225375736365707469626c655f436f756e746965735f776974685f68696768776179732a28496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a7461752f284d657461626f6c6974655f3130202b204d657461626f6c6974655f3131202b204d657461626f6c6974655f3132202b204d657461626f6c6974655f3133202b204d657461626f6c6974655f37202b204d657461626f6c6974655f38202b204d657461626f6c6974655f3929202b20496e6665637465645f436f756e746965735f776974685f68696768776179732a58586c616d62646158585f436f756e746965735f776974685f68696768776179732a657073696c6f6e2f284d657461626f6c6974655f3134202b204d657461626f6c6974655f3135202b204d657461626f6c6974655f3136202b204d657461626f6c6974655f3137202b204d657461626f6c6974655f3138202b204d657461626f6c6974655f3139202b204d657461626f6c6974655f32302929222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5375736365707469626c655f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f68696768776179732a6574615f436f756e746965735f776974685f6869676877617973222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f68696768776179732a707369222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f436f756e746965735f776974685f68696768776179732a64656c7461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f76657265645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5265636f76657265645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f776974685f68696768776179732a6f6d6567615f436f756e746965735f776974685f6869676877617973222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224943555f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f436f756e746965735f776974685f68696768776179732a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022446973636861726765645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a202243313534343735222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a446973636861726765645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f776974685f68696768776179732a7869222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f436f756e746965735f776974685f68696768776179732a6d755f436f756e746965735f776974685f6869676877617973222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a20225375736365707469626c655f4c6f775f7269736b5f636f756e746965732a28496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f7274732a67616d6d612f284d657461626f6c6974655f3130202b204d657461626f6c6974655f3131202b204d657461626f6c6974655f3132202b204d657461626f6c6974655f3133202b204d657461626f6c6974655f37202b204d657461626f6c6974655f38202b204d657461626f6c6974655f3929202b20496e6665637465645f436f756e746965735f776974685f68696768776179732a616c7068612f284d657461626f6c6974655f3134202b204d657461626f6c6974655f3135202b204d657461626f6c6974655f3136202b204d657461626f6c6974655f3137202b204d657461626f6c6974655f3138202b204d657461626f6c6974655f3139202b204d657461626f6c6974655f323029202b20496e6665637465645f4c6f775f7269736b5f636f756e746965732a58586c616d62646158585f4c6f775f7269736b5f636f756e746965732a657073696c6f6e2f284d657461626f6c6974655f3231202b204d657461626f6c6974655f3232202b204d657461626f6c6974655f3233202b204d657461626f6c6974655f3234202b204d657461626f6c6974655f3235202b204d657461626f6c6974655f3236202b204d657461626f6c6974655f32372929222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f6e65696768626f7572696e675f636f756e746965735f776974685f616972706f727473227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f436f756e746965735f776974685f6869676877617973222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f436f756e746965735f776974685f6869676877617973227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e6665637465645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5375736365707469626c655f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e6665637465645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f4c6f775f7269736b5f636f756e746965732a6574615f4c6f775f7269736b5f636f756e74696573222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f4c6f775f7269736b5f636f756e746965732a707369222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465645f4c6f775f7269736b5f636f756e746965732a64656c7461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e6665637465645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a496e6665637465645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f76657265645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a5265636f76657265645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f4c6f775f7269736b5f636f756e746965732a6f6d6567615f4c6f775f7269736b5f636f756e74696573222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224943555f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365645f4c6f775f7269736b5f636f756e746965732a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022446973636861726765645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a202243313534343735222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a446973636861726765645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f4c6f775f7269736b5f636f756e746965732a7869222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a486f73706974616c697365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4943555f4c6f775f7269736b5f636f756e746965732a6d755f4c6f775f7269736b5f636f756e74696573222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224943555f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433533353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a4943555f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202244656365617365645f4c6f775f7269736b5f636f756e74696573222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936393a44656365617365645f4c6f775f7269736b5f636f756e74696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
17	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a284d6f64656c56616c75655f322a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f362a4d6f64656c56616c75655f39292a284d6f64656c56616c75655f352a526f5f4341202b204d6f64656c56616c75655f362a526f5f4e5929222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935363a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935363a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935363a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a284d6f64656c56616c75655f322a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f362a4d6f64656c56616c75655f3929222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935363a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935363a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
18	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a284173796d70746f6d617469632a284d6f64656c56616c75655f302a6c5f615f315f4368696e61202b204d6f64656c56616c75655f312a6c5f615f315f4974616c79202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3634202b204d6f64656c56616c75655f332a6c5f615f315f4672616e6365202b204d6f64656c56616c75655f342a6c5f615f315f4765726d616e79202b204d6f64656c56616c75655f352a6c5f615f315f55534129202b20486f73706974616c697a65642a284d6f64656c56616c75655f302a6c5f315f4368696e61202b204d6f64656c56616c75655f312a6c5f315f4974616c79202b204d6f64656c56616c75655f322a6c5f315f537061696e202b204d6f64656c56616c75655f332a6c5f315f4672616e6365202b204d6f64656c56616c75655f342a6c5f315f4765726d616e79202b204d6f64656c56616c75655f352a6c5f315f55534129202b20496e66656374696f7573292a284d6f64656c56616c75655f302a626574615f315f4368696e61202b204d6f64656c56616c75655f312a626574615f315f4974616c79202b204d6f64656c56616c75655f322a626574615f315f537061696e202b204d6f64656c56616c75655f332a626574615f315f4672616e6365202b204d6f64656c56616c75655f342a626574615f315f4765726d616e79202b204d6f64656c56616c75655f352a626574615f315f555341292f284d6f64656c56616c75655f302a4d6f64656c56616c75655f313330202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f313331202b204d6f64656c56616c75655f3133322a4d6f64656c56616c75655f32202b204d6f64656c56616c75655f3133332a4d6f64656c56616c75655f33202b204d6f64656c56616c75655f3133342a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3133352a4d6f64656c56616c75655f3529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022486f73706974616c697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a486f73706974616c697a6564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a4d6f64656c56616c75655f31322a4d6f64656c56616c75655f3133222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a4d6f64656c56616c75655f31322a2831202d204d6f64656c56616c75655f313329222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3330202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f3532202b204d6f64656c56616c75655f3130322a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3131392a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3638202b204d6f64656c56616c75655f332a4d6f64656c56616c75655f383529222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a486f73706974616c697a6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3239202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f3533202b204d6f64656c56616c75655f3130332a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3132302a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3639202b204d6f64656c56616c75655f332a4d6f64656c56616c75655f383629222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3431202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f3537202b204d6f64656c56616c75655f3130382a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3132352a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3734202b204d6f64656c56616c75655f332a4d6f64656c56616c75655f393129222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224465636561736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a4d6f64656c56616c75655f31372a2831202d204d6f64656c56616c75655f313829222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a4d6f64656c56616c75655f31372a4d6f64656c56616c75655f3138222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224465636561736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697a65642a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3430202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f3536202b204d6f64656c56616c75655f3130372a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3132342a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3733202b204d6f64656c56616c75655f332a4d6f64656c56616c75655f393029222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a486f73706974616c697a6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224465636561736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a4465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697a65642a284d6f64656c56616c75655f302a4d6f64656c56616c75655f3238202b204d6f64656c56616c75655f312a4d6f64656c56616c75655f313238202b204d6f64656c56616c75655f3130342a4d6f64656c56616c75655f34202b204d6f64656c56616c75655f3132312a4d6f64656c56616c75655f35202b204d6f64656c56616c75655f322a4d6f64656c56616c75655f3730202b204d6f64656c56616c75655f332a4d6f64656c56616c75655f383729222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c697a6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a486f73706974616c697a6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303936303a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
19	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a486f73706974616c697365642a5375736365707469626c652a626574612a6c2f4e202b20312e302a496e66656374696f75732a5375736365707469626c652a626574612f4e202b20312e302a53757065725f7370726561646572732a5375736365707469626c652a626574615f7072696d652f4e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a486f73706974616c69736564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202253757065725f737072656164657273222c20226964656e74696669657273223a207b2269646f223a202230303030343633222c20226e636974223a2022433439353038222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a53757065725f737072656164657273227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6b617070612a282d72686f31202d2072686f32202b20312e3029222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6b617070612a72686f32222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202253757065725f737072656164657273222c20226964656e74696669657273223a207b2269646f223a202230303030343633222c20226e636974223a2022433439353038222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a53757065725f737072656164657273227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a6b617070612a72686f31222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202269646f223a202230303030353937222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a4578706f736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a53757065725f7370726561646572732a64656c74615f70222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202253757065725f737072656164657273222c20226964656e74696669657273223a207b2269646f223a202230303030343633222c20226e636974223a2022433439353038222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a53757065725f737072656164657273227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022466174616c6974696573222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a466174616c6974696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a53757065725f7370726561646572732a67616d6d615f61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202253757065725f737072656164657273222c20226964656e74696669657273223a207b2269646f223a202230303030343633222c20226e636974223a2022433439353038222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a53757065725f737072656164657273227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a486f73706974616c69736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a53757065725f7370726561646572732a67616d6d615f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202253757065725f737072656164657273222c20226964656e74696669657273223a207b2269646f223a202230303030343633222c20226e636974223a2022433439353038222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a53757065725f737072656164657273227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a64656c74615f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022466174616c6974696573222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a466174616c6974696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a67616d6d615f61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a486f73706974616c69736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e66656374696f75732a67616d6d615f69222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e66656374696f7573222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731353439222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a496e66656374696f7573227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a67616d6d615f72222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a486f73706974616c69736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a64656c74615f68222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b226e636974223a2022433235313739222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a486f73706974616c69736564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022466174616c6974696573222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303935383a466174616c6974696573227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
20	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a525f66697865642a5375736365707469626c652a67616d6d612f546f74616c5f706f70756c6174696f6e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a496e666563746564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5265636f76657265642a6f6d656761222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938303a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
21	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a496e6665637465642a5375736365707469626c652a626574612f546f74616c5f706f70756c6174696f6e222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a657073696c6f6e222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a616c706861222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224465636561736564222c20226964656e74696669657273223a207b226e636974223a202243313638393730222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937343a4465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
22	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574612a28312e30202d2071292a28635f62202b2028635f30202d20635f62292a657870282d725f312a74696d6529292a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a712a28312e30202d2062657461292a28635f62202b2028635f30202d20635f62292a657870282d725f312a74696d6529292a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f71756172616e74696e65642a58586c616d6264615858222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c655f71756172616e74696e6564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a72686f2a7369676d61222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7369676d612a28312e30202d2072686f29222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a64656c74615f495f302a64656c74615f495f662f2864656c74615f495f30202b20282d64656c74615f495f30202b2064656c74615f495f66292a657870282d725f322a74696d652929222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d615f49222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a67616d6d615f41222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a67616d6d615f48222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5265636f7665726564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a616c706861222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a616c706861222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574612a712a28635f62202b2028635f30202d20635f62292a657870282d725f312a74696d6529292a284173796d70746f6d617469632a7468657461202b20496e66656374656429222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353639222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f7365645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365645f71756172616e74696e65642a64656c74615f71222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f7365645f71756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a2022433731393032222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a4578706f7365645f71756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303937323a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
23	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a5375736365707469626c652a626574612a635f302a71312a284173796d70746f6d617469632a7869202b20496e666563746564292a657870282d546f74616c5f7265706f727465645f63617365732a64656c7461292f284173796d70746f6d61746963202b204578706f736564202b20496e666563746564202b205265636f7665726564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a2022546f74616c5f7265706f727465645f6361736573222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f7265706f727465645f6361736573227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c652a71332a28496e6665637465642a7132202b2051756172616e74696e65642a657461292f284173796d70746f6d61746963202b204578706f736564202b20496e666563746564202b205265636f7665726564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c655f69736f6c61746564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c655f69736f6c61746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353439227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a5375736365707469626c655f69736f6c617465642a6d75222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20225375736365707469626c655f69736f6c61746564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c655f69736f6c61746564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235353439227d7d2c20226f7574636f6d65223a207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7068692a7468657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a7068692a28312e30202d20746865746129222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4578706f7365642a71332a28496e6665637465642a7132202b2051756172616e74696e65642a657461292f284173796d70746f6d61746963202b204578706f736564202b20496e666563746564202b205265636f7665726564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c20226f7574636f6d65223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a7132222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a64222c202274797065223a20224e61747572616c4465677261646174696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a67616d6d615f49222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a496e6665637465642a71332a28496e6665637465642a7132202b2051756172616e74696e65642a657461292f284173796d70746f6d61746963202b204578706f736564202b20496e666563746564202b205265636f7665726564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a67616d6d615f41222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4173796d70746f6d617469632a71332a28496e6665637465642a7132202b2051756172616e74696e65642a657461292f284173796d70746f6d61746963202b204578706f736564202b20496e666563746564202b205265636f7665726564202b205375736365707469626c6529222c202274797065223a202247726f75706564436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c657273223a205b7b226e616d65223a2022496e666563746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a496e666563746564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c207b226e616d65223a2022546f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a546f74616c5f706f70756c6174696f6e227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20224578706f736564222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4578706f736564227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353937227d7d2c207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c207b226e616d65223a20225375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5375736365707469626c65227d2c2022636f6e74657874223a207b7d7d5d2c20227375626a656374223a207b226e616d65223a20224173796d70746f6d61746963222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4173796d70746f6d61746963227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030353639227d7d2c20226f7574636f6d65223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a51756172616e74696e65642a657461222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202251756172616e74696e6564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a51756172616e74696e6564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433731393032227d7d2c20226f7574636f6d65223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a64222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a20224465636561736564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a4465636561736564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a486f73706974616c697365642a67616d6d615f48222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022486f73706974616c69736564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a486f73706974616c69736564227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a20225265636f7665726564222c20226964656e74696669657273223a207b2269646f223a202230303030363231222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938313a5265636f7665726564227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
24	2022-11-28 15:41:02.997833	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022312e302a756e696e6665637465645f6e6f6e7465737465642a2831202d2065706964656d69635f657874696e677569736865645f626f6f6c292a28496e66656374696f6e5f66726f6d5f6e6f6e5f7465737465645f6e6f5f73796d70746f6d735f302a696e6665637465645f6e6f6e746573746564202b20496e66656374696f6e5f66726f6d5f6e6f6e5f7465737465645f73796d70746f6d732a73796d70746f6d735f6e6f6e746573746564202b20496e66656374696f6e5f66726f6d5f7465737465645f6e6f5f73796d70746f6d735f302a696e6665637465645f746573746564202b20496e66656374696f6e5f66726f6d5f7465737465645f73796d70746f6d732a73796d70746f6d735f746573746564292f536f6369616c5f44697374616e6365222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022756e696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a54657374696e675f52616e646f6d652a756e696e6665637465645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022756e696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022756e696e6665637465645f746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a756e696e6665637465645f7465737465642a2831202d2065706964656d69635f657874696e677569736865645f626f6f6c292a28496e66656374696f6e5f66726f6d5f6e6f6e5f7465737465645f6e6f5f73796d70746f6d735f302a696e6665637465645f6e6f6e746573746564202b20496e66656374696f6e5f66726f6d5f6e6f6e5f7465737465645f73796d70746f6d732a73796d70746f6d735f6e6f6e746573746564202b20496e66656374696f6e5f66726f6d5f7465737465645f6e6f5f73796d70746f6d735f302a696e6665637465645f746573746564202b20496e66656374696f6e5f66726f6d5f7465737465645f73796d70746f6d732a73796d70746f6d735f746573746564292f536f6369616c5f44697374616e6365222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022756e696e6665637465645f746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a2022696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a54657374696e675f52616e646f6d652a696e6665637465645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022696e6665637465645f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a53796d70746f6d735f6170706561722a696e6665637465645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a202273796d70746f6d735f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a53796d70746f6d735f6170706561722a696e6665637465645f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022696e6665637465645f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a202273796d70746f6d735f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a54657374696e675f666f725f53796d70746f6d732a73796d70746f6d735f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d735f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a202273796d70746f6d735f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f64656174685f726174655f636f6e7374616e742a73796d70746f6d735f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d735f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f636f726f6e615f746573746564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f636f726f6e615f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f7265636f7665722a73796d70746f6d735f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d735f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a20227265636f76657265645f746573746564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a7265636f76657265645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f7265636f7665722a73796d70746f6d735f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d735f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a20227265636f76657265645f6e6f6e746573746564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a7265636f76657265645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a42697274685f726174652a7375736365707469626c652a746f74616c5f706f70756c6174696f6e222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a2022746f74616c5f706f70756c6174696f6e222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a746f74616c5f706f70756c6174696f6e5f30227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a20227375736365707469626c65222c20226964656e74696669657273223a207b2269646f223a202230303030353134222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a7375736365707469626c655f30227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022756e696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4e6f726d616c5f64656174685f726174655f636f6e7374616e745f302a756e696e6665637465645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022756e696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f6e6f6e636f726f6e61222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f6e6f6e636f726f6e615f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4e6f726d616c5f64656174685f726174655f636f6e7374616e745f302a7265636f76657265645f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20227265636f76657265645f746573746564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a7265636f76657265645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a202269646f3a30303030363231227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f6e6f6e636f726f6e61222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f6e6f6e636f726f6e615f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4e6f726d616c5f64656174685f726174655f636f6e7374616e745f302a7265636f76657265645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a20227265636f76657265645f6e6f6e746573746564222c20226964656e74696669657273223a207b2262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a7265636f76657265645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f6e6f6e636f726f6e61222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f6e6f6e636f726f6e615f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f64656174685f726174655f636f6e7374616e742a696e6665637465645f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022696e6665637465645f746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f636f726f6e615f746573746564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f636f726f6e615f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f64656174685f726174655f636f6e7374616e742a696e6665637465645f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022696e6665637465645f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a696e6665637465645f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f636f726f6e615f6e6f6e746573746564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f636f726f6e615f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a4e6f726d616c5f64656174685f726174655f636f6e7374616e745f302a756e696e6665637465645f746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022756e696e6665637465645f746573746564222c20226964656e74696669657273223a207b2265666f223a202230303031343630222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a756e696e6665637465645f7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a433437383931227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f6e6f6e636f726f6e61222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f6e6f6e636f726f6e615f30227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022312e302a436f726f6e615f64656174685f726174655f636f6e7374616e742a73796d70746f6d735f6e6f6e746573746564222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202273796d70746f6d735f6e6f6e746573746564222c20226964656e74696669657273223a207b2269646f223a202230303030353131222c20226e636974223a202243313731313333222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a73796d70746f6d735f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c20226f7574636f6d65223a207b226e616d65223a2022646561645f636f726f6e615f6e6f6e746573746564222c20226964656e74696669657273223a207b226e636974223a2022433238353534222c202262696f6d6f64656c732e73706563696573223a202242494f4d44303030303030303938383a646561645f636f726f6e615f6e6f6e7465737465645f30227d2c2022636f6e74657874223a207b2270726f7065727479223a20226e6369743a43313031383837227d7d2c202270726f76656e616e6365223a205b5d7d5d7d
\.


                                                                                                                                                                                                                                                                                                3548.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3530.dat                                                                                            0000600 0004000 0002000 00000000047 14341155237 0014252 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        Petri Net	0.0.1	semantics_go_here
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         3564.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014253 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3544.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014251 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3540.dat                                                                                            0000600 0004000 0002000 00000003226 14341155237 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	vo:0004281	publications	1	obj
2	vo:0004281	intermediates	1	obj
3	vo:0004281	publications	2	obj
4	vo:0004281	intermediates	2	obj
5	doid:0080600	publications	3	obj
6	doid:0080600	intermediates	3	obj
7	doid:0080600	publications	4	obj
8	doid:0080600	intermediates	4	obj
9	vo:0004281	publications	5	obj
10	vo:0004281	intermediates	5	obj
11	doid:0080600	publications	6	obj
12	doid:0080600	intermediates	6	obj
13	doid:0080600	publications	7	obj
14	doid:0080600	intermediates	7	obj
15	vo:0004281	publications	8	obj
16	vo:0004281	intermediates	8	obj
17	vo:0004281	publications	9	obj
18	vo:0004281	intermediates	9	obj
19	vo:0004281	publications	10	obj
20	vo:0004281	intermediates	10	obj
21	doid:0080600	publications	11	obj
22	doid:0080600	intermediates	11	obj
23	vo:0004281	publications	12	obj
24	vo:0004281	intermediates	12	obj
25	vo:0004281	publications	13	obj
26	vo:0004281	intermediates	13	obj
27	vo:0004281	publications	14	obj
28	vo:0004281	intermediates	14	obj
29	doid:0080600	publications	15	obj
30	doid:0080600	intermediates	15	obj
31	vo:0004281	publications	16	obj
32	vo:0004281	intermediates	16	obj
33	doid:0080600	publications	17	obj
34	doid:0080600	intermediates	17	obj
35	doid:0080600	publications	18	obj
36	doid:0080600	intermediates	18	obj
37	doid:0080600	publications	19	obj
38	doid:0080600	intermediates	19	obj
39	doid:0080600	publications	20	obj
40	doid:0080600	intermediates	20	obj
41	doid:0080600	publications	21	obj
42	doid:0080600	intermediates	21	obj
43	vo:0004281	publications	22	obj
44	vo:0004281	intermediates	22	obj
45	doid:0080600	publications	23	obj
46	doid:0080600	intermediates	23	obj
47	doid:0080600	publications	24	obj
48	doid:0080600	intermediates	24	obj
\.


                                                                                                                                                                                                                                                                                                                                                                          3542.dat                                                                                            0000600 0004000 0002000 00000000054 14341155237 0014253 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	Adam Smith	Adam@test.io	Uncharted		t
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    3538.dat                                                                                            0000600 0004000 0002000 00000000104 14341155237 0014254 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	My Project	First project in TDS	2022-11-28 15:41:02.999537	t
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                            3552.dat                                                                                            0000600 0004000 0002000 00000003105 14341155237 0014254 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	1	publications	\N
2	1	1	intermediates	\N
3	1	2	publications	\N
4	1	2	intermediates	\N
5	1	3	publications	\N
6	1	3	intermediates	\N
7	1	4	publications	\N
8	1	4	intermediates	\N
9	1	5	publications	\N
10	1	5	intermediates	\N
11	1	6	publications	\N
12	1	6	intermediates	\N
13	1	7	publications	\N
14	1	7	intermediates	\N
15	1	8	publications	\N
16	1	8	intermediates	\N
17	1	9	publications	\N
18	1	9	intermediates	\N
19	1	10	publications	\N
20	1	10	intermediates	\N
21	1	11	publications	\N
22	1	11	intermediates	\N
23	1	12	publications	\N
24	1	12	intermediates	\N
25	1	13	publications	\N
26	1	13	intermediates	\N
27	1	14	publications	\N
28	1	14	intermediates	\N
29	1	15	publications	\N
30	1	15	intermediates	\N
31	1	16	publications	\N
32	1	16	intermediates	\N
33	1	17	publications	\N
34	1	17	intermediates	\N
35	1	18	publications	\N
36	1	18	intermediates	\N
37	1	19	publications	\N
38	1	19	intermediates	\N
39	1	20	publications	\N
40	1	20	intermediates	\N
41	1	21	publications	\N
42	1	21	intermediates	\N
43	1	22	publications	\N
44	1	22	intermediates	\N
45	1	23	publications	\N
46	1	23	intermediates	\N
47	1	24	publications	\N
48	1	24	intermediates	\N
49	1	1	datasets	\N
50	1	2	datasets	\N
51	1	3	datasets	\N
52	1	4	datasets	\N
53	1	5	datasets	\N
54	1	6	datasets	\N
55	1	7	datasets	\N
56	1	8	datasets	\N
57	1	9	datasets	\N
58	1	10	datasets	\N
59	1	11	datasets	\N
60	1	12	datasets	\N
61	1	13	datasets	\N
62	1	14	datasets	\N
63	1	15	datasets	\N
64	1	16	datasets	\N
65	1	17	datasets	\N
66	1	18	datasets	\N
67	1	19	datasets	\N
68	1	20	datasets	\N
69	1	21	datasets	\N
70	1	22	datasets	\N
71	1	23	datasets	\N
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                           3554.dat                                                                                            0000600 0004000 0002000 00000003442 14341155237 0014262 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	2022-11-28 15:41:02.995402	derivedfrom	1	intermediates	1	publications	1
2	2022-11-28 15:41:02.995402	derivedfrom	2	intermediates	2	publications	1
3	2022-11-28 15:41:02.995402	derivedfrom	3	intermediates	3	publications	1
4	2022-11-28 15:41:02.995402	derivedfrom	4	intermediates	4	publications	1
5	2022-11-28 15:41:02.995402	derivedfrom	5	intermediates	5	publications	1
6	2022-11-28 15:41:02.995402	derivedfrom	6	intermediates	6	publications	1
7	2022-11-28 15:41:02.995402	derivedfrom	7	intermediates	7	publications	1
8	2022-11-28 15:41:02.995402	derivedfrom	8	intermediates	8	publications	1
9	2022-11-28 15:41:02.995402	derivedfrom	9	intermediates	9	publications	1
10	2022-11-28 15:41:02.995402	derivedfrom	10	intermediates	10	publications	1
11	2022-11-28 15:41:02.995402	derivedfrom	11	intermediates	11	publications	1
12	2022-11-28 15:41:02.995402	derivedfrom	12	intermediates	12	publications	1
13	2022-11-28 15:41:02.995402	derivedfrom	13	intermediates	13	publications	1
14	2022-11-28 15:41:02.995402	derivedfrom	14	intermediates	14	publications	1
15	2022-11-28 15:41:02.995402	derivedfrom	15	intermediates	15	publications	1
16	2022-11-28 15:41:02.995402	derivedfrom	16	intermediates	16	publications	1
17	2022-11-28 15:41:02.995402	derivedfrom	17	intermediates	17	publications	1
18	2022-11-28 15:41:02.995402	derivedfrom	18	intermediates	18	publications	1
19	2022-11-28 15:41:02.995402	derivedfrom	19	intermediates	19	publications	1
20	2022-11-28 15:41:02.995402	derivedfrom	20	intermediates	20	publications	1
21	2022-11-28 15:41:02.995402	derivedfrom	21	intermediates	21	publications	1
22	2022-11-28 15:41:02.995402	derivedfrom	22	intermediates	22	publications	1
23	2022-11-28 15:41:02.995402	derivedfrom	23	intermediates	23	publications	1
24	2022-11-28 15:41:02.995402	derivedfrom	24	intermediates	24	publications	1
\.


                                                                                                                                                                                                                              3536.dat                                                                                            0000600 0004000 0002000 00000001234 14341155237 0014257 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	5ef392dca58f1dfd5209e2a9
2	5ef119afa58f1dfd5209bd33
3	616cf16267467f7269ccde6f
4	616efe6e67467f7269d640b2
5	5ef6202ca58f1dfd520c9ca2
6	5f6bc344a58f1dfd52164df2
7	5e949b4d998e17af826aadd4
8	5e75c322998e17af82656a5b
9	633c807dac235e971b159f20
10	5f0330e9a58f1dfd520fa5fe
11	5f6d1039a58f1dfd521b51ee
12	633c807cac235e971b159f0e
13	633c807cac235e971b159f08
14	5f6d0d79a58f1dfd5216f1a0
15	5e86d13d998e17af826a2572
16	5f6d0dbaa58f1dfd52179fbc
17	633c807cac235e971b159f01
18	633c807cac235e971b159f18
19	5ef61f90a58f1dfd520b5a8c
20	5f6bc344a58f1dfd52164df2
21	5f6d0e20a58f1dfd52184931
22	5e7ba3ed998e17af8267ba70
23	5f6d0dada58f1dfd521773d1
24	616cf3b667467f7269cce791
\.


                                                                                                                                                                                                                                                                                                                                                                    3560.dat                                                                                            0000600 0004000 0002000 00000002451 14341155237 0014256 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	Timestep feature qualifier	timestep_qualifier	float
2	2	Timestep feature qualifier	timestep_qualifier	float
3	3	Timestep feature qualifier	timestep_qualifier	float
4	4	Timestep feature qualifier	timestep_qualifier	float
5	5	Timestep feature qualifier	timestep_qualifier	float
6	6	Timestep feature qualifier	timestep_qualifier	float
7	7	Timestep feature qualifier	timestep_qualifier	float
8	8	Timestep feature qualifier	timestep_qualifier	float
9	9	Timestep feature qualifier	timestep_qualifier	float
10	10	Timestep feature qualifier	timestep_qualifier	float
11	11	Timestep feature qualifier	timestep_qualifier	float
12	12	Timestep feature qualifier	timestep_qualifier	float
13	13	Timestep feature qualifier	timestep_qualifier	float
14	14	Timestep feature qualifier	timestep_qualifier	float
15	15	Timestep feature qualifier	timestep_qualifier	float
16	16	Timestep feature qualifier	timestep_qualifier	float
17	17	Timestep feature qualifier	timestep_qualifier	float
18	18	Timestep feature qualifier	timestep_qualifier	float
19	19	Timestep feature qualifier	timestep_qualifier	float
20	20	Timestep feature qualifier	timestep_qualifier	float
21	21	Timestep feature qualifier	timestep_qualifier	float
22	22	Timestep feature qualifier	timestep_qualifier	float
23	23	Timestep feature qualifier	timestep_qualifier	float
\.


                                                                                                                                                                                                                       3566.dat                                                                                            0000600 0004000 0002000 00000002747 14341155237 0014274 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	1
2	1	2
3	1	3
4	1	4
5	2	5
6	2	6
7	2	7
8	2	8
9	2	9
10	2	10
11	2	11
12	3	12
13	3	13
14	3	14
15	3	15
16	3	16
17	3	17
18	3	18
19	3	19
20	4	20
21	4	21
22	4	22
23	4	23
24	4	24
25	4	25
26	5	26
27	5	27
28	5	28
29	6	29
30	6	30
31	6	31
32	6	32
33	6	33
34	7	34
35	7	35
36	7	36
37	7	37
38	7	38
39	8	39
40	8	40
41	8	41
42	8	42
43	8	43
44	9	44
45	9	45
46	9	46
47	9	47
48	9	48
49	9	49
50	10	50
51	10	51
52	10	52
53	10	53
54	11	54
55	11	55
56	11	56
57	12	57
58	12	58
59	12	59
60	12	60
61	12	61
62	12	62
63	12	63
64	12	64
65	13	65
66	13	66
67	13	67
68	13	68
69	14	69
70	14	70
71	14	71
72	14	72
73	15	73
74	15	74
75	15	75
76	15	76
77	15	77
78	15	78
79	15	79
80	15	80
81	15	81
82	15	82
83	15	83
84	15	84
85	15	85
86	15	86
87	15	87
88	15	88
89	15	89
90	15	90
91	15	91
92	15	92
93	15	93
94	15	94
95	15	95
96	15	96
97	15	97
98	15	98
99	15	99
100	15	100
101	16	101
102	16	102
103	16	103
104	17	104
105	17	105
106	17	106
107	17	107
108	17	108
109	17	109
110	17	110
111	18	111
112	18	112
113	18	113
114	18	114
115	18	115
116	18	116
117	18	117
118	18	118
119	19	119
120	19	120
121	19	121
122	19	122
123	19	123
124	20	124
125	20	125
126	20	126
127	20	127
128	20	128
129	20	129
130	21	130
131	21	131
132	21	132
133	21	133
134	21	134
135	21	135
136	21	136
137	21	137
138	22	138
139	22	139
140	22	140
141	22	141
142	22	142
143	22	143
144	22	144
145	22	145
146	22	146
147	22	147
148	22	148
149	23	149
150	23	150
151	23	151
152	23	152
153	23	153
154	23	154
155	23	155
156	23	156
157	23	157
158	23	158
159	23	159
160	23	160
161	23	161
\.


                         3570.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014250 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3562.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014251 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3568.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014257 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3534.dat                                                                                            0000600 0004000 0002000 00000000005 14341155237 0014250 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           restore.sql                                                                                         0000600 0004000 0002000 00000115556 14341155237 0015406 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Homebrew)

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

DROP DATABASE askem;
--
-- Name: askem; Type: DATABASE; Schema: -; Owner: dev
--

CREATE DATABASE askem WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE askem OWNER TO dev;

\connect askem

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
-- Name: relationtype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.relationtype AS ENUM (
    'cites',
    'copiedfrom',
    'derivedfrom',
    'editedFrom',
    'gluedFrom',
    'stratifiedFrom'
);


ALTER TYPE public.relationtype OWNER TO dev;

--
-- Name: resourcetype; Type: TYPE; Schema: public; Owner: dev
--

CREATE TYPE public.resourcetype AS ENUM (
    'datasets',
    'extractions',
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
    deprecated boolean,
    sensitivity text,
    quality text,
    temporal_resolution character varying,
    geospatial_resolution character varying,
    annotations json,
    maintainer integer NOT NULL
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
-- Name: model; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    framework character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    content json
);


ALTER TABLE public.model OWNER TO dev;

--
-- Name: model_framework; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_framework (
    name character varying NOT NULL,
    version character varying NOT NULL,
    semantics character varying NOT NULL
);


ALTER TABLE public.model_framework OWNER TO dev;

--
-- Name: model_id_seq; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE public.model_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_id_seq OWNER TO dev;

--
-- Name: model_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev
--

ALTER SEQUENCE public.model_id_seq OWNED BY public.model.id;


--
-- Name: model_parameter; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.model_parameter (
    id integer NOT NULL,
    model_id integer NOT NULL,
    name character varying NOT NULL,
    type public.valuetype NOT NULL,
    default_value character varying
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
    active boolean NOT NULL
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
    left_type public.resourcetype NOT NULL,
    "right" integer NOT NULL,
    right_type public.resourcetype NOT NULL,
    user_id integer
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
    xdd_uri character varying NOT NULL
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
-- Name: model id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model ALTER COLUMN id SET DEFAULT nextval('public.model_id_seq'::regclass);


--
-- Name: model_parameter id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_parameter ALTER COLUMN id SET DEFAULT nextval('public.model_parameter_id_seq'::regclass);


--
-- Name: model_runtime id; Type: DEFAULT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime ALTER COLUMN id SET DEFAULT nextval('public.model_runtime_id_seq'::regclass);


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
-- Data for Name: association; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.association (id, person_id, resource_id, resource_type, role) FROM stdin;
\.
COPY public.association (id, person_id, resource_id, resource_type, role) FROM '$$PATH$$/3556.dat';

--
-- Data for Name: dataset; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.dataset (id, name, url, description, "timestamp", deprecated, sensitivity, quality, temporal_resolution, geospatial_resolution, annotations, maintainer) FROM stdin;
\.
COPY public.dataset (id, name, url, description, "timestamp", deprecated, sensitivity, quality, temporal_resolution, geospatial_resolution, annotations, maintainer) FROM '$$PATH$$/3546.dat';

--
-- Data for Name: extraction; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.extraction (id, publication_id, type, data, img) FROM stdin;
\.
COPY public.extraction (id, publication_id, type, data, img) FROM '$$PATH$$/3550.dat';

--
-- Data for Name: feature; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.feature (id, dataset_id, description, display_name, name, value_type) FROM stdin;
\.
COPY public.feature (id, dataset_id, description, display_name, name, value_type) FROM '$$PATH$$/3558.dat';

--
-- Data for Name: intermediate; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.intermediate (id, "timestamp", source, type, content) FROM stdin;
\.
COPY public.intermediate (id, "timestamp", source, type, content) FROM '$$PATH$$/3532.dat';

--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model (id, name, description, framework, "timestamp", content) FROM stdin;
\.
COPY public.model (id, name, description, framework, "timestamp", content) FROM '$$PATH$$/3548.dat';

--
-- Data for Name: model_framework; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_framework (name, version, semantics) FROM stdin;
\.
COPY public.model_framework (name, version, semantics) FROM '$$PATH$$/3530.dat';

--
-- Data for Name: model_parameter; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_parameter (id, model_id, name, type, default_value) FROM stdin;
\.
COPY public.model_parameter (id, model_id, name, type, default_value) FROM '$$PATH$$/3564.dat';

--
-- Data for Name: model_runtime; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_runtime (id, "timestamp", name, "left", "right") FROM stdin;
\.
COPY public.model_runtime (id, "timestamp", name, "left", "right") FROM '$$PATH$$/3544.dat';

--
-- Data for Name: ontology_concept; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.ontology_concept (id, curie, type, object_id, status) FROM stdin;
\.
COPY public.ontology_concept (id, curie, type, object_id, status) FROM '$$PATH$$/3540.dat';

--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.person (id, name, email, org, website, is_registered) FROM stdin;
\.
COPY public.person (id, name, email, org, website, is_registered) FROM '$$PATH$$/3542.dat';

--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project (id, name, description, "timestamp", active) FROM stdin;
\.
COPY public.project (id, name, description, "timestamp", active) FROM '$$PATH$$/3538.dat';

--
-- Data for Name: project_asset; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project_asset (id, project_id, resource_id, resource_type, external_ref) FROM stdin;
\.
COPY public.project_asset (id, project_id, resource_id, resource_type, external_ref) FROM '$$PATH$$/3552.dat';

--
-- Data for Name: provenance; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.provenance (id, "timestamp", relation_type, "left", left_type, "right", right_type, user_id) FROM stdin;
\.
COPY public.provenance (id, "timestamp", relation_type, "left", left_type, "right", right_type, user_id) FROM '$$PATH$$/3554.dat';

--
-- Data for Name: publication; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.publication (id, xdd_uri) FROM stdin;
\.
COPY public.publication (id, xdd_uri) FROM '$$PATH$$/3536.dat';

--
-- Data for Name: qualifier; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier (id, dataset_id, description, name, value_type) FROM stdin;
\.
COPY public.qualifier (id, dataset_id, description, name, value_type) FROM '$$PATH$$/3560.dat';

--
-- Data for Name: qualifier_xref; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier_xref (id, qualifier_id, feature_id) FROM stdin;
\.
COPY public.qualifier_xref (id, qualifier_id, feature_id) FROM '$$PATH$$/3566.dat';

--
-- Data for Name: simulation_parameter; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_parameter (id, run_id, name, value, type) FROM stdin;
\.
COPY public.simulation_parameter (id, run_id, name, value, type) FROM '$$PATH$$/3570.dat';

--
-- Data for Name: simulation_plan; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_plan (id, model_id, simulator, query, content) FROM stdin;
\.
COPY public.simulation_plan (id, model_id, simulator, query, content) FROM '$$PATH$$/3562.dat';

--
-- Data for Name: simulation_run; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_run (id, simulator_id, "timestamp", completed_at, success, response) FROM stdin;
\.
COPY public.simulation_run (id, simulator_id, "timestamp", completed_at, success, response) FROM '$$PATH$$/3568.dat';

--
-- Data for Name: software; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.software (id, "timestamp", source, storage_uri) FROM stdin;
\.
COPY public.software (id, "timestamp", source, storage_uri) FROM '$$PATH$$/3534.dat';

--
-- Name: association_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.association_id_seq', 1, false);


--
-- Name: dataset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.dataset_id_seq', 23, true);


--
-- Name: extraction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.extraction_id_seq', 1, false);


--
-- Name: feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.feature_id_seq', 161, true);


--
-- Name: intermediate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.intermediate_id_seq', 24, true);


--
-- Name: model_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_id_seq', 1, false);


--
-- Name: model_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_parameter_id_seq', 1, false);


--
-- Name: model_runtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_runtime_id_seq', 1, false);


--
-- Name: ontology_concept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.ontology_concept_id_seq', 48, true);


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.person_id_seq', 1, true);


--
-- Name: project_asset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_asset_id_seq', 71, true);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_id_seq', 1, true);


--
-- Name: provenance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.provenance_id_seq', 24, true);


--
-- Name: publication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.publication_id_seq', 24, true);


--
-- Name: qualifier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_id_seq', 23, true);


--
-- Name: qualifier_xref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_xref_id_seq', 161, true);


--
-- Name: simulation_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.simulation_parameter_id_seq', 1, false);


--
-- Name: simulation_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.simulation_plan_id_seq', 1, false);


--
-- Name: simulation_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.simulation_run_id_seq', 1, false);


--
-- Name: software_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.software_id_seq', 1, false);


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
-- Name: model model_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_pkey PRIMARY KEY (id);


--
-- Name: model_runtime model_runtime_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_runtime
    ADD CONSTRAINT model_runtime_pkey PRIMARY KEY (id);


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
-- Name: model model_framework_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_framework_fkey FOREIGN KEY (framework) REFERENCES public.model_framework(name);


--
-- Name: model_parameter model_parameter_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.model_parameter
    ADD CONSTRAINT model_parameter_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model(id);


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
    ADD CONSTRAINT simulation_plan_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.model(id);


--
-- Name: simulation_run simulation_run_simulator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.simulation_run
    ADD CONSTRAINT simulation_run_simulator_id_fkey FOREIGN KEY (simulator_id) REFERENCES public.simulation_plan(id);


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  