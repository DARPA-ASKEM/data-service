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
ido:0000592	immune population
ido:0000511	infected population
ido:0000514	susceptible population
ido:0000512	diseased population
apollosv:00000154	exposed population
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

COPY public.dataset (id, name, url, description, "timestamp", deprecated, sensitivity, quality, temporal_resolution, geospatial_resolution, annotations, maintainer, simulation_run) FROM stdin;
\.


--
-- Data for Name: publication; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.publication (id, xdd_uri, title) FROM stdin;
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
\.


--
-- Data for Name: intermediate; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.intermediate (id, "timestamp", source, type, content) FROM stdin;
1	2023-01-09 15:34:02.31213	mrepresentationa	bilayer	\\x7b2274656d706c61746573223a205b7b22726174655f6c6177223a2022452a532a62657461222c202274797065223a2022436f6e74726f6c6c6564436f6e76657273696f6e222c2022636f6e74726f6c6c6572223a207b226e616d65223a202245222c20226964656e74696669657273223a207b2261706f6c6c6f7376223a20223030303030313534227d2c2022636f6e74657874223a207b7d7d2c20227375626a656374223a207b226e616d65223a202253222c20226964656e74696669657273223a207b2269646f223a202230303030353134227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a202245222c20226964656e74696669657273223a207b2261706f6c6c6f7376223a20223030303030313534227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022452a64656c74615f31222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202245222c20226964656e74696669657273223a207b2261706f6c6c6f7376223a20223030303030313534227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022495f6173796d222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a4333383333227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022452a64656c74615f32222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202245222c20226964656e74696669657273223a207b2261706f6c6c6f7376223a20223030303030313534227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022495f6d696c64222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a433235323639227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022452a64656c74615f33222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a202245222c20226964656e74696669657273223a207b2261706f6c6c6f7376223a20223030303030313534227d2c2022636f6e74657874223a207b7d7d2c20226f7574636f6d65223a207b226e616d65223a2022495f686f7370222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a433235323639222c2022686f73706974616c697a6174696f6e5f737461747573223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022495f6173796d2a67616d6d615f31222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022495f6173796d222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a4333383333227d7d2c20226f7574636f6d65223a207b226e616d65223a202252222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022495f6d696c642a67616d6d615f32222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022495f6d696c64222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a433235323639227d7d2c20226f7574636f6d65223a207b226e616d65223a202252222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022495f686f73702a64656c74615f34222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022495f686f7370222c20226964656e74696669657273223a207b2269646f223a202230303030353131227d2c2022636f6e74657874223a207b22646973656173655f7365766572697479223a20226e6369743a433235323639222c2022686f73706974616c697a6174696f6e5f737461747573223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a2022525f686f7370222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b22686f73706974616c697a6174696f6e5f737461747573223a20226e6369743a433235313739227d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022525f686f73702a746175222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022525f686f7370222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b22686f73706974616c697a6174696f6e5f737461747573223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a202252222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d2c207b22726174655f6c6177223a2022525f686f73702a64656c74615f35222c202274797065223a20224e61747572616c436f6e76657273696f6e222c20227375626a656374223a207b226e616d65223a2022525f686f7370222c20226964656e74696669657273223a207b2269646f223a202230303030353932227d2c2022636f6e74657874223a207b22686f73706974616c697a6174696f6e5f737461747573223a20226e6369743a433235313739227d7d2c20226f7574636f6d65223a207b226e616d65223a202244222c20226964656e74696669657273223a207b2269646f223a202230303030353132227d2c2022636f6e74657874223a207b7d7d2c202270726f76656e616e6365223a205b5d7d5d7d
\.


--
-- Data for Name: model_framework; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_framework (name, version, semantics) FROM stdin;
Petri Net	0.0.1	semantics_go_here
\.


