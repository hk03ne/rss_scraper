--
-- PostgreSQL database dump
--

-- Dumped from database version 11.6
-- Dumped by pg_dump version 11.5

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
-- Data for Name: feeds; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.feeds (id, user_id, site_title, site_url, feed_url) FROM stdin;
1	1	Wikipedia	https://ja.wikipedia.org	https://ja.wikipedia.org/w/index.php?title=%E7%89%B9%E5%88%A5:%E6%96%B0%E3%81%97%E3%81%84%E3%83%9A%E3%83%BC%E3%82%B8&feed=rss
\.


--
-- Name: feeds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.feeds_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

