#!/bin/sh
./utils/wait-for db:5432
alembic upgrade head
$@