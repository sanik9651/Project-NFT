from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")

bot = Bot(token=BOT_TOKEN)

user_addresses = {}

class RecipientRequest(BaseModel):
    user_id: str

class RegisterAddressRequest(BaseModel):
    user_id: int
    address: str

@app.post("/api/get-recipient-address")
async def get_recipient_address(request: RecipientRequest):
    user_id = request.user_id

    if user_id not in user_addresses:
        raise HTTPException(status_code=404, detail="Адрес получателя не найден")

    return {"address": user_addresses[user_id]}

@app.post("/api/register-address")
async def register_address(request: RegisterAddressRequest):
    user_addresses[str(request.user_id)] = request.address
    logger.info(f"Зарегистрирован адрес для пользователя {request.user_id}: {request.address}")
    return {"status": "ok"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
