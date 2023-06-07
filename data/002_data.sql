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
-- Data for Name: active_concept; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.active_concept (curie, name) FROM stdin;
ido:0000512	diseased population
ido:0000514	susceptible population
ido:0000592	immune population
apollosv:00000154	exposed population
ido:0000511	infected population
ido:0000573	symptomatic host of infectious agent
ncit:C28554	Dead
ncit:C113725	Undiagnosed
ido:0000621	acquired immunity to infectious agent
ncit:C15220	Diagnosis
ncit:C25587	Newly Diagnosed
ido:0000468	susceptibility to infectious agent
covoc:0010003	confirmed case
disdriv:0000002	socioeconomic drivers
apollosv:00000497	count of disease cases
vo:0004908	COVID-19 vaccine
so:0001564	gene_variant
cemo:cumulative_cases	cumulative cases
cemo:number_of_tests	number of tests
cemo:daily_cases	daily cases
askemo:0000001	population
vo:0000595	vaccine dose
ncit:C28320	Booster
ncit:C25179	Hospitalization
ncit:C173779	Case Fatality Rate
cemo:number_of_deaths_new_this_week	number of deaths new this week
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.alembic_version (version_num) FROM stdin;
139b9ec56f3e
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.person (id, name, email, org, website, is_registered) FROM stdin;
1	Adam Smith	Adam@test.io	Uncharted		t
\.


--
-- Data for Name: association; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.association (id, person_id, resource_id, resource_type, role) FROM stdin;
\.


