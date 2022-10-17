# ASKEM Data Store API

## Usage

The API can be started by simply calling

```
docker compose up
```
(Please note that any changes in the `src/generated` directory
will forbid the API from starting.)

## Development

To simply start the server, run:
```
docker compose --profile dev up
```
which will also start a development instance of Postgres.

The API also has a CLI tool which can be used by `cd`ing into and
running `./main.py`. This will return a list of possible subcommands
which are `start` and `gen`. The docker container runs `start` under the hood
while `gen` is a command the developer only runs if there has been a change
to the data model in `askem.dbml`.

If the tables don't exist yet it in Postgres, make sure to POST to the `/admin/db/init`
endpoint.

## ASKEM Data Model

![The generated graphic](./misc/askem.png)

ERD was created using [DBML](https://www.dbml.org/home/) and rendered and edited using [dbdiagram](https://dbdiagram.io/)
