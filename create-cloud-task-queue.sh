#!/bin/bash

echo "Creating cloud task queue..."
gcloud tasks queues create dj-pep-song-player --max-concurrent-dispatches 1 --project personal-site-staging-a449f
echo "Finished creating cloud task queue"
