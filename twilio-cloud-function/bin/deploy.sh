#!/bin/bash

if [ -z "$FUNCTION_NAME" ]; then
  echo "Please provide the function name: FUNCTION_NAME"
  exit
fi

if [ -z "$ENTRY_POINT" ]; then
  ENTRY_POINT=$FUNCTION_NAME
fi

if [ -z "$GOOGLE_PROJECT_ID" ]; then
  echo "Please provide the project ID: $GOOGLE_PROJECT_ID"
  exit
fi


deploy_command="gcloud functions deploy $FUNCTION_NAME --entry-point $ENTRY_POINT --runtime python37
--trigger-http --project $GOOGLE_PROJECT_ID --set-env-vars
GOOGLE_PROJECT_ID=$GOOGLE_PROJECT_ID,GROUP_ME_BOT_ID=$GROUP_ME_BOT_ID,TWILIO_ACCOUNT_SID=$TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN=$TWILIO_AUTH_TOKEN"

echo "$deploy_command"

$deploy_command
