#!/bin/bash
echo "staring application"
uvicorn main:app --host 0.0.0.0 --port 8080 --reload




