--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: country; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.country (
    cname character varying(50) NOT NULL,
    population bigint
);


ALTER TABLE public.country OWNER TO myuser;

--
-- Name: discover; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.discover (
    cname character varying(50) NOT NULL,
    disease_code character varying(50) NOT NULL,
    first_enc_date date
);


ALTER TABLE public.discover OWNER TO myuser;

--
-- Name: disease; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.disease (
    disease_code character varying(50) NOT NULL,
    pathogen character varying(20),
    description character varying(140),
    id integer
);


ALTER TABLE public.disease OWNER TO myuser;

--
-- Name: disease_type; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.disease_type (
    id integer NOT NULL,
    description character varying(140)
);


ALTER TABLE public.disease_type OWNER TO myuser;

--
-- Name: disease_type_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.disease_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.disease_type_id_seq OWNER TO myuser;

--
-- Name: disease_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.disease_type_id_seq OWNED BY public.disease_type.id;


--
-- Name: doctor; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.doctor (
    email character varying(60) NOT NULL,
    degree character varying(20)
);


ALTER TABLE public.doctor OWNER TO myuser;

--
-- Name: patient_disease; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.patient_disease (
    email character varying(60) NOT NULL,
    disease_code character varying(50) NOT NULL
);


ALTER TABLE public.patient_disease OWNER TO myuser;

--
-- Name: users; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.users (
    email character varying(60) NOT NULL,
    name character varying(30),
    surname character varying(40),
    salary integer,
    phone character varying(20),
    cname character varying(50)
);


ALTER TABLE public.users OWNER TO myuser;

--
-- Name: patient_diseases_view; Type: VIEW; Schema: public; Owner: myuser
--

CREATE VIEW public.patient_diseases_view AS
 SELECT u.name,
    u.surname,
    pd.disease_code
   FROM (public.users u
     JOIN public.patient_disease pd ON (((u.email)::text = (pd.email)::text)));


ALTER TABLE public.patient_diseases_view OWNER TO myuser;

--
-- Name: patients; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.patients (
    email character varying(60) NOT NULL
);


ALTER TABLE public.patients OWNER TO myuser;

--
-- Name: public_servant; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.public_servant (
    email character varying(60) NOT NULL,
    department character varying(50)
);


ALTER TABLE public.public_servant OWNER TO myuser;

--
-- Name: record; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.record (
    email character varying(60) NOT NULL,
    cname character varying(50) NOT NULL,
    disease_code character varying(50) NOT NULL,
    total_deaths integer,
    total_patients integer
);


ALTER TABLE public.record OWNER TO myuser;

--
-- Name: specialize; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.specialize (
    id integer NOT NULL,
    email character varying(60) NOT NULL
);


ALTER TABLE public.specialize OWNER TO myuser;

--
-- Name: disease_type id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.disease_type ALTER COLUMN id SET DEFAULT nextval('public.disease_type_id_seq'::regclass);


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.country (cname, population) FROM stdin;
United Kingdom	67886011
Germany	83783942
Italy	60461826
Spain	46754778
Australia	25499884
China	1439323776
Japan	126476461
Democratic Republic of the Congo	89561403
Nigeria	206139589
India	1380004385
Brazil	212559417
Argentina	45195777
Peru	32971854
Chile	19116201
Colombia	50882891
Kazakhstan	34984
United States	1111111
BOOK	234235
Canada	1111111
\.


--
-- Data for Name: discover; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.discover (cname, disease_code, first_enc_date) FROM stdin;
China	COVID-19	2019-12-01
United States	Influenza	1918-01-01
United Kingdom	Tuberculosis	1882-03-24
Democratic Republic of the Congo	Ebola	1976-08-01
United States	Alzheimer	1906-11-03
United Kingdom	Common Cold	1950-01-01
United States	Lyme Disease	1975-01-01
Nigeria	Malaria	2222-12-13
\.


