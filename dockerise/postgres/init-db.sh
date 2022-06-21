#!/bin/bash

set -e

psql -v ON_ERROR_STOP=0 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION postgis;
    CREATE ROLE debug WITH LOGIN SUPERUSER PASSWORD 'debug';
    CREATE DATABASE directory_cms_debug;
    CREATE DATABASE directory_api_debug;
EOSQL
psql -v ON_ERROR_STOP=0 --quiet --username debug directory_cms_debug < /data/directory_cms.sql
