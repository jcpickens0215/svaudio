#!/bin/bash

set -o errexit
set -o nounset


watchgod celery.__main__.main --args -A config.celery_app worker -l INFO
