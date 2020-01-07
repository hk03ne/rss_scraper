init:
	pip3 install -r requirements.txt
	psql --dbname=testdb < schema.sql
	psql --dbname=productiondb < schema.sql
test:
	python3 -m unittest discover
	
reinit:
	psql --dbname=productiondb < scripts/drop.sql
	psql --dbname=testdb < scripts/drop.sql
	psql --dbname=productiondb < schema.sql
	psql --dbname=testdb < schema.sql