--
-- Data for Name: model_state; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_state (id, "timestamp", content) FROM stdin;
1	2023-01-09 15:34:06.231801	{"S": [{"sname": "S", "mira_ids": "[('identity', 'ido:0000514')]", "mira_context": "[]"}, {"sname": "E", "mira_ids": "[('identity', 'apollosv:00000154')]", "mira_context": "[]"}, {"sname": "I_asym", "mira_ids": "[('identity', 'ido:0000511')]", "mira_context": "[('disease_severity', 'ncit:C3833')]"}, {"sname": "I_mild", "mira_ids": "[('identity', 'ido:0000511')]", "mira_context": "[('disease_severity', 'ncit:C25269')]"}, {"sname": "I_hosp", "mira_ids": "[('identity', 'ido:0000511')]", "mira_context": "[('disease_severity', 'ncit:C25269'), ('hospitalization_status', 'ncit:C25179')]"}, {"sname": "R", "mira_ids": "[('identity', 'ido:0000592')]", "mira_context": "[]"}, {"sname": "R_hosp", "mira_ids": "[('identity', 'ido:0000592')]", "mira_context": "[('hospitalization_status', 'ncit:C25179')]"}, {"sname": "D", "mira_ids": "[('identity', 'ido:0000512')]", "mira_context": "[]"}], "T": [{"tname": "t1", "template_type": "ControlledConversion", "parameter_name": "beta", "parameter_value": 1.0}, {"tname": "t2", "template_type": "NaturalConversion", "parameter_name": "delta_1", "parameter_value": 1.0}, {"tname": "t3", "template_type": "NaturalConversion", "parameter_name": "delta_2", "parameter_value": 1.0}, {"tname": "t4", "template_type": "NaturalConversion", "parameter_name": "delta_3", "parameter_value": 1.0}, {"tname": "t5", "template_type": "NaturalConversion", "parameter_name": "gamma_1", "parameter_value": 1.0}, {"tname": "t6", "template_type": "NaturalConversion", "parameter_name": "gamma_2", "parameter_value": 1.0}, {"tname": "t7", "template_type": "NaturalConversion", "parameter_name": "delta_4", "parameter_value": 1.0}, {"tname": "t8", "template_type": "NaturalConversion", "parameter_name": "tau", "parameter_value": 1.0}, {"tname": "t9", "template_type": "NaturalConversion", "parameter_name": "delta_5", "parameter_value": 1.0}], "I": [{"is": 2, "it": 1}, {"is": 1, "it": 1}, {"is": 2, "it": 2}, {"is": 2, "it": 3}, {"is": 2, "it": 4}, {"is": 3, "it": 5}, {"is": 4, "it": 6}, {"is": 5, "it": 7}, {"is": 7, "it": 8}, {"is": 7, "it": 9}], "O": [{"os": 2, "ot": 1}, {"os": 2, "ot": 1}, {"os": 3, "ot": 2}, {"os": 4, "ot": 3}, {"os": 5, "ot": 4}, {"os": 6, "ot": 5}, {"os": 6, "ot": 6}, {"os": 7, "ot": 7}, {"os": 6, "ot": 8}, {"os": 8, "ot": 9}]}
\.


--
-- Data for Name: model_description; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_description (id, name, description, framework, "timestamp", state_id) FROM stdin;
1	Bucky	The JHUAPL-Bucky model is a COVID-19 metapopulation compartment model initially designed to estimate medium-term (on the order of weeks) case incidence and healthcare usage at the second administrative (admin-2, ADM2) level (counties in the United States; cities or districts in various countries). It is documented at https://docs.buckymodel.com/en/latest/.	Petri Net	2023-01-09 15:34:02.299607	1
\.


--
-- Data for Name: model_parameter; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.model_parameter (id, model_id, name, type, default_value, state_variable) FROM stdin;
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
1	ido:0000592	intermediates	1	obj
2	ido:0000511	intermediates	1	obj
3	ido:0000514	intermediates	1	obj
4	ido:0000512	intermediates	1	obj
5	apollosv:00000154	intermediates	1	obj
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project (id, name, description, "timestamp", active) FROM stdin;
1	My Project	First project in TDS	2023-01-09 15:34:02.313731	t
\.


--
-- Data for Name: project_asset; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.project_asset (id, project_id, resource_id, resource_type, external_ref) FROM stdin;
1	1	1	intermediates	\N
\.


--
-- Data for Name: provenance; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.provenance (id, "timestamp", relation_type, "left", left_type, "right", right_type, user_id) FROM stdin;
1	2023-01-09 15:34:02.309626	BEGINS_AT	1	Model	1	ModelRevision	\N
\.


--
-- Data for Name: qualifier; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier (id, dataset_id, description, name, value_type) FROM stdin;
\.


--
-- Data for Name: qualifier_xref; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.qualifier_xref (id, qualifier_id, feature_id) FROM stdin;
\.


--
-- Data for Name: simulation_plan; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_plan (id, model_id, simulator, query, content) FROM stdin;
\.


--
-- Data for Name: simulation_run; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_run (id, simulator_id, "timestamp", completed_at, success, dataset_id, description, response) FROM stdin;
\.


--
-- Data for Name: simulation_parameter; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY public.simulation_parameter (id, run_id, name, value, type) FROM stdin;
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

SELECT pg_catalog.setval('public.dataset_id_seq', 1, false);


--
-- Name: extraction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.extraction_id_seq', 1, false);


--
-- Name: feature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.feature_id_seq', 1, false);


--
-- Name: intermediate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.intermediate_id_seq', 1, true);


--
-- Name: model_description_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_description_id_seq', 1, true);


--
-- Name: model_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_parameter_id_seq', 1, false);


--
-- Name: model_runtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_runtime_id_seq', 1, false);


--
-- Name: model_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.model_state_id_seq', 1, true);


--
-- Name: ontology_concept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.ontology_concept_id_seq', 5, true);


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.person_id_seq', 1, true);


--
-- Name: project_asset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_asset_id_seq', 1, true);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.project_id_seq', 1, true);


--
-- Name: provenance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.provenance_id_seq', 1, true);


--
-- Name: publication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.publication_id_seq', 1, false);


--
-- Name: qualifier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_id_seq', 1, false);


--
-- Name: qualifier_xref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.qualifier_xref_id_seq', 1, false);


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
-- PostgreSQL database dump complete
--

