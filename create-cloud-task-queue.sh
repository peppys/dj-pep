#!/bin/bash

if [ -z "$PROJECT_ID" ]; then
  echo "Please provide the project ID: PROJECT_ID"
  exit
fi

echo "Creating cloud task queue..."
gcloud tasks queues create dj-pep-song-player --max-concurrent-dispatches 1 --project $PROJECT_ID
echo "Finished creating cloud task queue"
