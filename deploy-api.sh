#!/bin/bash

echo "Building docker image..."
docker build ./backend -t us.gcr.io/personal-site-staging-a449f/dj-pep-api
echo "Finished building docker image!"

echo "Pushing docker image..."
docker push us.gcr.io/personal-site-staging-a449f/dj-pep-api:latest
echo "Finished pushing docker image!"

echo "Deploying to cloud run service..."
gcloud beta run deploy dj-pep-api --image us.gcr.io/personal-site-staging-a449f/dj-pep-api:latest --platform managed --project personal-site-staging-a449f --region us-central1
echo "Finished deploying to cloud run service!"
