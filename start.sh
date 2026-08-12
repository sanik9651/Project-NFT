#!/bin/bash

# Запускаем API с встроенным webhook для бота
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
