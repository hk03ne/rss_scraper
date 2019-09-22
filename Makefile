init:
	pip3 install -r requirements.txt
	psql --dbname=testdb < schema.sql
	psql --dbname=productiondb < schema.sql
test:
	python3 test_scraper.py
	
