#!/bin/bash
sqlite3 test.sqlite3 "CREATE TABLE entries (site_title not null, site_url not null, entry_title not null, entry_url not null, updated not null)"
sqlite3 production.sqlite3 "CREATE TABLE entries (site_title not null, site_url not null, entry_title not null, entry_url not null, updated not null)"
