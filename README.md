# Blahgr

Blahgr is a simple Django blogging application that supports:

- Signing up as a new user
- Creating posts
- Commenting on yours or others' posts
- Deleting your own posts or comments<sup>1</sup>
- A custom `manage.py` command to generate sample data

It is composed of the following **apps**:
- `blog` for managing all posts and comments
- `users` for handling registration and authentication

It uses [Poetry](https://python-poetry.org/)<sup>2</sup> for managing
the project and dependencies, which can either be installed manually
(assuming Python 3.10.4<sup>3</sup> is installed) or everything can
be run via `docker-compose`.

> <sup>1</sup> Deletes are performed *soft* such that
> nothing is removed from the database; only the UI.
>
> <sup>2</sup> Projects I have worked on to-date have typically
> used setuptools and `pip` etc. so I took this as an opportunity
> to see what using `poetry` was like.
>
> <sup>3</sup> Likewise with having an opportunity to use `poetry`,
> I have typically been locked into older versions of Python, eg. 3.5,
> so this was a great excuse to start playing with *assignment expressions*,
> *structural pattern matching*, etc. to see if they improve ergonomics.

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
migrations or seed data.

If you would like to **reset the database completely** then
run `docker-compose down -v` to remove the data volume from your host system.
