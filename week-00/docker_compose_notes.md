# Docker Compose — Revision Notes

Written from my Week 0 work on `de-project-1` (Postgres in Docker Compose). Keep this in `de-notes/week-00/`. Read top to bottom once, then use the section titles to look things up.

---

## 1. The three building blocks

| Thing | What it is | Lifespan |
|---|---|---|
| **Image** (`postgres:17`) | A read-only template with the software installed | Stays until deleted |
| **Container** (`de-project-1-de-postgres-1`) | A running copy made from the image | Disposable; `down` deletes it |
| **Volume** (`de-project-1_pgdata`) | Storage Docker manages outside any container | Survives until the volume itself is deleted |

**Analogy:** the container is a laptop you are allowed to throw away; the volume is an external drive plugged into it. Replace the laptop, plug the drive back in, and your files are still there.

The link between a container and a volume is one line in the compose file:

```yaml
- pgdata:/var/lib/postgresql/data
```

Postgres writes its data to `/var/lib/postgresql/data` inside the container. That folder is really the `pgdata` volume, so the data outlives the container.

**Compose adds the project name (the folder name) in front of volume names.** That is why `pgdata` appears as `de-project-1_pgdata` in `docker volume ls`.

### What each command does to them

| Command | Container | Volume (your data) |
|---|---|---|
| `docker compose stop` | stopped, kept | kept |
| `docker compose down` | **deleted** | **kept** |
| `docker compose down -v` | deleted | **deleted** |

`down` is a normal shutdown. `down -v` is a reset that erases the database. Think before you type `-v`.

---

## 2. A compose file is a recipe card

Each part of your app (web app, database, cache) is a **service**. For every service, answer the same six questions. Learn the questions and you can read or write any compose file.

| # | Question | Key | Example from my file |
|---|---|---|---|
| 1 | What runs? | `image:` (ready-made) or `build:` (my own code, via a Dockerfile) | `image: postgres:17` |
| 2 | How do I reach it? | `ports:` as `host:container` | `127.0.0.1:55432:5432` |
| 3 | What settings does it need? | `environment:` or `env_file:` | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` |
| 4 | What must survive? | `volumes:` | `pgdata` |
| 5 | What must it wait for? | `depends_on:` plus `healthcheck:` | the `pg_isready` check |
| 6 | How does it start? | `command:` (only if the default is wrong) | not needed |

### My file, line by line

```yaml
services:
  de-postgres:                      # service name (my choice); other containers reach it by this name
    image: postgres:17              # ready-made image, version pinned
    environment:                    # names come from the Postgres image's docs
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}   # :? = stop with a message if missing
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      # Bound to localhost only; "5432:5432" would expose it on all interfaces
      - "127.0.0.1:${POSTGRES_PORT:-5432}:5432"   # laptop door : container door; default 5432 if unset
    volumes:
      - pgdata:/var/lib/postgresql/data           # named volume: the database files
      - ./data:/data:ro                           # bind mount: my folder, visible inside as /data, read-only
    healthcheck:                    # "healthy" = Postgres actually accepts connections
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:                           # declares the named volume
```

### Small facts worth remembering
- `${NAME}` is replaced with the value from the `.env` file. That is why the compose file holds no real secrets and is safe to commit.
- The `POSTGRES_*` variables are read **only the first time**, when the data directory is empty. Changing the password in `.env` later does not change an existing database.
- A **named volume** (`pgdata:`) is managed by Docker. A **bind mount** (`./data:/data`) shows a folder from my own machine inside the container. `\copy` runs inside the container, so it can only see files that are mounted.
- `:ro` means read-only, so the container cannot change my files.
- Binding to `127.0.0.1` means only my own machine can connect, not other devices on the network.

---

## 3. Where do the words in a compose file come from?

There are **three sources**:

1. **Compose's own words** (`services`, `image`, `ports`, `volumes`, `healthcheck`...). A fixed vocabulary, the same in every project. Reference: https://docs.docker.com/reference/compose-file/
2. **The image's words.** `POSTGRES_PASSWORD`, port `5432` and the folder `/var/lib/postgresql/data` are not Compose. The people who built the image chose them, and they are documented on the image's Docker Hub page. Another image uses other names (MySQL wants `MYSQL_ROOT_PASSWORD`).
   - Postgres: https://hub.docker.com/_/postgres
   - MySQL: https://hub.docker.com/_/mysql
   - Nginx: https://hub.docker.com/_/nginx
3. **My app's words.** The port my app listens on, the environment variables its code reads, and the command that starts it come from my code and framework docs.

**Rule:** the *keys* are Compose; the *names inside `environment`* belong to the image (or my app); the *values* are mine.

### Routine for any new project
1. List the parts of the app. Each part is one service.
2. For each ready-made part, read the "how to use this image" section on its Docker Hub page: variables, port, data folder.
3. For my own code, find the port it uses, the variables it reads, and the command that starts it.
4. Look up any unfamiliar Compose key in the reference.
5. Run `docker compose config`, then `docker compose up -d`, then read `docker compose logs`.

---

## 4. Ports and networking: two sets of doors

`ports: "127.0.0.1:55432:5432"` means: laptop door **55432** leads to container room **5432**.

| Who is connecting | From where | Use |
|---|---|---|
| A tool on my laptop (DBeaver, host `psql`) | Outside Docker | `localhost:55432` |
| Another container (e.g. Django's `web`) | Inside the Compose network | `db:5432` (service name + the container's own port) |
| `docker compose exec de-postgres psql ...` | Inside the container | no host or port needed |

Key ideas:
- Each container is its own tiny computer. `localhost` inside a container means **that same container**, so a web container using `localhost` for the database fails.
- Compose puts all services on a private network where they find each other by **service name**.
- `ports:` is only for letting things **outside** the network in. A service that only other containers use needs no `ports:` line at all.
- Two services on different ports inside the network never clash. A clash happens only on the **host side**, as it did when two Postgres servers on my machine already held 5432 and 5433.

---

## 5. Dockerfile vs docker-compose.yml

- A **Dockerfile** is the recipe for **one dish**: it builds one image.
- A **compose file** is the order for **the whole table**: which containers run together, how they connect, what to keep.

| | Dockerfile | docker-compose.yml |
|---|---|---|
| Job | Build **one image** | Run **several containers together** |
| Contains | Base system, install steps, copy code, default start command | Services, ports, environment, volumes, dependencies |
| Used when | **Build time** | `docker compose up` |
| Used for | **My own code** | Everything, including ready-made images |

The link between them is `build: .` in the compose file, which means "build this service's image from the Dockerfile in this folder".

A small Django Dockerfile:

```dockerfile
FROM python:3.12-slim              # start from an image that already has Python
WORKDIR /app                       # work inside /app
COPY requirements.txt .            # copy the dependency list first
RUN pip install -r requirements.txt
COPY . .                           # then copy my code
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]   # default start command
```

`de-project-1` has **no Dockerfile** yet, because Postgres is a ready-made image.

---

## 6. Examples for other stacks

These are starting points, not copy-paste-ready. They still need a Dockerfile (and, for Laravel, an Nginx config).

### Django + Postgres

```yaml
services:
  web:
    build: .                        # needs a Dockerfile next to this file
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "127.0.0.1:8000:8000"
    env_file: .env
    volumes:
      - .:/app                      # my code appears live inside the container
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      retries: 5
volumes:
  pgdata:
