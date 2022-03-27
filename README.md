# Blahgr

Blahgr is a simple blogging application.

## Setup

Start the database and web server by running:

```bash
# Run the services in the foreground
$ docker-compose up

# Or run them in the background
$ docker-compose up -d
```

This will take care of initializing a new database, running migrations,
and starting the web server.
You should then be able to visit http://localhost:8000 and see the running application!

If you would like to seed the database with sample data, you can run the
(comically long) command:

```bash
$ docker-compose run server poetry run python manage.py seedblog
```

To stop the services, either `CTRL-C` if running in foreground or `docker-compose down`
if running detached. This will preserve the database so future restarts will not require
migrations or seed data. If you would like to *reset the database completely* then
run `docker-compose down -v` to remove the data volume from your host system.
