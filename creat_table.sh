#!/bin/bash
sqlite3 test.sqlite3 "CREATE TABLE entries (site_title not null, site_url not null, entry_title not null, entry_url not null, summary, updated not null)"
sqlite3 test.sqlite3 "CREATE TABLE feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    site_title not null, site_url not null, feed_url not null unique)"


sqlite3 production.sqlite3 "CREATE TABLE entries (site_title not null, site_url not null, entry_title not null, entry_url not null, summary, updated not null)"
sqlite3 production.sqlite3 "CREATE TABLE feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    site_title not null, site_url not null, feed_url not unique)"
sqlite3 production.sqlite3 'INSERT INTO feeds (site_title, site_url, feed_url) VALUES ("技術評論社", "https://gihyo.jp", "https://gihyo.jp/feed/atom")'