```

- `0.0.0.0:8000` matters. Without `0.0.0.0`, Django listens only inside its own container and the browser cannot reach it.
- In `settings.py`, the database host is `db` (the service name), port `5432`.
- `db` has no `ports:` line, yet `web` reaches it. That is correct.

### Laravel + MySQL

```yaml
services:
  app:                              # PHP-FPM runs the Laravel code
    build: .
    volumes:
      - .:/var/www
    depends_on:
      - mysql
  nginx:                            # web server in front of PHP-FPM
    image: nginx:alpine
    ports:
      - "127.0.0.1:8080:80"
    volumes:
      - .:/var/www:ro
      - ./docker/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
  mysql:
    image: mysql:8
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysqldata:/var/lib/mysql
volumes:
  mysqldata:
```

- **Why one more service than Django?** PHP-FPM does not speak HTTP, so Nginx sits in front and passes PHP requests to it. Django's server speaks HTTP itself.
- The `MYSQL_*` variable names and `/var/lib/mysql` came from the MySQL image's Hub page.
- In Laravel's `.env`: `DB_HOST=mysql` (the service name), `DB_PORT=3306`.
- Laravel's official shortcut is **Sail**, which generates this for you: https://laravel.com/docs/sail

---

## 7. Command reference

| Command | What it does |
|---|---|
| `docker compose up -d` | Reads the file and `.env`, pulls missing images, creates the network and volume, starts containers in the background. Safe to re-run |
| `docker compose up` | Same, but attached to the terminal. Ctrl+C **stops** the containers |
| `docker compose ps` | Shows status, including `healthy` |
| `docker compose ps -a` | Also shows stopped and created-only containers |
| `docker compose logs de-postgres` | Shows the service's output so far |
| `docker compose logs -f de-postgres` | Follows the output live. Ctrl+C stops only the viewing |
| `docker compose exec de-postgres psql -U <user> -d <db>` | Opens psql inside the running container |
| `docker compose attach de-postgres` | Attaches to the main process. Ctrl+C may stop the container, so prefer `logs -f` |
| `docker compose config` | Prints the file with every `${...}` filled in and validates it. **Shows the real password, so never share the output** |
| `docker compose stop` / `start` | Stop or restart containers, keep everything |
| `docker compose down` | Remove containers and the network, **keep the volume** |
| `docker compose down -v` | Also **delete the volume (erases the database)** |
| `docker volume ls` | List volumes |
| `docker volume inspect de-project-1_pgdata` | Show where Docker stores one |

### What `docker compose up -d` does, in order
1. Reads the config and fills in `${...}` from `.env`. It stops with an error if a required variable (like the password) is missing.
2. Pulls images it does not have (the first pull of `postgres:17` took about 14 minutes on my connection; later runs use the local copy).
3. Creates the network and the volume if they do not exist.
4. Creates and starts the containers. On the very first start, Postgres creates the user, password and database from the environment variables and saves them in the volume.
5. Gives the terminal back (`-d` = detached, running in the background).

### If I interrupt it
- During a download: finished layers stay cached. Re-run the command.
- After containers started (with `-d`): only the command stops; the containers keep running.
- Partway through: some pieces may exist but not be started. Re-run `docker compose up -d`; it only creates or starts what is missing.
- If Postgres was interrupted during its very first start and the logs complain about the data directory, and there is **no data yet**, `docker compose down -v` then `up -d` resets it. Never use `-v` once there is data to keep.

---

## 8. psql basics

| Do this | Why |
|---|---|
| End every SQL statement with `;` | psql waits for the end of the statement |
| `\copy`, `\dt`, `\q` need no `;` | They are psql commands, not SQL |
| Prompt `=#` | Ready for a new command |
| Prompt `-#` | Mid-statement. Press Ctrl+C to discard and start again |
| `\dt` | List tables |
| `\q` | Quit |

