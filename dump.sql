--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Ubuntu 17.4-1.pgdg24.04+2)
-- Dumped by pg_dump version 17.4 (Ubuntu 17.4-1.pgdg24.04+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: favourite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favourite (
    id integer NOT NULL,
    user_id_fk integer NOT NULL,
    fav_user_id_fk integer NOT NULL
);


ALTER TABLE public.favourite OWNER TO postgres;

--
-- Name: favourite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favourite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favourite_id_seq OWNER TO postgres;

--
-- Name: favourite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favourite_id_seq OWNED BY public.favourite.id;


--
-- Name: profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profile (
    id integer NOT NULL,
    user_id_fk integer NOT NULL,
    description character varying,
    parish character varying,
    biography character varying,
    sex character varying,
    race character varying,
    birth_year integer,
    height double precision,
    fav_cuisine character varying,
    fav_colour character varying,
    fav_school_subject character varying,
    political boolean,
    religious boolean,
    family_oriented boolean
);


ALTER TABLE public.profile OWNER TO postgres;

--
-- Name: profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.profile_id_seq OWNER TO postgres;

--
-- Name: profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profile_id_seq OWNED BY public.profile.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    photo character varying,
    date_joined timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: favourite id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourite ALTER COLUMN id SET DEFAULT nextval('public.favourite_id_seq'::regclass);


--
-- Name: profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile ALTER COLUMN id SET DEFAULT nextval('public.profile_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: favourite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favourite (id, user_id_fk, fav_user_id_fk) FROM stdin;
4	2	1
5	1	2
6	1	3
7	1	4
8	2	4
9	3	4
10	3	1
11	1	1
12	4	1
13	1	6
14	6	2
15	6	3
16	4	3
17	2	6
18	4	2
19	4	6
20	2	3
21	3	6
22	6	1
\.


--
-- Data for Name: profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profile (id, user_id_fk, description, parish, biography, sex, race, birth_year, height, fav_cuisine, fav_colour, fav_school_subject, political, religious, family_oriented) FROM stdin;
6	3	Love hiking and outdoor adventures.	St.Catherine	Tech enthusiast and coffee lover.	Female	Mixed	1998	1.75	Chinese	Blue	Mathematics	t	t	t
7	4	Love hiking and outdoor adventures.	St.Catherine	Tech enthusiast and coffee lover.	Female	Mixed	1998	1.75	Chinese	Blue	Mathematics	t	t	t
5	2	Love hiking and outdoor adventures.	Kingston	Tech enthusiast and coffee lover.	Female	Mixed	1998	172	Japanese	Blue	English	f	t	t
10	1	bjeksbwekjbfewkjbfwekjbkjfwebkjfebwkjfbewkjfbkjewb	St. Elizabeth	fwejefqkbfwejbjkfewbkjfewbkjqwbkjwebqkjwbqjhwdbmnfeqbw	Male	Black	1997	178	Chinese	Blue	Math	f	f	t
4	1	Love hiking and outdoor adventures.	Kingston	efwhjbfwekhfewhbfwehjbfwehjbfwehjbfew	Male	Mixed	1999	175	Japanese	Blue	Mathematics	f	t	t
11	6	bjeksbwekjbfewkjbfwekjbkjfwebkjfebwkjfbewkjfbkjewb	St. Elizabeth	cdbkcdbwjhbcewjbcejwhbchjewbc	Male	Black	1991	178	Chinese	Blue	Math	t	t	f
8	6	ferhbwefjhbfwejhbfewhjbewh	St. Elizabeth	csdm jdsnjcwnkjewnkjnwee	Female	White	1991	173	Chinese	Red	Math	f	t	t
9	1	bjeksbwekjbfewkjbfwekjbkjfwebkjfebwkjfbewkjfbkjewb	St. Elizabeth	bkjdsbkjwebewvbcbsqkjbceqhywbdewqkjbdwqjkbdwhdqwjkbdckjbaslkjdbjkewbajkdeb	Male	White	1991	178	Chinese	Blue	Math	f	t	f
12	7	bjeksbwekjbfewkjbfwekjbkjfwebkjfebwkjfbewkjfbkjewb	Kingston	ehsbwhejwqbhejfwbhjfwebhjfwebhjwfeb	Female	White	2007	189	Chinese	Blue	Math	f	t	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, name, email, photo, date_joined) FROM stdin;
1	kevonteh	scrypt:32768:8:1$BR0g9jHPAeoR4jE5$83fd602d1ad742bd80b77dda58780ecc05e39f5489b821c382c30d2913506d73bf6b209f47c35afc78366b8f0cc712f1f0528dc1de9ac05704ea9b8a5aadf21c	kevontehB	bro@gmail.com	\N	2025-04-27 18:38:29.325553
2	kevonteh2	scrypt:32768:8:1$7lgLMd5RsxuugACW$90e4a09df62e36b457e12ce22d5f2e80d768e6883da73f3f76b65d46789f61de39370e4cb7d44c774269214819df63be77b785474ee04cea9ae7454a6f1cc035	kevontehB2	bro2@gmail.com	\N	2025-04-27 22:09:33.451967
3	kevonteh3	scrypt:32768:8:1$NiUATS7WuUxvooBl$4bd314e01591b94f4426eeea4b4cc7faae2e3277d164f509da53cbb4ffae8e34c23ce0b6852020184dde6c93cad4f5e5befe9ffff2261eca61cd008bd20fb465	kevontehB3	bro3@gmail.com	\N	2025-04-28 05:20:54.530155
4	kevonteh4	scrypt:32768:8:1$XsO5fdsODOMgkzXc$d9d9a0f888f67b2481c15ddb2f687a70d21e74ebc49bcc4188feb26b3e034d136374e541d50543d11a1b48018f39f8c89be0e7be7045600e7e378adb7b1edb39	kevontehB4	bro4@gmail.com	\N	2025-04-28 05:22:31.11351
5	kevonteh5	scrypt:32768:8:1$tMHFMjvtfuWkovt0$857814879243ba002afcfc6f189a2f9f94841a4d651a8194fa5917c6eb077836a66bbe422928c075e9d8afc600aae3f7b2b6b630d20c2771a55b21546df87cf9	kevontehB5	bro5@gmail.com	Screenshot_from_2025-04-23_13-59-55.png	2025-04-28 17:26:35.536246
6	doe	scrypt:32768:8:1$hExRPvcDPnwkizZh$8c678055ac47ae5c4fde93fb3bbec234cdd7086acfbc7bccda65bc6af8a6b01bf98cfc5fd0ae91060da30f23651933d64e8bab55df16688f7c09ea9cfb9cf376	john	john@gmail.com	drone_arm.drawio_1.png	2025-05-02 19:37:14.872486
7	kevy	scrypt:32768:8:1$oJXLMY8j5whPMEEI$508eda50310aa35700df5cad0ced05495eb8ff595ce92851288b563ad36cde7b74f004a0a2fc7f2d0b0244be4589767166b0baa38ef8650ea8b816701e4e81f7	kevonteh	brownkevonteh@gmail.com	space-soldier-1182023.png	2025-05-04 08:36:06.126864
\.


--
-- Name: favourite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favourite_id_seq', 22, true);


--
-- Name: profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profile_id_seq', 12, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: favourite favourite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourite
    ADD CONSTRAINT favourite_pkey PRIMARY KEY (id);


--
-- Name: profile profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: favourite favourite_fav_user_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourite
    ADD CONSTRAINT favourite_fav_user_id_fk_fkey FOREIGN KEY (fav_user_id_fk) REFERENCES public.users(id);


--
-- Name: favourite favourite_user_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourite
    ADD CONSTRAINT favourite_user_id_fk_fkey FOREIGN KEY (user_id_fk) REFERENCES public.users(id);


--
-- Name: profile profile_user_id_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_user_id_fk_fkey FOREIGN KEY (user_id_fk) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