--
-- Data for Name: disease; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.disease (disease_code, pathogen, description, id) FROM stdin;
COVID-19	virus	Respiratory illness caused by SARS-CoV-2	6
Influenza	virus	Seasonal flu	6
Tuberculosis	bacteria	Bacterial infection affecting lungs	7
Malaria	parasite	Mosquito-borne infectious disease	8
Diabetes	N/A	Chronic condition affecting insulin	4
Alzheimer	N/A	Progressive neurological disorder	9
Common Cold	virus	Upper respiratory tract infection	6
Cholera	bacteria	Infectious disease causing severe diarrhea	7
Lyme Disease	bacteria	Tick-borne illness	7
Ebola	virus	Severe viral disease	6
\.


--
-- Data for Name: disease_type; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.disease_type (id, description) FROM stdin;
2	Genetic diseases
3	Deficiency diseases
4	Physiological diseases
5	Zoonotic diseases
6	Viral diseases
7	Bacterial diseases
8	Parasitic diseases
9	Neurological diseases
10	Respiratory diseases
11	Virology
12	book
\.


--
-- Data for Name: doctor; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.doctor (email, degree) FROM stdin;
alex.brown@example.com	MD
michael.green@example.com	DO
laura.martinez@medcenter.es	DO
giuseppe.rossi@ospedale.it	MD
anna.bianchi@clinica.it	PhD
marco.verdi@centromedico.it	DO
\.


--
-- Data for Name: patient_disease; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.patient_disease (email, disease_code) FROM stdin;
aibek.narik8@gmail.com	Malaria
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.patients (email) FROM stdin;
laura.martinez@medcenter.es
anna.bianchi@clinica.it
aibek.narik8@gmail.com
\.


--
-- Data for Name: public_servant; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.public_servant (email, department) FROM stdin;
alex.brown@example.com	Public Health
michael.green@example.com	Health Department
mariana.souza@healthdept.br	Health Department
pedro.almeida@epidemiology.br	Epidemiology
carla.costa@publichealth.br	Public Health
john.doe@example.com	Health Building
anna.bianchi@clinica.it	Health Building
aibek.narik8@gmail.com	Health Department 
\.


--
-- Data for Name: record; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.record (email, cname, disease_code, total_deaths, total_patients) FROM stdin;
alex.brown@example.com	United Kingdom	Tuberculosis	2000	30000
mariana.souza@healthdept.br	Brazil	COVID-19	120	4800
pedro.almeida@epidemiology.br	Brazil	COVID-19	130	6000
pedro.almeida@epidemiology.br	Chile	COVID-19	125	5900
carla.costa@publichealth.br	Brazil	COVID-19	90	4700
carla.costa@publichealth.br	Colombia	COVID-19	100	4800
john.doe@example.com	United States	COVID-19	500	3000
michael.green@example.com	Nigeria	Malaria	300	1000
aibek.narik8@gmail.com	Spain	Malaria	234	2452
\.


--
-- Data for Name: specialize; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.specialize (id, email) FROM stdin;
11	anna.bianchi@clinica.it
11	marco.verdi@centromedico.it
6	laura.martinez@medcenter.es
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.users (email, name, surname, salary, phone, cname) FROM stdin;
arsen@gmail.com	Arsen	sdfsdf	324234	234234	Italy
laura.martinez@medcenter.es	Laura	Martinez	125000	600-345-678	Spain
ainurka@gmail.com	Ainurka	asfsdf	234234	23423	Spain
aibek.narik343238@mail.ru	booooook	sfsfsdf	234234234	2423423	Spain
giuseppe.rossi@ospedale.it	Giuseppe	Rossi	130000	600-123-456	Italy
anna.bianchi@clinica.it	Anna	Bianchi	125000	600-234-567	Italy
marco.verdi@centromedico.it	Marco	Verdi	120000	600-345-678	Italy
carla.costa@publichealth.br	Carla	Costa	54272000	600-456-789	Brazil
joao.silva@healthdept.br	João	Silva	56320000	600-123-456	Brazil
john.doe@example.com	John	Doe	409600000	123-456-7890	United States
mariana.souza@healthdept.br	Mariana	Souza	53248000	600-234-567	Brazil
pedro.almeida@epidemiology.br	Pedro	Almeida	52224000	600-345-678	Brazil
aibek.narik8@gmail.com	Aibek	Pushka	234235	235234	Spain
michael.green@example.com	Michael	Green	111111	567-890-1234	\N
aibek.narik899@gmail.com	Aibek	Narik	4234234	2432	Spain
alex.brown@example.com	Alex	Brown	60000	345-678-9012	Spain
\.


