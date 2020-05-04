update:
	git pull
	sudo docker-compose down
	sudo docker-compose build
	sudo docker-compose up -d

user:
	sudo docker-compose exec web python create_user.py

login-psql:
	sudo docker-compose exec db psql -U testuser -d testdb
	
