#!/bin/bash

cd src && celery -A config flower --broker=redis://redis