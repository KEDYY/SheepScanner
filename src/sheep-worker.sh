#!/usr/bin/env sh
celery worker -A sheepscan --config config.celery -l debug