`\copy table FROM '/data/file.csv' CSV HEADER` loads a CSV. It reads the path **inside the container**, so the folder must be mounted.

---

## 9. Problems I hit and how I fixed them

| Symptom | Cause | Fix |
|---|---|---|
| `bind: address already in use` on 5432, then 5433 | Two Postgres servers installed on my machine already used those ports | Find owners with `sudo ss -ltnp \| grep -E ':(5432\|5433)\b'`. Pick a free high port, set `POSTGRES_PORT=55432` in `.env` |
| `psql` on my machine connects to the wrong database | Host Postgres servers are also running | Use `docker compose exec ...` or the port `55432` |
| psql prompt changed to `-#`, then `relation does not exist` | I forgot the `;` after `CREATE TABLE`, so `\copy` ran before the table existed | End SQL with `;`; Ctrl+C clears a half-typed statement |
| Changed `POSTGRES_PASSWORD` in `.env` but the old password still works | Variables are read only when the data directory is empty | Change the password inside the database, or reset the volume if it holds no data |
| `data/` folder owned by root | Docker created it because it did not exist | `sudo chown "$USER": data`, and run `mkdir data` before `up` |
| `.gitignore` rule ignoring too much | `raw/` without a leading `/` matches at any depth | Anchor it: `/raw/`, `/data/`. Whitelist `!dbt/seeds/*.csv` |

---

## 10. Self-check questions

Try to answer before reading the answers.

1. What is the difference between an image, a container and a volume?
2. After `docker compose down`, is my table gone? After `down -v`?
3. Where do `POSTGRES_USER` and `/var/lib/postgresql/data` come from?
4. What does `127.0.0.1:55432:5432` mean, left to right?
5. Why can't a Django container connect to Postgres with `localhost`?
6. Which host and port does the Django container use for the database? Which does DBeaver on my laptop use?
7. What is the difference between a Dockerfile and a compose file?
8. If I want DBeaver on my laptop to see the Django project's database, what must I add to the `db` service?

**Answers**
1. Image = read-only template. Container = running copy of it, disposable. Volume = storage that outlives containers.
2. After `down`, the table is still there (the volume is kept). After `down -v`, it is gone.
3. Both come from the Postgres image's documentation (Docker Hub), not from Compose.
4. Laptop address (localhost only) : laptop port 55432 : container port 5432.
5. `localhost` inside a container means that same container, and Postgres runs in a different one.
6. Django container: `db:5432` (service name and the container's own port). DBeaver: `localhost:55432`.
7. A Dockerfile builds one image. A compose file runs several containers together.
8. A `ports:` line such as `- "127.0.0.1:55432:5432"` (pick a port that is free on my machine), then connect DBeaver to `localhost:55432`.

---

## 11. Links

- Compose file reference: https://docs.docker.com/reference/compose-file/
- Docker Compose overview: https://docs.docker.com/compose/
- Docker get started: https://docs.docker.com/get-started/
- Postgres image: https://hub.docker.com/_/postgres
- MySQL image: https://hub.docker.com/_/mysql
- Nginx image: https://hub.docker.com/_/nginx
- Laravel Sail: https://laravel.com/docs/sail
- PostgreSQL docs: https://www.postgresql.org/docs/current/
