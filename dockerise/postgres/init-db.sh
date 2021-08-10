#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE debug WITH LOGIN SUPERUSER PASSWORD 'debug';
    CREATE DATABASE directory_cms_debug;
EOSQL
psql -v ON_ERROR_STOP=0 --quiet --username debug directory_cms_debug < /directory_cms.sql
