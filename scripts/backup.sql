--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

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
-- Data for Name: feeds; Type: TABLE DATA; Schema: public; Owner: komine
--

INSERT INTO public.feeds (id, site_title, site_url, feed_url) VALUES (1, 'Menthas Programming', 'https://menthas.com', 'https://menthas.com/programming/rss');
INSERT INTO public.feeds (id, site_title, site_url, feed_url) VALUES (2, '日々常々', 'https://irof.hateblo.jp', 'https://irof.hateblo.jp/rss');


--
-- Name: feeds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: komine
--

SELECT pg_catalog.setval('public.feeds_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

