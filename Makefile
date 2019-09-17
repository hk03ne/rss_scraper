init:
	pip3 install -r requirements.txt
	sqlite3 test.sqlite3         < schema.sql
	sqlite3 production.sqlite3   < schema.sql
test:
	python3 test_scraper.py
	
