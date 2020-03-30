#!/bin/bash

echo "Building docker image..."
docker build ./backend -t us.gcr.io/personal-site-staging-a449f/career-day-api
echo "Finihed building docker image."

echo "Pushing docker image..."
docker push us.gcr.io/personal-site-staging-a449f/career-day-api:latest
echo "Finished pushing docker image."
