#!/bin/bash
pg_restore -U $POSTGRES_USER -d $POSTGRES_DB -v docker-entrypoint-initdb.d/songs.dump