--
-- Name: disease_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.disease_type_id_seq', 1, false);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (cname);


--
-- Name: discover discover_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.discover
    ADD CONSTRAINT discover_pkey PRIMARY KEY (cname, disease_code);


--
-- Name: disease disease_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_pkey PRIMARY KEY (disease_code);


--
-- Name: disease_type disease_type_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.disease_type
    ADD CONSTRAINT disease_type_pkey PRIMARY KEY (id);


--
-- Name: doctor doctor_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (email);


--
-- Name: patient_disease patient_disease_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.patient_disease
    ADD CONSTRAINT patient_disease_pkey PRIMARY KEY (email, disease_code);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (email);


--
-- Name: public_servant public_servant_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.public_servant
    ADD CONSTRAINT public_servant_pkey PRIMARY KEY (email);


--
-- Name: record record_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.record
    ADD CONSTRAINT record_pkey PRIMARY KEY (email, cname, disease_code);


--
-- Name: specialize specialize_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.specialize
    ADD CONSTRAINT specialize_pkey PRIMARY KEY (id, email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


--
-- Name: idx_disease_code; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX idx_disease_code ON public.disease USING btree (disease_code);


--
-- Name: idx_disease_disease_code; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX idx_disease_disease_code ON public.disease USING btree (disease_code);


--
-- Name: discover discover_cname_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.discover
    ADD CONSTRAINT discover_cname_fkey FOREIGN KEY (cname) REFERENCES public.country(cname);


--
-- Name: discover discover_disease_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.discover
    ADD CONSTRAINT discover_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES public.disease(disease_code);


--
-- Name: disease disease_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_id_fkey FOREIGN KEY (id) REFERENCES public.disease_type(id);


--
-- Name: doctor doctor_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_email_fkey FOREIGN KEY (email) REFERENCES public.users(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: patient_disease patient_disease_disease_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.patient_disease
    ADD CONSTRAINT patient_disease_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES public.disease(disease_code);


--
-- Name: patient_disease patient_disease_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.patient_disease
    ADD CONSTRAINT patient_disease_email_fkey FOREIGN KEY (email) REFERENCES public.patients(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: patients patients_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_email_fkey FOREIGN KEY (email) REFERENCES public.users(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public_servant public_servant_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.public_servant
    ADD CONSTRAINT public_servant_email_fkey FOREIGN KEY (email) REFERENCES public.users(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: record record_cname_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.record
    ADD CONSTRAINT record_cname_fkey FOREIGN KEY (cname) REFERENCES public.country(cname);


--
-- Name: record record_disease_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.record
    ADD CONSTRAINT record_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES public.disease(disease_code);


--
-- Name: record record_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.record
    ADD CONSTRAINT record_email_fkey FOREIGN KEY (email) REFERENCES public.public_servant(email) ON DELETE CASCADE;


--
-- Name: specialize specialize_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.specialize
    ADD CONSTRAINT specialize_email_fkey FOREIGN KEY (email) REFERENCES public.doctor(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: specialize specialize_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.specialize
    ADD CONSTRAINT specialize_id_fkey FOREIGN KEY (id) REFERENCES public.disease_type(id);


--
-- Name: users users_cname_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_cname_fkey FOREIGN KEY (cname) REFERENCES public.country(cname);


--
-- PostgreSQL database dump complete
--

