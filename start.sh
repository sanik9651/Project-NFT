#!/bin/bash

# Запускаем бота в фоне
cd backend
python bot.py &

# Запускаем API
uvicorn main:app --host 0.0.0.0 --port $PORT
