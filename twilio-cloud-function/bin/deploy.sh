#!/bin/bash

if [ -z "$FUNCTION_NAME" ]; then
  echo "Please provide the function name: FUNCTION_NAME"
  exit
fi

if [ -z "$ENTRY_POINT" ]; then
  ENTRY_POINT=$FUNCTION_NAME
fi

if [ -z "$SPOTIFY_CLIENT_ID" ]; then
  echo "Please provide the spotify client ID: $SPOTIFY_CLIENT_ID"
  exit
fi

if [ -z "$SPOTIFY_CLIENT_SECRET" ]; then
  echo "Please provide the spotify client secret: $SPOTIFY_CLIENT_SECRET"
  exit
fi

if [ -z "$GOOGLE_PROJECT_ID" ]; then
  echo "Please provide the project ID: $GOOGLE_PROJECT_ID"
  exit
fi


deploy_command="gcloud functions deploy $FUNCTION_NAME --entry-point $ENTRY_POINT --runtime python37
--trigger-http --project $GOOGLE_PROJECT_ID --set-env-vars
GOOGLE_PROJECT_ID=$GOOGLE_PROJECT_ID,SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET"

echo "$deploy_command"

$deploy_command
