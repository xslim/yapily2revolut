#!/bin/sh

API_HOST="http://localhost:5000"

curl -s $API_HOST/yapily/institutions | jq 
