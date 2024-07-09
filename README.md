# xml-api
An API for receiving XML files, extracting relevant information and storing it in an SQLite database.

The app serves two endpoints:

* http://127.0.0.1:8000/api/upload/

    Accepts POST requests for the file upload, `Content-Type: multipart/form-data`, key `file` 
    with the uploaded XML file.

* http://127.0.0.1:8000/api/db-view/

    Accepts GET request to get the content of the database.

## Run in docker

https://hub.docker.com/repository/docker/vcerchez/xml-api/general

```bash
docker run -p 8000:8000 vcerchez/xml-api:v1
```

The database is stored in the container.

## Run locally

Initialize app:

```bash
python manage.py makemigrations
python manage.py migrate
```

Run app:

```bash
python manage.py runserver
```
