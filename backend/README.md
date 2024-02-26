# Projectify Backend

# Requirements

- Python 3.11 (I recommend using [asdf](https://asdf-vm.com/))
- [poetry](https://python-poetry.org/docs/)
- PostgreSQL >= 15.5
- Redis (6 >= for production)

## Debian 12 (bullseye) installation

Make sure you have Postgres 15 and its dev library installed.

```
sudo apt install postgresql-15 libpq-dev
# Optionally run this, if not using nix flake
sudo apt install libpq-dev
```

Managing Python is convenient using asdf:

```
asdf plugin-add python
# This is the version used at the time of writing, subject to change
asdf install python 3.11.4
```

# Quickstart

To get started, you have to

1. Clone the repository,
2. cd into `backend` directory,
3. create a `.env` file from `.env.template`,
4. edit the `.env` file to add a `DATABASE_URL` and `REDIS_TLS_URL` for a local
   Redis and PostgreSQL 15 instance, and
5. create the projectify PostgreSQL database. Then,
6. inside a poetry shell,
  a. migrate the database,
  b. seed it with test data, and then
  c. run the development server

The commands to run are these:

```
git clone git@github.com:jwp-consulting/projectify-backend.git
cd projectify-backend/backend
poetry install --with dev --with test --no-root
cp .env.template .env
vim .env
# Inside .env:
# 1) Edit DATABASE_URL
# 2) Edit REDIS_TLS_URL
# Create the database
createdb projectify
# Now you can run the server
poetry shell
./manage.py migrate
./manage.py seeddb
./manage.py runserver
```

Furthermore, to run a celery worker:

`celery -A projectify worker -c 1`

To run neovim with the correct pyright:

```
poetry run nvim
```

# Production Environment Variables

- `DJANGO_SETTINGS_MODULE`
- `DJANGO_CONFIGURATION`
- `DATABASE_URL`
- `SECRET_KEY`
- `MAILGUN_API_KEY`
- `MAILGUN_DOMAIN`
- `FRONTEND_URL`
- `REDIS_TLS_URL`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_PRICE_OBJECT`
- `STRIPE_ENDPOINT_SECRET`

# Updating poetry dependencies

When updating a package installed by poetry, make sure to recreate and check in
requirements.txt by running

```
poetry lock --no-update
poetry install --sync
bin/update-requirements
git add requirements.txt
# Maybe git commit here
```


## Flake

There is a nix flake in this repository.

- https://github.com/nix-community/poetry2nix
- https://github.com/nix-community/nix-direnv

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