--
-- Data for Name: dataset; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.dataset (id, name, url, description, "timestamp", deprecated, sensitivity, quality, temporal_resolution, geospatial_resolution, annotations, data_path, maintainer, simulation_result) FROM stdin;
52	COVID-19 Nursing Home Data	https://data.cms.gov/covid-19/covid-19-nursing-home-data/data	Nursing home cases and deaths at the county level from Centers for Medicare & Medicaid Services (CMS)	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/52/d7ac1807-99d4-4d11-a75f-1de76af57d45.parquet.gzip"]}	"s3://datasets/52/d7ac1807-99d4-4d11-a75f-1de76af57d45.parquet.gzip"	1	f
26	Simulation output from CHIME-SVIIvR : run number 2		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 2	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/26/sim_output.csv"]}	"s3://datasets/26/sim_output.csv"	1	t
45	CDC COVID-19 Vaccination and Case Trends by Age Group	https://data.cdc.gov/Vaccinations/Archive-COVID-19-Vaccination-and-Case-Trends-by-Ag/gxj9-t96f/data	COVID-19 Vaccination and Case Trends by Age Group	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/45/419e141a-2ba9-4fc8-91ba-27698a12a6e6.parquet.gzip"]}	"s3://datasets/45/419e141a-2ba9-4fc8-91ba-27698a12a6e6.parquet.gzip"	1	f
1	Simulation output from Bucky : run number 0		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 0	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/1/sim_output.csv"]}	"s3://datasets/1/sim_output.csv"	1	t
2	Simulation output from Bucky : run number 1		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 1	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/2/sim_output.csv"]}	"s3://datasets/2/sim_output.csv"	1	t
48	US Daily COVID-19 Confirmed Case Counts from JHU CSSE	https://github.com/CSSEGISandData/COVID-19	This is the data repository for the 2019 Novel Coronavirus Visual Dashboard operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). Also, Supported by ESRI Living Atlas Team and the Johns Hopkins University Applied Physics Lab (JHU APL).	2023-05-12 14:58:36.63499	f		Data is aggregated from a variety of sources.			{"annotations": {}, "data_paths": ["s3://datasets/48/7782dad0-2867-41e0-bddb-f435c796ef8f.parquet.gzip"]}	"s3://datasets/48/7782dad0-2867-41e0-bddb-f435c796ef8f.parquet.gzip"	1	f
3	Simulation output from Bucky : run number 10		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 10	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/3/sim_output.csv"]}	"s3://datasets/3/sim_output.csv"	1	t
4	Simulation output from Bucky : run number 2		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 2	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/4/sim_output.csv"]}	"s3://datasets/4/sim_output.csv"	1	t
5	Simulation output from Bucky : run number 3		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 3	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/5/sim_output.csv"]}	"s3://datasets/5/sim_output.csv"	1	t
6	Simulation output from Bucky : run number 4		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 4	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/6/sim_output.csv"]}	"s3://datasets/6/sim_output.csv"	1	t
7	Simulation output from Bucky : run number 5		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 5	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/7/sim_output.csv"]}	"s3://datasets/7/sim_output.csv"	1	t
8	Simulation output from Bucky : run number 6		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 6	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/8/sim_output.csv"]}	"s3://datasets/8/sim_output.csv"	1	t
9	Simulation output from Bucky : run number 7		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 7	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/9/sim_output.csv"]}	"s3://datasets/9/sim_output.csv"	1	t
20	Simulation output from CHIME-SIR : run number 7		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 7	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/20/sim_output.csv"]}	"s3://datasets/20/sim_output.csv"	1	t
10	Simulation output from Bucky : run number 8		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 8	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/10/sim_output.csv"]}	"s3://datasets/10/sim_output.csv"	1	t
11	Simulation output from Bucky : run number 9		Dataset from simulation run output- Model description: Bucky was used to create this dataset. Run number 9	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_mild", "display_name": "", "description": "I_mild state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_asym", "display_name": "", "description": "I_asym state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_hosp", "display_name": "", "description": "I_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "E", "display_name": "", "description": "E state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "D", "display_name": "", "description": "D state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R_hosp", "display_name": "", "description": "R_hosp state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I_mild", "time", "I_asym", "I_hosp", "E", "R", "D", "R_hosp"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/11/sim_output.csv"]}	"s3://datasets/11/sim_output.csv"	1	t
12	Simulation output from CHIME-SIR : run number 0		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 0	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/12/sim_output.csv"]}	"s3://datasets/12/sim_output.csv"	1	t
13	Simulation output from CHIME-SIR : run number 1		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 1	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/13/sim_output.csv"]}	"s3://datasets/13/sim_output.csv"	1	t
14	Simulation output from CHIME-SIR : run number 10		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 10	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/14/sim_output.csv"]}	"s3://datasets/14/sim_output.csv"	1	t
15	Simulation output from CHIME-SIR : run number 2		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 2	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/15/sim_output.csv"]}	"s3://datasets/15/sim_output.csv"	1	t
16	Simulation output from CHIME-SIR : run number 3		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 3	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/16/sim_output.csv"]}	"s3://datasets/16/sim_output.csv"	1	t
17	Simulation output from CHIME-SIR : run number 4		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 4	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/17/sim_output.csv"]}	"s3://datasets/17/sim_output.csv"	1	t
18	Simulation output from CHIME-SIR : run number 5		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 5	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/18/sim_output.csv"]}	"s3://datasets/18/sim_output.csv"	1	t
19	Simulation output from CHIME-SIR : run number 6		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 6	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/19/sim_output.csv"]}	"s3://datasets/19/sim_output.csv"	1	t
22	Simulation output from CHIME-SIR : run number 9		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 9	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/22/sim_output.csv"]}	"s3://datasets/22/sim_output.csv"	1	t
23	Simulation output from CHIME-SVIIvR : run number 0		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 0	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/23/sim_output.csv"]}	"s3://datasets/23/sim_output.csv"	1	t
24	Simulation output from CHIME-SVIIvR : run number 1		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 1	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/24/sim_output.csv"]}	"s3://datasets/24/sim_output.csv"	1	t
25	Simulation output from CHIME-SVIIvR : run number 10		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 10	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/25/sim_output.csv"]}	"s3://datasets/25/sim_output.csv"	1	t
28	Simulation output from CHIME-SVIIvR : run number 4		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 4	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/28/sim_output.csv"]}	"s3://datasets/28/sim_output.csv"	1	t
21	Simulation output from CHIME-SIR : run number 8		Dataset from simulation run output- Model description: CHIME-SIR was used to create this dataset. Run number 8	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "time", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/21/sim_output.csv"]}	"s3://datasets/21/sim_output.csv"	1	t
27	Simulation output from CHIME-SVIIvR : run number 3		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 3	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/27/sim_output.csv"]}	"s3://datasets/27/sim_output.csv"	1	t
29	Simulation output from CHIME-SVIIvR : run number 5		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 5	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/29/sim_output.csv"]}	"s3://datasets/29/sim_output.csv"	1	t
30	Simulation output from CHIME-SVIIvR : run number 6		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 6	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/30/sim_output.csv"]}	"s3://datasets/30/sim_output.csv"	1	t
31	Simulation output from CHIME-SVIIvR : run number 7		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 7	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/31/sim_output.csv"]}	"s3://datasets/31/sim_output.csv"	1	t
32	Simulation output from CHIME-SVIIvR : run number 8		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 8	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/32/sim_output.csv"]}	"s3://datasets/32/sim_output.csv"	1	t
33	Simulation output from CHIME-SVIIvR : run number 9		Dataset from simulation run output- Model description: CHIME-SVIIvR was used to create this dataset. Run number 9	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "S", "display_name": "", "description": "S state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I", "display_name": "", "description": "I state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "V", "display_name": "", "description": "V state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "I_v", "display_name": "", "description": "I_v state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "R", "display_name": "", "description": "R state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["S", "I", "V", "time", "I_v", "R"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/33/sim_output.csv"]}	"s3://datasets/33/sim_output.csv"	1	t
34	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 1		Dataset from simulation run output- Model description: Baseline scenario (see Fig. 2): \n        Day 1, before the introduction of any public health measures (R0 = 2.38); \n        Day 4, introduction of basic public health recommendations and government school closures (R0 = 1.66); \n        Day 12, policy of limiting screening to symptomatic individuals only (R0 = 1.80);\n        Day 22: introduction of incomplete lockdown (R0 = 1.60);\n        Day 28: fully operational lockdown with strict measures, working is no longer a good reason for going out: gradually, non-indispensable activities are stopped (R0 = 0.99);\n        Day 38: wider testing campaign is launched (R0 = 0.85).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/34/sim_output.csv"]}	"s3://datasets/34/sim_output.csv"	1	t
35	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 2		Dataset from simulation run output- Model description: Future scenario (see Fig. 3a, b) : Day 1-49, baseline; Day 50: the lockdown is weakened by increasing the S-I transmission rate `alpha` from 0.210 to 0.252 (R0 = 0.98).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/35/sim_output.csv"]}	"s3://datasets/35/sim_output.csv"	1	t
36	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 3		Dataset from simulation run output- Model description: Future scenario (see Fig. 3c, d) : Day 1-49, baseline; Day 50: the lockdown is strengthened by decreasing the S-I transmission rate `alpha` from 0.210 to 0.105 (R0 = 0.50).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/36/sim_output.csv"]}	"s3://datasets/36/sim_output.csv"	1	t
37	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 4		Dataset from simulation run output- Model description: Future scenario (see Fig. 4a, b): Day 1-49, baseline; Day 50: introduction of population-wide testing and contact tracing by increasing the asymptomatic-case detection rate `epsilon` from 0.200 to 0.400 (R0 = 0.59)	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/37/sim_output.csv"]}	"s3://datasets/37/sim_output.csv"	1	t
38	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 5		Dataset from simulation run output- Model description: Future scenario (see Fig. 4c, d): Day 1-49, baseline; Day 50: a milder lockdown with widespread testing and contact tracing by increasing the S-I transmission rate `alpha` from 0.210 to 0.420 and increasing the asymptomatic-case detection rate `epsilon` from 0.200 to 0.600 (R0 = 0.77).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/38/sim_output.csv"]}	"s3://datasets/38/sim_output.csv"	1	t
44	Monthly State Retail Sales (Year on Year)	https://www.census.gov/retail/state_retail_sales.html	The Monthly State Retail Sales (MSRS) is the Census Bureau's new experimental data product featuring modeled state-level retail sales. This is a blended data product using Monthly Retail Trade Survey data, administrative data, and third-party data. Year-over-year percentage changes are available for Total Retail Sales excluding Nonstore Retailers as well as 11 retail North American Industry Classification System (NAICS) retail subsectors. These data are provided by state and NAICS codes beginning with January 2019. The Census Bureau plans to continue to improve the methodology to be able to publish more data in the future.	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/44/289c7406-3695-4c2b-90d0-e88606abe7f9.parquet.gzip"]}	"s3://datasets/44/289c7406-3695-4c2b-90d0-e88606abe7f9.parquet.gzip"	1	f
39	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 6		Dataset from simulation run output- Model description: Alternate scenario (see Extended Fig. 1a, b): Day 1-21, baseline; Day 22: absence of further countermeasures after day 22, just closing schools and hygiene recommendations - transmission rates `alpha` = 0.422, `gamma` = 0.285 and `beta` = `delta` = 0.0057 (R0 = 1.66).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/39/sim_output.csv"]}	"s3://datasets/39/sim_output.csv"	1	t
49	New York Population by City	https://worldpopulationreview.com/states/cities/new-york	Population of cities in New York State	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/49/794ae391-fe6b-4cdd-8757-0afdf45e5140.parquet.gzip"]}	"s3://datasets/49/794ae391-fe6b-4cdd-8757-0afdf45e5140.parquet.gzip"	1	f
40	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 7		Dataset from simulation run output- Model description: Alternate scenario (see Extended Fig. 1c, d): Day 1-21, baseline; Day 22: mild social-distancing countermeasures - transmission rates `alpha` = 0.285 and `gamma` = 0.171 (R0 = 1.13).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/40/sim_output.csv"]}	"s3://datasets/40/sim_output.csv"	1	t
41	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 8		Dataset from simulation run output- Model description: Alternate scenario (see Extended Fig. 1e, f): Day 1-21, baseline; Day 22: stronger social-distancing countermeasures - transmission rates `alpha` = 0.200 and `gamma` = 0.086 (R0 = 0.787).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/41/sim_output.csv"]}	"s3://datasets/41/sim_output.csv"	1	t
47	New York Positive Tests Over Time	https://coronavirus.health.ny.gov/positive-tests-over-time-region-and-county	Positive COVID-19 tests over time for New York by Region and County.\n\nThis dataset includes information on the number of tests of individuals for COVID-19 infection performed in New York State beginning March 1, 2020, when the first case of COVID-19 was identified in the state. The primary goal of publishing this dataset is to provide users timely information about local disease spread and reporting of positive cases. The data will be updated daily, reflecting tests completed by 12:00 am (midnight) the day of the update (i.e., all tests reported by the end of the day on the day before the update).	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/47/6d274390-ca90-407e-a9cc-39e5be57d53a.parquet.gzip", "s3://datasets/47/6d274390-ca90-407e-a9cc-39e5be57d53a_str.parquet.gzip"]}	"s3://datasets/47/6d274390-ca90-407e-a9cc-39e5be57d53a.parquet.gzip"	1	f
51	New York State Daily Hospitalization Summary	https://coronavirus.health.ny.gov/daily-hospitalization-summary	Daily hospitalization summary by region. \n\nNew admissions and total hospitalization data come from the Health Electronic Response Data System (HERDS). Hospitals are required to complete this survey Monday through Friday and data reflects information reported by hospitals through the survey each day. These data include NYS resident and non-NYS resident hospitalizations.\n\nHealth care facilities pause COVID-19 data submission through the Health Electronic Response Data System (HERDS) during weekends and certain holidays. Therefore, the dashboard will show no data for those dates. The first reporting date thereafter will contain those data and estimated 7-day averages are provided for all days.	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/51/b42882f4-3823-424c-94f2-cb6d8f383984.parquet.gzip"]}	"s3://datasets/51/b42882f4-3823-424c-94f2-cb6d8f383984.parquet.gzip"	1	f
42	Biomodel simulation output: Giordano2020 - SIDARTHE model of COVID-19 spread in Italy run number - 9		Dataset from simulation run output- Model description: Alternate scenario (see Extended Fig. 1g, h): Day 1-21, baseline; Day 22: even stronger social-distancing countermeasures - transmission rates `alpha` = `gamma` = 0.057 (R0 = 0.0329).	2023-05-12 14:58:36.63499	f		Measured			{"annotations": {"geo": [{"name": "mock_lon", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "longitude", "primary_geo": true, "resolve_to_gadm": false, "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}, {"name": "mock_lat", "display_name": "loc", "description": "location", "type": "geo", "geo_type": "latitude", "primary_geo": true, "resolve_to_gadm": false, "is_geo_pair": "mock_lon", "coord_format": "lonlat", "qualifies": [], "aliases": {}, "gadm_level": "admin1"}], "date": [{"name": "mock_time", "display_name": "", "description": "date", "type": "date", "date_type": "date", "primary_date": true, "time_format": "%m/%d/%Y", "qualifies": [], "aliases": {}}], "feature": [{"name": "Infected", "display_name": "", "description": "Infected state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Healed", "display_name": "", "description": "Healed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000621", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Extinct", "display_name": "", "description": "Extinct state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Diagnosed", "display_name": "", "description": "Diagnosed state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Ailing", "display_name": "", "description": "Ailing state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C113725", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Recognized", "display_name": "", "description": "Recognized state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C25587", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Susceptible", "display_name": "", "description": "Susceptible state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ido:0000468", "qualifierrole": "breakdown", "aliases": {}}, {"name": "Threatened", "display_name": "", "description": "Threatened state feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": [], "primary_ontology_id": "ncit:C15220", "qualifierrole": "breakdown", "aliases": {}}, {"name": "time", "display_name": "", "description": "time step feature", "type": "feature", "feature_type": "float", "units": "na", "units_description": "", "qualifies": ["Infected", "Healed", "Extinct", "Diagnosed", "Ailing", "Recognized", "time", "Susceptible", "Threatened"], "primary_ontology_id": "", "qualifierrole": "breakdown", "aliases": {}}]}, "data_paths": ["s3://datasets/42/sim_output.csv"]}	"s3://datasets/42/sim_output.csv"	1	t
46	COVID-19 Variant Proportions (USA)	https://covid.cdc.gov/covid-data-tracker/#variant-proportions	SARS-CoV-2, the virus that causes COVID-19, is constantly changing and accumulating mutations in its genetic code over time. New variants of SARS-CoV-2 are expected to continue to emerge. Some variants will emerge and disappear, while others will emerge and continue to spread and may replace previous variants.\n\nTo identify and track SARS-CoV-2 variants, CDC uses genomic surveillance. CDC's national genomic surveillance system collects SARS-CoV-2 specimens for sequencing through the National SARS-CoV-2 Strain Surveillance (NS3) program, as well as SARS-CoV-2 sequences generated by commercial or academic laboratories contracted by CDC and state or local public health laboratories. Virus genetic sequences are analyzed and classified as a particular variant. The proportion of variants in a population are calculated nationally, by HHS region, and by jurisdiction. The thousands of sequences analyzed every week through CDC’s national genomic sequencing and bioinformatics efforts fuel the comprehensive and population-based U.S. surveillance system established to identify and monitor the spread of variants.\n\nRapid virus genomic sequencing data combined with phenotypic data are further used to determine whether COVID-19 tests, treatments, and vaccines authorized or approved for use in the United States will work against emerging variants.	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/46/69d17d0c-8009-4b48-afc2-b87d49f937d2.parquet.gzip"]}	"s3://datasets/46/69d17d0c-8009-4b48-afc2-b87d49f937d2.parquet.gzip"	1	f
50	COVID-19 Vaccination Demographics in the United States	https://data.cdc.gov/Vaccinations/COVID-19-Vaccination-Demographics-in-the-United-St/km4m-vcsb/data	Overall Demographic Characteristics of People Receiving COVID-19 Vaccinations in the United States at national level. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities. 	2023-05-12 14:58:36.63499	f					{"annotations": {}, "data_paths": ["s3://datasets/50/9554fca6-1143-4fe3-adce-c528a0b7d886.parquet.gzip"]}	"s3://datasets/50/9554fca6-1143-4fe3-adce-c528a0b7d886.parquet.gzip"	1	f
43	US Daily COVID-19 Confirmed Case Counts from JHU CSSE	https://github.com/CSSEGISandData/COVID-19	This is the data repository for the 2019 Novel Coronavirus Visual Dashboard operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). Also, Supported by ESRI Living Atlas Team and the Johns Hopkins University Applied Physics Lab (JHU APL).	2023-05-12 14:58:36.63499	f		Data is aggregated from multiple sources.			{"annotations": {}, "data_paths": ["s3://datasets/43/0ac71f26-dfb9-48e7-a51c-bdcb43dae9ac.parquet.gzip"]}	"s3://datasets/43/0ac71f26-dfb9-48e7-a51c-bdcb43dae9ac.parquet.gzip"	1	f
\.


--
-- Data for Name: publication; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.publication (id, xdd_uri, title) FROM stdin;
1	60fee31f67467f7269153935	CHIME (COVID-19 Hospital Impact Model for Epidemics) Manual
2	616cf16267467f7269ccde6f	Modelling the COVID-19 epidemic and implementation of population-wide interventions in Italy
\.


--
-- Data for Name: extraction; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.extraction (id, publication_id, type, data, img) FROM stdin;
\.


--
-- Data for Name: feature; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.feature (id, dataset_id, description, display_name, name, value_type) FROM stdin;
1	1	S state feature	S	S	float
2	1	I_mild state feature	I_mild	I_mild	float
3	1	time state feature	time	time	float
4	1	I_asym state feature	I_asym	I_asym	float
5	1	I_hosp state feature	I_hosp	I_hosp	float
6	1	E state feature	E	E	float
7	1	R state feature	R	R	float
8	1	D state feature	D	D	float
9	1	R_hosp state feature	R_hosp	R_hosp	float
10	2	S state feature	S	S	float
11	2	I_mild state feature	I_mild	I_mild	float
12	2	time state feature	time	time	float
13	2	I_asym state feature	I_asym	I_asym	float
14	2	I_hosp state feature	I_hosp	I_hosp	float
15	2	E state feature	E	E	float
16	2	R state feature	R	R	float
17	2	D state feature	D	D	float
18	2	R_hosp state feature	R_hosp	R_hosp	float
19	3	S state feature	S	S	float
20	3	I_mild state feature	I_mild	I_mild	float
21	3	time state feature	time	time	float
22	3	I_asym state feature	I_asym	I_asym	float
23	3	I_hosp state feature	I_hosp	I_hosp	float
24	3	E state feature	E	E	float
25	3	R state feature	R	R	float
26	3	D state feature	D	D	float
27	3	R_hosp state feature	R_hosp	R_hosp	float
28	4	S state feature	S	S	float
29	4	I_mild state feature	I_mild	I_mild	float
30	4	time state feature	time	time	float
31	4	I_asym state feature	I_asym	I_asym	float
32	4	I_hosp state feature	I_hosp	I_hosp	float
33	4	E state feature	E	E	float
34	4	R state feature	R	R	float
35	4	D state feature	D	D	float
36	4	R_hosp state feature	R_hosp	R_hosp	float
37	5	S state feature	S	S	float
38	5	I_mild state feature	I_mild	I_mild	float
39	5	time state feature	time	time	float
40	5	I_asym state feature	I_asym	I_asym	float
41	5	I_hosp state feature	I_hosp	I_hosp	float
42	5	E state feature	E	E	float
43	5	R state feature	R	R	float
44	5	D state feature	D	D	float
45	5	R_hosp state feature	R_hosp	R_hosp	float
46	6	S state feature	S	S	float
47	6	I_mild state feature	I_mild	I_mild	float
48	6	time state feature	time	time	float
49	6	I_asym state feature	I_asym	I_asym	float
50	6	I_hosp state feature	I_hosp	I_hosp	float
51	6	E state feature	E	E	float
52	6	R state feature	R	R	float
53	6	D state feature	D	D	float
54	6	R_hosp state feature	R_hosp	R_hosp	float
55	7	S state feature	S	S	float
56	7	I_mild state feature	I_mild	I_mild	float
57	7	time state feature	time	time	float
58	7	I_asym state feature	I_asym	I_asym	float
59	7	I_hosp state feature	I_hosp	I_hosp	float
60	7	E state feature	E	E	float
61	7	R state feature	R	R	float
62	7	D state feature	D	D	float
63	7	R_hosp state feature	R_hosp	R_hosp	float
64	8	S state feature	S	S	float
65	8	I_mild state feature	I_mild	I_mild	float
66	8	time state feature	time	time	float
67	8	I_asym state feature	I_asym	I_asym	float
68	8	I_hosp state feature	I_hosp	I_hosp	float
69	8	E state feature	E	E	float
70	8	R state feature	R	R	float
71	8	D state feature	D	D	float
72	8	R_hosp state feature	R_hosp	R_hosp	float
73	9	S state feature	S	S	float
74	9	I_mild state feature	I_mild	I_mild	float
75	9	time state feature	time	time	float
76	9	I_asym state feature	I_asym	I_asym	float
77	9	I_hosp state feature	I_hosp	I_hosp	float
78	9	E state feature	E	E	float
79	9	R state feature	R	R	float
80	9	D state feature	D	D	float
81	9	R_hosp state feature	R_hosp	R_hosp	float
82	10	S state feature	S	S	float
83	10	I_mild state feature	I_mild	I_mild	float
84	10	time state feature	time	time	float
85	10	I_asym state feature	I_asym	I_asym	float
86	10	I_hosp state feature	I_hosp	I_hosp	float
87	10	E state feature	E	E	float
88	10	R state feature	R	R	float
89	10	D state feature	D	D	float
90	10	R_hosp state feature	R_hosp	R_hosp	float
91	11	S state feature	S	S	float
92	11	I_mild state feature	I_mild	I_mild	float
93	11	time state feature	time	time	float
94	11	I_asym state feature	I_asym	I_asym	float
95	11	I_hosp state feature	I_hosp	I_hosp	float
96	11	E state feature	E	E	float
97	11	R state feature	R	R	float
98	11	D state feature	D	D	float
99	11	R_hosp state feature	R_hosp	R_hosp	float
100	12	S state feature	S	S	float
101	12	I state feature	I	I	float
102	12	time state feature	time	time	float
103	12	R state feature	R	R	float
104	13	S state feature	S	S	float
105	13	I state feature	I	I	float
106	13	time state feature	time	time	float
107	13	R state feature	R	R	float
108	14	S state feature	S	S	float
109	14	I state feature	I	I	float
110	14	time state feature	time	time	float
111	14	R state feature	R	R	float
112	15	S state feature	S	S	float
113	15	I state feature	I	I	float
114	15	time state feature	time	time	float
115	15	R state feature	R	R	float
116	16	S state feature	S	S	float
117	16	I state feature	I	I	float
118	16	time state feature	time	time	float
119	16	R state feature	R	R	float
120	17	S state feature	S	S	float
121	17	I state feature	I	I	float
124	18	S state feature	S	S	float
129	19	I state feature	I	I	float
132	20	S state feature	S	S	float
137	21	I state feature	I	I	float
140	22	S state feature	S	S	float
144	23	S state feature	S	S	float
149	23	R state feature	R	R	float
151	24	I state feature	I	I	float
157	25	I state feature	I	I	float
164	26	V state feature	V	V	float
170	27	V state feature	V	V	float
177	28	time state feature	time	time	float
183	29	time state feature	time	time	float
190	30	I_v state feature	I_v	I_v	float
192	31	S state feature	S	S	float
197	31	R state feature	R	R	float
122	17	time state feature	time	time	float
127	18	R state feature	R	R	float
130	19	time state feature	time	time	float
135	20	R state feature	R	R	float
138	21	time state feature	time	time	float
143	22	R state feature	R	R	float
146	23	V state feature	V	V	float
152	24	V state feature	V	V	float
159	25	time state feature	time	time	float
165	26	time state feature	time	time	float
172	27	I_v state feature	I_v	I_v	float
178	28	I_v state feature	I_v	I_v	float
181	29	I state feature	I	I	float
189	30	time state feature	time	time	float
196	31	I_v state feature	I_v	I_v	float
123	17	R state feature	R	R	float
126	18	time state feature	time	time	float
131	19	R state feature	R	R	float
134	20	time state feature	time	time	float
139	21	R state feature	R	R	float
142	22	time state feature	time	time	float
145	23	I state feature	I	I	float
153	24	time state feature	time	time	float
156	25	S state feature	S	S	float
161	25	R state feature	R	R	float
162	26	S state feature	S	S	float
167	26	R state feature	R	R	float
169	27	I state feature	I	I	float
175	28	I state feature	I	I	float
182	29	V state feature	V	V	float
188	30	V state feature	V	V	float
194	31	V state feature	V	V	float
125	18	I state feature	I	I	float
128	19	S state feature	S	S	float
133	20	I state feature	I	I	float
136	21	S state feature	S	S	float
141	22	I state feature	I	I	float
147	23	time state feature	time	time	float
154	24	I_v state feature	I_v	I_v	float
160	25	I_v state feature	I_v	I_v	float
163	26	I state feature	I	I	float
171	27	time state feature	time	time	float
174	28	S state feature	S	S	float
179	28	R state feature	R	R	float
180	29	S state feature	S	S	float
185	29	R state feature	R	R	float
187	30	I state feature	I	I	float
195	31	time state feature	time	time	float
148	23	I_v state feature	I_v	I_v	float
150	24	S state feature	S	S	float
155	24	R state feature	R	R	float
158	25	V state feature	V	V	float
166	26	I_v state feature	I_v	I_v	float
168	27	S state feature	S	S	float
173	27	R state feature	R	R	float
176	28	V state feature	V	V	float
184	29	I_v state feature	I_v	I_v	float
186	30	S state feature	S	S	float
191	30	R state feature	R	R	float
193	31	I state feature	I	I	float
198	32	S state feature	S	S	float
199	32	I state feature	I	I	float
200	32	V state feature	V	V	float
201	32	time state feature	time	time	float
202	32	I_v state feature	I_v	I_v	float
203	32	R state feature	R	R	float
204	33	S state feature	S	S	float
205	33	I state feature	I	I	float
206	33	V state feature	V	V	float
207	33	time state feature	time	time	float
208	33	I_v state feature	I_v	I_v	float
209	33	R state feature	R	R	float
210	34	Infected state feature	Infected	Infected	float
211	34	Healed state feature	Healed	Healed	float
212	34	Extinct state feature	Extinct	Extinct	float
213	34	Diagnosed state feature	Diagnosed	Diagnosed	float
214	34	Ailing state feature	Ailing	Ailing	float
215	34	Recognized state feature	Recognized	Recognized	float
216	34	time state feature	time	time	float
217	34	Susceptible state feature	Susceptible	Susceptible	float
218	34	Threatened state feature	Threatened	Threatened	float
219	35	Infected state feature	Infected	Infected	float
220	35	Healed state feature	Healed	Healed	float
221	35	Extinct state feature	Extinct	Extinct	float
222	35	Diagnosed state feature	Diagnosed	Diagnosed	float
223	35	Ailing state feature	Ailing	Ailing	float
224	35	Recognized state feature	Recognized	Recognized	float
225	35	time state feature	time	time	float
226	35	Susceptible state feature	Susceptible	Susceptible	float
227	35	Threatened state feature	Threatened	Threatened	float
228	36	Infected state feature	Infected	Infected	float
229	36	Healed state feature	Healed	Healed	float
230	36	Extinct state feature	Extinct	Extinct	float
231	36	Diagnosed state feature	Diagnosed	Diagnosed	float
232	36	Ailing state feature	Ailing	Ailing	float
233	36	Recognized state feature	Recognized	Recognized	float
234	36	time state feature	time	time	float
235	36	Susceptible state feature	Susceptible	Susceptible	float
236	36	Threatened state feature	Threatened	Threatened	float
237	37	Infected state feature	Infected	Infected	float
238	37	Healed state feature	Healed	Healed	float
239	37	Extinct state feature	Extinct	Extinct	float
240	37	Diagnosed state feature	Diagnosed	Diagnosed	float
241	37	Ailing state feature	Ailing	Ailing	float
242	37	Recognized state feature	Recognized	Recognized	float
243	37	time state feature	time	time	float
244	37	Susceptible state feature	Susceptible	Susceptible	float
245	37	Threatened state feature	Threatened	Threatened	float
246	38	Infected state feature	Infected	Infected	float
247	38	Healed state feature	Healed	Healed	float
248	38	Extinct state feature	Extinct	Extinct	float
249	38	Diagnosed state feature	Diagnosed	Diagnosed	float
250	38	Ailing state feature	Ailing	Ailing	float
251	38	Recognized state feature	Recognized	Recognized	float
252	38	time state feature	time	time	float
253	38	Susceptible state feature	Susceptible	Susceptible	float
254	38	Threatened state feature	Threatened	Threatened	float
255	39	Infected state feature	Infected	Infected	float
256	39	Healed state feature	Healed	Healed	float
257	39	Extinct state feature	Extinct	Extinct	float
258	39	Diagnosed state feature	Diagnosed	Diagnosed	float
259	39	Ailing state feature	Ailing	Ailing	float
260	39	Recognized state feature	Recognized	Recognized	float
261	39	time state feature	time	time	float
262	39	Susceptible state feature	Susceptible	Susceptible	float
263	39	Threatened state feature	Threatened	Threatened	float
264	40	Infected state feature	Infected	Infected	float
265	40	Healed state feature	Healed	Healed	float
266	40	Extinct state feature	Extinct	Extinct	float
267	40	Diagnosed state feature	Diagnosed	Diagnosed	float
268	40	Ailing state feature	Ailing	Ailing	float
269	40	Recognized state feature	Recognized	Recognized	float
270	40	time state feature	time	time	float
271	40	Susceptible state feature	Susceptible	Susceptible	float
272	40	Threatened state feature	Threatened	Threatened	float
273	41	Infected state feature	Infected	Infected	float
274	41	Healed state feature	Healed	Healed	float
275	41	Extinct state feature	Extinct	Extinct	float
276	41	Diagnosed state feature	Diagnosed	Diagnosed	float
277	41	Ailing state feature	Ailing	Ailing	float
278	41	Recognized state feature	Recognized	Recognized	float
279	41	time state feature	time	time	float
280	41	Susceptible state feature	Susceptible	Susceptible	float
281	41	Threatened state feature	Threatened	Threatened	float
282	42	Infected state feature	Infected	Infected	float
283	42	Healed state feature	Healed	Healed	float
284	42	Extinct state feature	Extinct	Extinct	float
285	42	Diagnosed state feature	Diagnosed	Diagnosed	float
286	42	Ailing state feature	Ailing	Ailing	float
287	42	Recognized state feature	Recognized	Recognized	float
288	42	time state feature	time	time	float
289	42	Susceptible state feature	Susceptible	Susceptible	float
295	45	Completion of COVID-19 vaccine series by age group as a percentage		Series_Complete_Pop_pct_agegroup	float
300	47	Cumulative positive cases		Cumulative Number of Positives	int
306	49	population density 	population density	density	int
307	50	COVID-19 dose 1 administered		Administered_Dose1	int
325	52	Confirmed nursing home COVID-19 deaths		Residents Weekly COVID-19 Deaths	float
290	42	Threatened state feature	Threatened	Threatened	float
296	46	Share of variant		share	float
301	47	Total Number of Tests Performed		Total Number of Tests Performed	int
304	48	Covid 19 cases	COVID-19 Cases	Cases	int
315	50	Bivalent booster administered		Bivalent_Booster	int
318	51	Patients Admitted Due to COVID		Patients Admitted Due to COVID	int
291	43	Confirmed COVID-19 cases		Cases	int
297	46	Share of variant (high)		share_hi	float
309	50	COVID-19 vaccine series complete		Series_Complete_Yes	int
312	50	Booster doses as percent of age group		Booster_Doses_Vax_pct_agegroup	float
321	51	Total Staffed Beds Currently Available		Total Staffed Beds Currently Available	int
292	44	Not Adjusted State Retail Sales Year-over-Year Percentage Changes		Retail Sales YoY	float
293	45	7 day average cases per 100,000 people by age group		7-day_avg_group_cases_per_100k	float
298	46	Share of variant (low)		share_lo	float
303	47	Test % Positive		Test % Positive	str
310	50	Series complete as percent of age group		Series_Complete_Pop_pct_agegroup	float
313	50	Second booster administered by age group		Second_Booster	int
319	51	Cumulative COVID-19 Fatalities to Date		Cumulative COVID-19 Fatalities to Date	int
322	51	Total Staffed ICU Beds		Total Staffed ICU Beds	int
294	45	Percent of age group receiving 1 dose of COVID-19 vaccine		Administered_Dose1_pct_agegroup	float
305	49	population in 2022	population	pop2022	int
314	50	Booster doses as percent of known		Booster_Doses_Pop_Pct_known	int
316	50	Bivalent booster as percent of age group		Bivalent_Booster_Pop_Pct_agegroup	float
324	52	Confirmed nursing home COVID-19 cases		Residents Weekly Confirmed COVID-19	float
299	47	New positives		New Positives	int
302	47	Cumulative Number of Tests Performed		Cumulative Number of Tests Performed	int
308	50	COVID-19 vaccine dose 1 administered as percent of age group		Administered_Dose1_pct_agegroup	float
311	50	Booster doses total for age group		Booster_Doses_Yes	int
317	51	Patients Currently Hospitalized		Patients Currently Hospitalized	int
320	51	Total staffed beds		Total Staffed Beds	int
323	51	Total Staffed ICU Beds Currently Available		Total Staffed ICU Beds Currently Available	int
\.

--
-- Data for Name: model_framework; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_framework (name, version, semantics, schema_url) FROM stdin;
Petri Net	0.0.1	semantics_go_here	https://raw.githubusercontent.com/DARPA-ASKEM/Model-Representations/petrinet_v0.2/petrinet/petrinet_schema.json
\.

--
-- Data for Name: model_runtime; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_runtime (id, "timestamp", name, "left", "right") FROM stdin;
\.


--
-- Data for Name: ontology_concept; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.ontology_concept (id, curie, type, object_id, status) FROM stdin;
11	ido:0000512	models	1	obj
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project (id, name, description, "timestamp", active, username) FROM stdin;
1	My Project	First project in TDS	2023-05-12 14:58:36.649427	t	Adam Smith
\.


--
-- Data for Name: project_asset; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project_asset (id, project_id, resource_id, resource_type, external_ref) FROM stdin;
2	1	1	models	\N
3	1	1	model_configurations	\N
4	1	1	datasets	\N
5	1	1	simulations	\N
6	1	2	datasets	\N
7	1	2	simulations	\N
8	1	3	datasets	\N
9	1	3	simulations	\N
10	1	4	datasets	\N
11	1	4	simulations	\N
12	1	5	datasets	\N
13	1	5	simulations	\N
14	1	6	datasets	\N
15	1	6	simulations	\N
16	1	7	datasets	\N
17	1	7	simulations	\N
18	1	8	datasets	\N
19	1	8	simulations	\N
20	1	9	datasets	\N
21	1	9	simulations	\N
22	1	10	datasets	\N
23	1	10	simulations	\N
24	1	11	datasets	\N
25	1	11	simulations	\N
26	1	1	publications	\N
29	1	2	models	\N
30	1	2	model_configurations	\N
31	1	12	datasets	\N
32	1	12	simulations	\N
33	1	13	datasets	\N
34	1	13	simulations	\N
35	1	14	datasets	\N
36	1	14	simulations	\N
37	1	15	datasets	\N
38	1	15	simulations	\N
39	1	16	datasets	\N
40	1	16	simulations	\N
41	1	17	datasets	\N
42	1	17	simulations	\N
43	1	18	datasets	\N
44	1	18	simulations	\N
45	1	19	datasets	\N
46	1	19	simulations	\N
47	1	20	datasets	\N
48	1	20	simulations	\N
49	1	21	datasets	\N
50	1	21	simulations	\N
51	1	22	datasets	\N
52	1	22	simulations	\N
55	1	3	models	\N
56	1	3	model_configurations	\N
57	1	23	datasets	\N
58	1	23	simulations	\N
59	1	24	datasets	\N
60	1	24	simulations	\N
61	1	25	datasets	\N
62	1	25	simulations	\N
63	1	26	datasets	\N
64	1	26	simulations	\N
65	1	27	datasets	\N
66	1	27	simulations	\N
67	1	28	datasets	\N
68	1	28	simulations	\N
69	1	29	datasets	\N
70	1	29	simulations	\N
71	1	30	datasets	\N
72	1	30	simulations	\N
73	1	31	datasets	\N
74	1	31	simulations	\N
75	1	32	datasets	\N
76	1	32	simulations	\N
77	1	33	datasets	\N
78	1	33	simulations	\N
79	1	2	publications	\N
82	1	4	models	\N
83	1	4	model_configurations	\N
84	1	34	datasets	\N
85	1	34	simulations	\N
86	1	35	datasets	\N
87	1	35	simulations	\N
88	1	36	datasets	\N
89	1	36	simulations	\N
90	1	37	datasets	\N
91	1	37	simulations	\N
92	1	38	datasets	\N
93	1	38	simulations	\N
94	1	39	datasets	\N
95	1	39	simulations	\N
96	1	40	datasets	\N
97	1	40	simulations	\N
98	1	41	datasets	\N
99	1	41	simulations	\N
100	1	42	datasets	\N
101	1	42	simulations	\N
102	1	43	datasets	\N
103	1	44	datasets	\N
104	1	45	datasets	\N
105	1	46	datasets	\N
106	1	47	datasets	\N
107	1	48	datasets	\N
108	1	49	datasets	\N
109	1	50	datasets	\N
110	1	51	datasets	\N
111	1	52	datasets	\N
\.


--
-- Data for Name: provenance; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.provenance (id, "timestamp", relation_type, "left", left_type, "right", right_type, user_id, concept) FROM stdin;
12	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	Model	1	.
13	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Model	1	ido:0000512
14	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Model	1	ido:0000514
15	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Model	1	ido:0000592
16	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Model	1	apollosv:00000154
17	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Model	1	ido:0000511
18	2023-05-12 14:58:36.644108	USES	1	ModelConfiguration	1	Model	1	.
19	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Dataset	1	ido:0000512
20	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Dataset	1	ido:0000514
21	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Dataset	1	ido:0000592
22	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Dataset	1	apollosv:00000154
23	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Dataset	1	ido:0000511
24	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
25	2023-05-12 14:58:36.644108	GENERATED_BY	1	Simulation	1	ModelConfiguration	1	.
26	2023-05-12 14:58:36.644108	REINTERPRETS	1	Dataset	1	Simulation	1	.
27	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	Simulation	1	.
28	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Dataset	1	ido:0000512
29	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Dataset	1	ido:0000514
30	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Dataset	1	ido:0000592
31	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Dataset	1	apollosv:00000154
32	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Dataset	1	ido:0000511
33	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
34	2023-05-12 14:58:36.644108	GENERATED_BY	2	Simulation	1	ModelConfiguration	1	.
35	2023-05-12 14:58:36.644108	REINTERPRETS	2	Dataset	2	Simulation	1	.
36	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	Simulation	1	.
37	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Dataset	1	ido:0000512
38	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Dataset	1	ido:0000514
39	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Dataset	1	ido:0000592
40	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Dataset	1	apollosv:00000154
41	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Dataset	1	ido:0000511
42	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
43	2023-05-12 14:58:36.644108	GENERATED_BY	3	Simulation	1	ModelConfiguration	1	.
44	2023-05-12 14:58:36.644108	REINTERPRETS	3	Dataset	3	Simulation	1	.
45	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	Simulation	1	.
46	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Dataset	1	ido:0000512
47	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Dataset	1	ido:0000514
48	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Dataset	1	ido:0000592
49	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Dataset	1	apollosv:00000154
50	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Dataset	1	ido:0000511
51	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
52	2023-05-12 14:58:36.644108	GENERATED_BY	4	Simulation	1	ModelConfiguration	1	.
53	2023-05-12 14:58:36.644108	REINTERPRETS	4	Dataset	4	Simulation	1	.
54	2023-05-12 14:58:36.644108	CONTAINS	1	Project	4	Simulation	1	.
55	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	5	Dataset	1	ido:0000512
56	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	5	Dataset	1	ido:0000514
57	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	5	Dataset	1	ido:0000592
58	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	5	Dataset	1	apollosv:00000154
59	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	5	Dataset	1	ido:0000511
60	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
61	2023-05-12 14:58:36.644108	GENERATED_BY	5	Simulation	1	ModelConfiguration	1	.
62	2023-05-12 14:58:36.644108	REINTERPRETS	5	Dataset	5	Simulation	1	.
63	2023-05-12 14:58:36.644108	CONTAINS	1	Project	5	Simulation	1	.
64	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	6	Dataset	1	ido:0000512
65	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	6	Dataset	1	ido:0000514
66	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	6	Dataset	1	ido:0000592
67	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	6	Dataset	1	apollosv:00000154
68	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	6	Dataset	1	ido:0000511
69	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
70	2023-05-12 14:58:36.644108	GENERATED_BY	6	Simulation	1	ModelConfiguration	1	.
71	2023-05-12 14:58:36.644108	REINTERPRETS	6	Dataset	6	Simulation	1	.
72	2023-05-12 14:58:36.644108	CONTAINS	1	Project	6	Simulation	1	.
73	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	7	Dataset	1	ido:0000512
74	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	7	Dataset	1	ido:0000514
75	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	7	Dataset	1	ido:0000592
76	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	7	Dataset	1	apollosv:00000154
77	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	7	Dataset	1	ido:0000511
78	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
79	2023-05-12 14:58:36.644108	GENERATED_BY	7	Simulation	1	ModelConfiguration	1	.
80	2023-05-12 14:58:36.644108	REINTERPRETS	7	Dataset	7	Simulation	1	.
81	2023-05-12 14:58:36.644108	CONTAINS	1	Project	7	Simulation	1	.
82	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	8	Dataset	1	ido:0000512
83	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	8	Dataset	1	ido:0000514
84	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	8	Dataset	1	ido:0000592
85	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	8	Dataset	1	apollosv:00000154
86	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	8	Dataset	1	ido:0000511
87	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
88	2023-05-12 14:58:36.644108	GENERATED_BY	8	Simulation	1	ModelConfiguration	1	.
89	2023-05-12 14:58:36.644108	REINTERPRETS	8	Dataset	8	Simulation	1	.
90	2023-05-12 14:58:36.644108	CONTAINS	1	Project	8	Simulation	1	.
91	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	9	Dataset	1	ido:0000512
92	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	9	Dataset	1	ido:0000514
93	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	9	Dataset	1	ido:0000592
94	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	9	Dataset	1	apollosv:00000154
95	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	9	Dataset	1	ido:0000511
96	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
97	2023-05-12 14:58:36.644108	GENERATED_BY	9	Simulation	1	ModelConfiguration	1	.
98	2023-05-12 14:58:36.644108	REINTERPRETS	9	Dataset	9	Simulation	1	.
99	2023-05-12 14:58:36.644108	CONTAINS	1	Project	9	Simulation	1	.
100	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	10	Dataset	1	ido:0000512
108	2023-05-12 14:58:36.644108	CONTAINS	1	Project	10	Simulation	1	.
112	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	11	Dataset	1	apollosv:00000154
116	2023-05-12 14:58:36.644108	REINTERPRETS	11	Dataset	11	Simulation	1	.
121	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	Publication	1	.
135	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	Model	1	.
145	2023-05-12 14:58:36.644108	GENERATED_BY	12	Simulation	2	ModelConfiguration	1	.
152	2023-05-12 14:58:36.644108	GENERATED_BY	13	Simulation	2	ModelConfiguration	1	.
159	2023-05-12 14:58:36.644108	GENERATED_BY	14	Simulation	2	ModelConfiguration	1	.
166	2023-05-12 14:58:36.644108	GENERATED_BY	15	Simulation	2	ModelConfiguration	1	.
173	2023-05-12 14:58:36.644108	GENERATED_BY	16	Simulation	2	ModelConfiguration	1	.
180	2023-05-12 14:58:36.644108	GENERATED_BY	17	Simulation	2	ModelConfiguration	1	.
187	2023-05-12 14:58:36.644108	GENERATED_BY	18	Simulation	2	ModelConfiguration	1	.
194	2023-05-12 14:58:36.644108	GENERATED_BY	19	Simulation	2	ModelConfiguration	1	.
201	2023-05-12 14:58:36.644108	GENERATED_BY	20	Simulation	2	ModelConfiguration	1	.
208	2023-05-12 14:58:36.644108	GENERATED_BY	21	Simulation	2	ModelConfiguration	1	.
215	2023-05-12 14:58:36.644108	GENERATED_BY	22	Simulation	2	ModelConfiguration	1	.
221	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	Publication	1	.
235	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	Model	1	.
241	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	23	Dataset	1	ido:0000592
254	2023-05-12 14:58:36.644108	CONTAINS	1	Project	24	Simulation	1	.
256	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	25	Dataset	1	ido:0000511
260	2023-05-12 14:58:36.644108	REINTERPRETS	25	Dataset	25	Simulation	1	.
262	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	26	Dataset	1	ido:0000592
275	2023-05-12 14:58:36.644108	CONTAINS	1	Project	27	Simulation	1	.
277	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	28	Dataset	1	ido:0000511
281	2023-05-12 14:58:36.644108	REINTERPRETS	28	Dataset	28	Simulation	1	.
283	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	29	Dataset	1	ido:0000592
296	2023-05-12 14:58:36.644108	CONTAINS	1	Project	30	Simulation	1	.
301	2023-05-12 14:58:36.644108	GENERATED_BY	31	Simulation	3	ModelConfiguration	1	.
101	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	10	Dataset	1	ido:0000514
106	2023-05-12 14:58:36.644108	GENERATED_BY	10	Simulation	1	ModelConfiguration	1	.
109	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	11	Dataset	1	ido:0000512
117	2023-05-12 14:58:36.644108	CONTAINS	1	Project	11	Simulation	1	.
118	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000592
141	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	12	Dataset	1	ido:0000592
154	2023-05-12 14:58:36.644108	CONTAINS	1	Project	13	Simulation	1	.
155	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	14	Dataset	1	ido:0000592
168	2023-05-12 14:58:36.644108	CONTAINS	1	Project	15	Simulation	1	.
169	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	16	Dataset	1	ido:0000592
182	2023-05-12 14:58:36.644108	CONTAINS	1	Project	17	Simulation	1	.
183	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	18	Dataset	1	ido:0000592
196	2023-05-12 14:58:36.644108	CONTAINS	1	Project	19	Simulation	1	.
197	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	20	Dataset	1	ido:0000592
210	2023-05-12 14:58:36.644108	CONTAINS	1	Project	21	Simulation	1	.
211	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	22	Dataset	1	ido:0000592
218	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000592
245	2023-05-12 14:58:36.644108	GENERATED_BY	23	Simulation	3	ModelConfiguration	1	.
250	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	24	Dataset	1	ido:0000514
251	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
261	2023-05-12 14:58:36.644108	CONTAINS	1	Project	25	Simulation	1	.
268	2023-05-12 14:58:36.644108	CONTAINS	1	Project	26	Simulation	1	.
273	2023-05-12 14:58:36.644108	GENERATED_BY	27	Simulation	3	ModelConfiguration	1	.
280	2023-05-12 14:58:36.644108	GENERATED_BY	28	Simulation	3	ModelConfiguration	1	.
284	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	29	Dataset	1	ido:0000511
288	2023-05-12 14:58:36.644108	REINTERPRETS	29	Dataset	29	Simulation	1	.
291	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	30	Dataset	1	ido:0000511
295	2023-05-12 14:58:36.644108	REINTERPRETS	30	Dataset	30	Simulation	1	.
298	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	31	Dataset	1	ido:0000511
302	2023-05-12 14:58:36.644108	REINTERPRETS	31	Dataset	31	Simulation	1	.
102	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	10	Dataset	1	ido:0000592
110	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	11	Dataset	1	ido:0000514
115	2023-05-12 14:58:36.644108	GENERATED_BY	11	Simulation	1	ModelConfiguration	1	.
119	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000511
137	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Model	1	ido:0000592
143	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	12	Dataset	1	ido:0000514
144	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
149	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	13	Dataset	1	ido:0000511
153	2023-05-12 14:58:36.644108	REINTERPRETS	13	Dataset	13	Simulation	1	.
157	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	14	Dataset	1	ido:0000514
158	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
163	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	15	Dataset	1	ido:0000511
167	2023-05-12 14:58:36.644108	REINTERPRETS	15	Dataset	15	Simulation	1	.
171	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	16	Dataset	1	ido:0000514
172	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
177	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	17	Dataset	1	ido:0000511
181	2023-05-12 14:58:36.644108	REINTERPRETS	17	Dataset	17	Simulation	1	.
185	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	18	Dataset	1	ido:0000514
186	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
191	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	19	Dataset	1	ido:0000511
195	2023-05-12 14:58:36.644108	REINTERPRETS	19	Dataset	19	Simulation	1	.
199	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	20	Dataset	1	ido:0000514
200	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
205	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	21	Dataset	1	ido:0000511
209	2023-05-12 14:58:36.644108	REINTERPRETS	21	Dataset	21	Simulation	1	.
213	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	22	Dataset	1	ido:0000514
214	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
239	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Model	1	ido:0000514
240	2023-05-12 14:58:36.644108	USES	3	ModelConfiguration	3	Model	1	.
243	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	23	Dataset	1	ido:0000514
244	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
248	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	24	Dataset	1	ido:0000592
255	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	25	Dataset	1	ido:0000592
266	2023-05-12 14:58:36.644108	GENERATED_BY	26	Simulation	3	ModelConfiguration	1	.
271	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	27	Dataset	1	ido:0000514
272	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
282	2023-05-12 14:58:36.644108	CONTAINS	1	Project	28	Simulation	1	.
289	2023-05-12 14:58:36.644108	CONTAINS	1	Project	29	Simulation	1	.
294	2023-05-12 14:58:36.644108	GENERATED_BY	30	Simulation	3	ModelConfiguration	1	.
299	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	31	Dataset	1	ido:0000514
300	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
103	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	10	Dataset	1	apollosv:00000154
107	2023-05-12 14:58:36.644108	REINTERPRETS	10	Dataset	10	Simulation	1	.
111	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	11	Dataset	1	ido:0000592
139	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Model	1	ido:0000514
142	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	12	Dataset	1	ido:0000511
146	2023-05-12 14:58:36.644108	REINTERPRETS	12	Dataset	12	Simulation	1	.
150	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	13	Dataset	1	ido:0000514
151	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
156	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	14	Dataset	1	ido:0000511
160	2023-05-12 14:58:36.644108	REINTERPRETS	14	Dataset	14	Simulation	1	.
164	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	15	Dataset	1	ido:0000514
165	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
170	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	16	Dataset	1	ido:0000511
174	2023-05-12 14:58:36.644108	REINTERPRETS	16	Dataset	16	Simulation	1	.
178	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	17	Dataset	1	ido:0000514
179	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
184	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	18	Dataset	1	ido:0000511
188	2023-05-12 14:58:36.644108	REINTERPRETS	18	Dataset	18	Simulation	1	.
192	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	19	Dataset	1	ido:0000514
193	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
198	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	20	Dataset	1	ido:0000511
202	2023-05-12 14:58:36.644108	REINTERPRETS	20	Dataset	20	Simulation	1	.
206	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	21	Dataset	1	ido:0000514
207	2023-05-12 14:58:36.644108	CONTAINS	1	Project	2	ModelConfiguration	1	.
212	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	22	Dataset	1	ido:0000511
216	2023-05-12 14:58:36.644108	REINTERPRETS	22	Dataset	22	Simulation	1	.
220	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000514
238	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Model	1	ido:0000511
247	2023-05-12 14:58:36.644108	CONTAINS	1	Project	23	Simulation	1	.
252	2023-05-12 14:58:36.644108	GENERATED_BY	24	Simulation	3	ModelConfiguration	1	.
259	2023-05-12 14:58:36.644108	GENERATED_BY	25	Simulation	3	ModelConfiguration	1	.
263	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	26	Dataset	1	ido:0000511
267	2023-05-12 14:58:36.644108	REINTERPRETS	26	Dataset	26	Simulation	1	.
270	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	27	Dataset	1	ido:0000511
274	2023-05-12 14:58:36.644108	REINTERPRETS	27	Dataset	27	Simulation	1	.
278	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	28	Dataset	1	ido:0000514
279	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
285	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	29	Dataset	1	ido:0000514
286	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
290	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	30	Dataset	1	ido:0000592
303	2023-05-12 14:58:36.644108	CONTAINS	1	Project	31	Simulation	1	.
104	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	10	Dataset	1	ido:0000511
105	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
113	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	11	Dataset	1	ido:0000511
114	2023-05-12 14:58:36.644108	CONTAINS	1	Project	1	ModelConfiguration	1	.
120	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000514
138	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Model	1	ido:0000511
140	2023-05-12 14:58:36.644108	USES	2	ModelConfiguration	2	Model	1	.
147	2023-05-12 14:58:36.644108	CONTAINS	1	Project	12	Simulation	1	.
148	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	13	Dataset	1	ido:0000592
161	2023-05-12 14:58:36.644108	CONTAINS	1	Project	14	Simulation	1	.
162	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	15	Dataset	1	ido:0000592
175	2023-05-12 14:58:36.644108	CONTAINS	1	Project	16	Simulation	1	.
176	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	17	Dataset	1	ido:0000592
189	2023-05-12 14:58:36.644108	CONTAINS	1	Project	18	Simulation	1	.
190	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	19	Dataset	1	ido:0000592
203	2023-05-12 14:58:36.644108	CONTAINS	1	Project	20	Simulation	1	.
204	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	21	Dataset	1	ido:0000592
217	2023-05-12 14:58:36.644108	CONTAINS	1	Project	22	Simulation	1	.
219	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	1	Publication	1	ido:0000511
237	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	3	Model	1	ido:0000592
242	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	23	Dataset	1	ido:0000511
246	2023-05-12 14:58:36.644108	REINTERPRETS	23	Dataset	23	Simulation	1	.
249	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	24	Dataset	1	ido:0000511
253	2023-05-12 14:58:36.644108	REINTERPRETS	24	Dataset	24	Simulation	1	.
257	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	25	Dataset	1	ido:0000514
258	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
264	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	26	Dataset	1	ido:0000514
265	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
269	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	27	Dataset	1	ido:0000592
276	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	28	Dataset	1	ido:0000592
287	2023-05-12 14:58:36.644108	GENERATED_BY	29	Simulation	3	ModelConfiguration	1	.
292	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	30	Dataset	1	ido:0000514
293	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
297	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	31	Dataset	1	ido:0000592
304	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	32	Dataset	1	ido:0000592
305	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	32	Dataset	1	ido:0000511
306	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	32	Dataset	1	ido:0000514
307	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
308	2023-05-12 14:58:36.644108	GENERATED_BY	32	Simulation	3	ModelConfiguration	1	.
309	2023-05-12 14:58:36.644108	REINTERPRETS	32	Dataset	32	Simulation	1	.
310	2023-05-12 14:58:36.644108	CONTAINS	1	Project	32	Simulation	1	.
311	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	33	Dataset	1	ido:0000592
312	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	33	Dataset	1	ido:0000511
313	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	33	Dataset	1	ido:0000514
314	2023-05-12 14:58:36.644108	CONTAINS	1	Project	3	ModelConfiguration	1	.
315	2023-05-12 14:58:36.644108	GENERATED_BY	33	Simulation	3	ModelConfiguration	1	.
316	2023-05-12 14:58:36.644108	REINTERPRETS	33	Dataset	33	Simulation	1	.
317	2023-05-12 14:58:36.644108	CONTAINS	1	Project	33	Simulation	1	.
318	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Publication	1	ido:0000573
319	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Publication	1	ncit:C28554
320	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Publication	1	ido:0000511
321	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	2	Publication	1	ido:0000514
333	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Model	1	ido:0000573
334	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Model	1	ncit:C28554
335	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Model	1	ido:0000511
336	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	4	Model	1	ido:0000514
337	2023-05-12 14:58:36.644108	USES	4	ModelConfiguration	4	Model	1	.
338	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	34	Dataset	1	ido:0000573
339	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	34	Dataset	1	ncit:C28554
340	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	34	Dataset	1	ido:0000511
341	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	34	Dataset	1	ido:0000514
342	2023-05-12 14:58:36.644108	GENERATED_BY	34	Simulation	4	ModelConfiguration	1	.
343	2023-05-12 14:58:36.644108	REINTERPRETS	34	Dataset	34	Simulation	1	.
344	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	35	Dataset	1	ido:0000573
345	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	35	Dataset	1	ncit:C28554
346	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	35	Dataset	1	ido:0000511
347	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	35	Dataset	1	ido:0000514
348	2023-05-12 14:58:36.644108	GENERATED_BY	35	Simulation	4	ModelConfiguration	1	.
349	2023-05-12 14:58:36.644108	REINTERPRETS	35	Dataset	35	Simulation	1	.
350	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	36	Dataset	1	ido:0000573
351	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	36	Dataset	1	ncit:C28554
352	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	36	Dataset	1	ido:0000511
353	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	36	Dataset	1	ido:0000514
354	2023-05-12 14:58:36.644108	GENERATED_BY	36	Simulation	4	ModelConfiguration	1	.
355	2023-05-12 14:58:36.644108	REINTERPRETS	36	Dataset	36	Simulation	1	.
356	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	37	Dataset	1	ido:0000573
357	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	37	Dataset	1	ncit:C28554
358	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	37	Dataset	1	ido:0000511
359	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	37	Dataset	1	ido:0000514
360	2023-05-12 14:58:36.644108	GENERATED_BY	37	Simulation	4	ModelConfiguration	1	.
361	2023-05-12 14:58:36.644108	REINTERPRETS	37	Dataset	37	Simulation	1	.
362	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	38	Dataset	1	ido:0000573
363	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	38	Dataset	1	ncit:C28554
365	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	38	Dataset	1	ido:0000514
367	2023-05-12 14:58:36.644108	REINTERPRETS	38	Dataset	38	Simulation	1	.
372	2023-05-12 14:58:36.644108	GENERATED_BY	39	Simulation	4	ModelConfiguration	1	.
364	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	38	Dataset	1	ido:0000511
368	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	39	Dataset	1	ido:0000573
370	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	39	Dataset	1	ido:0000511
374	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	40	Dataset	1	ido:0000573
376	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	40	Dataset	1	ido:0000511
380	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	41	Dataset	1	ido:0000573
382	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	41	Dataset	1	ido:0000511
386	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	42	Dataset	1	ido:0000573
388	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	42	Dataset	1	ido:0000511
366	2023-05-12 14:58:36.644108	GENERATED_BY	38	Simulation	4	ModelConfiguration	1	.
387	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	42	Dataset	1	ncit:C28554
389	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	42	Dataset	1	ido:0000514
391	2023-05-12 14:58:36.644108	REINTERPRETS	42	Dataset	42	Simulation	1	.
369	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	39	Dataset	1	ncit:C28554
371	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	39	Dataset	1	ido:0000514
373	2023-05-12 14:58:36.644108	REINTERPRETS	39	Dataset	39	Simulation	1	.
378	2023-05-12 14:58:36.644108	GENERATED_BY	40	Simulation	4	ModelConfiguration	1	.
375	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	40	Dataset	1	ncit:C28554
377	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	40	Dataset	1	ido:0000514
379	2023-05-12 14:58:36.644108	REINTERPRETS	40	Dataset	40	Simulation	1	.
384	2023-05-12 14:58:36.644108	GENERATED_BY	41	Simulation	4	ModelConfiguration	1	.
381	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	41	Dataset	1	ncit:C28554
383	2023-05-12 14:58:36.644108	IS_CONCEPT_OF	1	Concept	41	Dataset	1	ido:0000514
385	2023-05-12 14:58:36.644108	REINTERPRETS	41	Dataset	41	Simulation	1	.
390	2023-05-12 14:58:36.644108	GENERATED_BY	42	Simulation	4	ModelConfiguration	1	.
\.


--
-- Data for Name: qualifier; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier (id, dataset_id, description, name, value_type) FROM stdin;
1	1	Timestep feature qualifier	timestep_qualifier	float
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
24	24	Timestep feature qualifier	timestep_qualifier	float
25	25	Timestep feature qualifier	timestep_qualifier	float
26	26	Timestep feature qualifier	timestep_qualifier	float
27	27	Timestep feature qualifier	timestep_qualifier	float
28	28	Timestep feature qualifier	timestep_qualifier	float
29	29	Timestep feature qualifier	timestep_qualifier	float
30	30	Timestep feature qualifier	timestep_qualifier	float
31	31	Timestep feature qualifier	timestep_qualifier	float
32	32	Timestep feature qualifier	timestep_qualifier	float
33	33	Timestep feature qualifier	timestep_qualifier	float
34	34	Timestep feature qualifier	timestep_qualifier	float
35	35	Timestep feature qualifier	timestep_qualifier	float
36	36	Timestep feature qualifier	timestep_qualifier	float
37	37	Timestep feature qualifier	timestep_qualifier	float
38	38	Timestep feature qualifier	timestep_qualifier	float
39	39	Timestep feature qualifier	timestep_qualifier	float
40	40	Timestep feature qualifier	timestep_qualifier	float
41	41	Timestep feature qualifier	timestep_qualifier	float
42	42	Timestep feature qualifier	timestep_qualifier	float
43	43	Date	Date	str
44	43	location	country	str
45	43	location	admin1	str
46	43	location	admin2	str
47	43	location	admin3	str
48	43	location	lat	str
49	43	location	lng	str
50	44	Three-digit numeric NAICS value for retail subsector code	naics	int
51	44	Month	Date	str
52	44	location	country	str
53	44	location	admin1	str
54	44	location	admin2	str
55	44	location	admin3	str
56	44	location	lat	str
57	44	location	lng	str
58	45	Age group	AgeGroupVacc	str
59	45	Date	Date Administered	str
60	45	location	country	str
61	45	location	admin1	str
62	45	location	admin2	str
63	45	location	admin3	str
64	45	location	lat	str
65	45	location	lng	str
66	46	COVID-19 variant	variant	str
67	46	model type	modeltype	str
68	46	date	week_ending	str
69	46	location	country	str
70	46	location	admin1	str
71	46	location	admin2	str
72	46	location	admin3	str
73	46	location	lat	str
74	46	location	lng	str
75	47	geography type	Geography	str
76	47	test date	Test Date	str
77	47	location	country	str
78	47	location	admin1	str
79	47	location	admin2	str
80	47	location	admin3	str
81	47	location	lat	str
82	47	location	lng	str
83	48	date	Date	str
84	48	location	country	str
85	48	location	admin1	str
86	48	location	admin2	str
87	48	location	admin3	str
88	48	location	lat	str
89	48	location	lng	str
90	49	year	Year	str
91	49	location	country	str
92	49	location	admin1	str
93	49	location	admin2	str
94	49	location	admin3	str
95	49	location	lat	str
96	49	location	lng	str
97	50	Demographic category	Demographic_category	str
98	50	date	Date	str
99	50	location	country	str
100	50	location	admin1	str
101	50	location	admin2	str
102	50	location	admin3	str
103	50	location	lat	str
104	50	location	lng	str
105	51	facility name	Facility Name	str
106	51	Date	As of Date	str
107	51	location	country	str
108	51	location	admin1	str
109	51	location	admin2	str
110	51	location	admin3	str
111	51	location	lat	str
112	51	location	lng	str
113	52	date	Week Ending	str
114	52	location	country	str
115	52	location	admin1	str
116	52	location	admin2	str
117	52	location	admin3	str
118	52	location	lat	str
119	52	location	lng	str
\.


--
-- Data for Name: qualifier_xref; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier_xref (id, qualifier_id, feature_id) FROM stdin;
1	1	1
2	1	2
3	1	4
4	1	5
5	1	6
6	1	7
7	1	8
8	1	9
9	2	10
10	2	11
11	2	13
12	2	14
13	2	15
14	2	16
15	2	17
16	2	18
17	3	19
18	3	20
19	3	22
20	3	23
21	3	24
22	3	25
23	3	26
24	3	27
25	4	28
26	4	29
27	4	31
28	4	32
29	4	33
30	4	34
31	4	35
32	4	36
33	5	37
34	5	38
35	5	40
36	5	41
37	5	42
38	5	43
39	5	44
40	5	45
41	6	46
42	6	47
43	6	49
44	6	50
45	6	51
46	6	52
47	6	53
48	6	54
49	7	55
50	7	56
51	7	58
52	7	59
53	7	60
54	7	61
55	7	62
56	7	63
57	8	64
58	8	65
59	8	67
60	8	68
61	8	69
62	8	70
63	8	71
64	8	72
65	9	73
66	9	74
67	9	76
68	9	77
69	9	78
70	9	79
71	9	80
72	9	81
73	10	82
74	10	83
75	10	85
76	10	86
77	10	87
78	10	88
79	10	89
80	10	90
81	11	91
82	11	92
83	11	94
84	11	95
85	11	96
86	11	97
87	11	98
88	11	99
89	12	100
90	12	101
91	12	103
92	13	104
93	13	105
94	13	107
95	14	108
96	14	109
97	14	111
98	15	112
99	15	113
100	15	115
101	16	116
102	16	117
103	16	119
104	17	120
105	17	121
106	17	123
107	18	124
108	18	125
109	18	127
110	19	128
111	19	129
112	19	131
113	20	132
114	20	133
115	20	135
116	21	136
117	21	137
118	21	139
119	22	140
120	22	141
121	22	143
122	23	144
123	23	145
124	23	146
125	23	148
126	23	149
127	24	150
128	24	151
129	24	152
130	24	154
131	24	155
132	25	156
133	25	157
134	25	158
135	25	160
136	25	161
137	26	162
138	26	163
139	26	164
140	26	166
141	26	167
142	27	168
143	27	169
144	27	170
145	27	172
146	27	173
147	28	174
148	28	175
149	28	176
150	28	178
151	28	179
152	29	180
153	29	181
154	29	182
155	29	184
156	29	185
157	30	186
158	30	187
159	30	188
160	30	190
161	30	191
162	31	192
163	31	193
164	31	194
165	31	196
166	31	197
167	32	198
168	32	199
169	32	200
170	32	202
171	32	203
172	33	204
173	33	205
174	33	206
175	33	208
176	33	209
177	34	210
178	34	211
179	34	212
180	34	213
181	34	214
182	34	215
183	34	217
184	34	218
185	35	219
186	35	220
191	35	226
196	36	231
203	37	239
208	37	245
210	38	247
215	38	253
220	39	258
227	40	266
232	40	272
237	41	277
265	58	294
273	61	293
277	62	294
285	65	293
288	66	296
292	67	296
300	70	296
304	71	297
312	74	296
324	76	303
328	77	302
339	79	303
343	80	302
354	82	303
358	86	304
380	97	311
385	97	316
389	98	310
394	98	315
410	100	311
415	100	316
419	101	310
424	101	315
440	103	311
445	103	316
449	104	310
454	104	315
456	105	317
461	105	322
474	107	321
478	108	318
483	108	323
487	109	320
491	110	317
496	110	322
509	112	321
513	113	325
516	115	324
523	118	325
187	35	221
192	35	227
197	36	232
209	38	246
214	38	251
217	39	255
222	39	260
225	40	264
230	40	269
233	41	273
238	41	278
241	42	282
246	42	287
252	46	291
256	50	292
260	54	292
267	59	293
271	60	294
279	63	293
283	64	294
293	67	298
299	69	298
305	71	298
311	73	298
318	75	302
329	77	303
333	78	302
344	80	303
348	81	302
365	91	306
368	93	305
375	96	306
376	97	307
381	97	312
388	98	309
393	98	314
397	99	308
402	99	313
406	100	307
411	100	312
418	101	309
423	101	314
427	102	308
432	102	313
436	103	307
441	103	312
448	104	309
453	104	314
460	105	321
464	106	318
469	106	323
473	107	320
477	108	317
482	108	322
495	110	321
499	111	318
504	111	323
508	112	320
512	113	324
519	116	325
522	118	324
188	35	222
195	36	230
200	36	236
205	37	241
213	38	250
226	40	265
231	40	271
236	41	276
243	42	284
248	42	290
250	44	291
254	48	291
258	52	292
262	56	292
270	60	293
274	61	294
282	64	293
286	65	294
291	67	297
295	68	297
303	71	296
307	72	297
319	75	303
323	76	302
334	78	303
338	79	302
349	81	303
353	82	302
364	91	305
371	94	306
374	96	305
378	97	309
383	97	314
387	98	308
392	98	313
396	99	307
401	99	312
408	100	309
413	100	314
417	101	308
422	101	313
426	102	307
431	102	312
438	103	309
443	103	314
447	104	308
452	104	313
459	105	320
463	106	317
468	106	322
481	108	321
485	109	318
490	109	323
494	110	320
498	111	317
503	111	322
515	114	325
518	116	324
525	119	325
189	35	223
202	37	238
207	37	244
211	38	248
216	38	254
221	39	259
234	41	274
239	41	280
244	42	285
264	58	293
268	59	294
276	62	293
280	63	294
290	66	298
296	68	298
302	70	298
308	72	298
314	74	298
317	75	301
321	76	300
325	77	299
332	78	301
336	79	300
340	80	299
347	81	301
351	82	300
355	83	304
359	87	304
363	90	306
366	92	305
373	95	306
390	98	311
395	98	316
399	99	310
404	99	315
420	101	311
425	101	316
429	102	310
434	102	315
450	104	311
455	104	316
457	105	318
462	105	323
466	106	320
470	107	317
475	107	322
488	109	321
492	110	318
497	110	323
501	111	320
505	112	317
510	112	322
517	115	325
520	117	324
190	35	224
193	36	228
198	36	233
201	37	237
206	37	242
212	38	249
219	39	257
224	39	263
229	40	268
242	42	283
247	42	289
251	45	291
255	49	291
259	53	292
263	57	292
266	58	295
272	60	295
278	62	295
284	64	295
289	66	297
297	69	296
301	70	297
309	73	296
313	74	297
316	75	300
320	76	299
327	77	301
331	78	300
335	79	299
342	80	301
346	81	300
350	82	299
356	84	304
360	88	304
362	90	305
369	93	306
372	95	305
377	97	308
382	97	313
386	98	307
391	98	312
398	99	309
403	99	314
407	100	308
412	100	313
416	101	307
421	101	312
428	102	309
433	102	314
437	103	308
442	103	313
446	104	307
451	104	312
467	106	321
471	107	318
476	107	323
480	108	320
484	109	317
489	109	322
502	111	321
506	112	318
511	112	323
514	114	324
521	117	325
524	119	324
194	36	229
199	36	235
204	37	240
218	39	256
223	39	262
228	40	267
235	41	275
240	41	281
245	42	286
249	43	291
253	47	291
257	51	292
261	55	292
269	59	295
275	61	295
281	63	295
287	65	295
294	68	296
298	69	297
306	72	296
310	73	297
315	75	299
322	76	301
326	77	300
330	78	299
337	79	301
341	80	300
345	81	299
352	82	301
357	85	304
361	89	304
367	92	306
370	94	305
379	97	310
384	97	315
400	99	311
405	99	316
409	100	310
414	100	315
430	102	311
435	102	316
439	103	310
444	103	315
458	105	319
465	106	319
472	107	319
479	108	319
486	109	319
493	110	319
500	111	319
507	112	319
\.

--
-- Data for Name: software; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.software (id, "timestamp", source, storage_uri) FROM stdin;
\.


--
-- Name: association_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.association_id_seq', 1, false);


--
-- Name: dataset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.dataset_id_seq', 52, true);


--
-- Name: extraction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.extraction_id_seq', 1, false);


--
-- Name: feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.feature_id_seq', 325, true);


--
-- Name: model_runtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_runtime_id_seq', 1, false);


--
-- Name: ontology_concept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.ontology_concept_id_seq', 12, true);


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.person_id_seq', 1, true);


--
-- Name: project_asset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_asset_id_seq', 111, true);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_id_seq', 1, true);


--
-- Name: provenance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.provenance_id_seq', 391, true);


--
-- Name: publication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.publication_id_seq', 2, true);


--
-- Name: qualifier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_id_seq', 119, true);


--
-- Name: qualifier_xref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_xref_id_seq', 525, true);


--
-- Name: software_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.software_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--
--- Data updates to facilitate basic flow.
-- delete from public.provenance where left_type  = 'Intermediate';
-- delete from public.provenance where right_type  = 'Intermediate';
-- delete from public.project_asset where resource_type  = 'intermediates';

update public.model_framework
set schema_url = 'https://raw.githubusercontent.com/DARPA-ASKEM/Model-Representations/petrinet_v0.2/petrinet/petrinet_schema.json'
where "name" = 'Petri Net';
