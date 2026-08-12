# Telegram NFT Transfer Bot

Перевод NFT между Telegram аккаунтами одной кнопкой через Mini App.

## Возможности

- 🦦 Простой перевод NFT между аккаунтами
- 💎 Поддержка всех Telegram NFT на TON блокчейне
- 🔒 Безопасные транзакции через TON Connect
- 📱 Нативный Telegram Mini App интерфейс

## Деплой на Render.com

### 1. Backend API

1. Форкни этот репозиторий
2. Зайди на [render.com](https://render.com)
3. Создай новый **Web Service**
4. Подключи GitHub репозиторий
5. Настройки:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
6. Добавь переменные окружения:
   - `TELEGRAM_BOT_TOKEN` = токен от BotFather
   - `MINI_APP_URL` = (оставь пустым, заполним после деплоя frontend)

### 2. Telegram Bot

1. На Render создай ещё один **Background Worker**
2. Подключи тот же репозиторий
3. Настройки:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python bot.py`
4. Добавь те же переменные окружения

### 3. Frontend (Vercel/Netlify)

**Vercel:**
```bash
npm install -g vercel
vercel
```

**Netlify:**
1. Зайди на [netlify.com](https://netlify.com)
2. Drag & Drop папку `dist/` после билда
3. Или подключи GitHub и настрой:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

### 4. Финальная настройка

1. Скопируй URL frontend приложения (например `https://yourapp.vercel.app`)
2. Обнови `MINI_APP_URL` в переменных Render для бота и API
3. Обнови `public/tonconnect-manifest.json`:
   ```json
   {
     "url": "https://yourapp.vercel.app",
     "name": "NFT Transfer",
     "iconUrl": "https://yourapp.vercel.app/icon.png"
   }
   ```
4. В @BotFather настрой Mini App:
   - `/mybots`
   - Выбери бота
   - Bot Settings → Menu Button → Configure Menu Button
   - Укажи URL: `https://yourapp.vercel.app`

### 5. Настройка бота в BotFather

```
/setdomain - установи свой домен
/setmenubutton - настрой кнопку меню с URL Mini App
/setcommands - добавь команды:
start - Начать работу с ботом
send_nft - Отправить NFT пользователю
```

## Локальная разработка

```bash
# Frontend
npm install
npm run dev

# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Создать .env
echo "TELEGRAM_BOT_TOKEN=your_token" > .env
echo "MINI_APP_URL=http://localhost:3000" >> .env

# Запустить
python backend/main.py  # API на :8000
python backend/bot.py   # Bot
```

## Использование

1. Отправь `/start` боту в основном аккаунте
2. Получи ссылку на Mini App
3. Отправь ссылку на аккаунт с NFT
4. Открой ссылку → подключи кошелёк → отправь NFT

## Технологии

- React + Vite
- TON Connect 2.0
- FastAPI
- python-telegram-bot
- TON Blockchain
