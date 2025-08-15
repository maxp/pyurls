#!/bin/bash

curl -v -X POST \
    -d "url=http://ya.ru" \
    http://localhost:8000/api/v1/shorten

echo ""

curl -v -X POST \
    -d "url=http://github.com" \
    http://localhost:8000/api/v1/shorten

echo ""

curl -v -X POST \
    -d "url=https://ya.ru" \
    http://localhost:8000/api/v1/shorten

echo ""
