#!/bin/bash
pg_dump --column-inserts --data-only -t feeds productiondb > backup.sql
psql --dbname=productiondb < drop.sql
psql --dbname=productiondb < ../schema.sql
psql --dbname=productiondb < backup.sql
