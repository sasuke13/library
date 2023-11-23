Documentation:
  All the needed comments are located in interfaces and views of every app.
  Project has 5 root endpoints: api/v1/ + (visitors, books, reading_statistics, sessions) and admin/

Before the start of the project you should create .env in root directory with fields:
  POSTGRES_DB
  POSTGRES_PASSWORD
  POSTGRES_USER
  POSTGRES_HOST
  POSTGRES_PORT
  REDIS_HOST
  REDIS_PORT

How to run:
  Via console(you need to have a postgresql and reddis databases):
    cd src
    python manage.py migrate
    python manage.py runserver

    Celery:
      celery -A config worker -l INFO
    Celery beat:
      celery -A config beat -l info
    Flower:
      celery -A config flower --broker=redis://redis
    
  Via Docker:
    docker-compose up --build
  
