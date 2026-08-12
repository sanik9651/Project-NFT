# 🦦 Telegram NFT Transfer - Инструкция по деплою

## Шаг 1: Загрузка на GitHub

```bash
# Создай новый репозиторий на GitHub.com
# Назови его например: telegram-nft-transfer

# Добавь remote
cd "/media/sanik/SSD512GB/PyProjects/Project NFT"
git remote add origin https://github.com/YOUR_USERNAME/telegram-nft-transfer.git
git push -u origin main
```

## Шаг 2: Деплой Backend на Render.com

### 2.1 Web Service (API)

1. Зайди на https://render.com
2. Нажми **New +** → **Web Service**
3. Подключи GitHub репозиторий `telegram-nft-transfer`
4. Заполни настройки:
   - **Name**: `nft-transfer-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** (Add Secret File или по одной):
   ```
   TELEGRAM_BOT_TOKEN=8966422942:AAGDNLr3ZuLdP9MBiikVKIKAUlvwNLEplFk
   MINI_APP_URL=https://your-frontend.vercel.app
   ```
6. Выбери **Free Plan**
7. Нажми **Create Web Service**
8. Скопируй URL (например `https://nft-transfer-api.onrender.com`)

### 2.2 Background Worker (Bot)

1. На Render нажми **New +** → **Background Worker**
2. Подключи тот же репозиторий
3. Настройки:
   - **Name**: `nft-transfer-bot`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python bot.py`
4. Добавь те же **Environment Variables**:
   ```
   TELEGRAM_BOT_TOKEN=8966422942:AAGDNLr3ZuLdP9MBiikVKIKAUlvwNLEplFk
   MINI_APP_URL=https://your-frontend.vercel.app
   ```
5. Нажми **Create Background Worker**

## Шаг 3: Деплой Frontend на Vercel

### Вариант A: Через сайт Vercel.com

1. Зайди на https://vercel.com
2. Нажми **Add New** → **Project**
3. Import репозиторий `telegram-nft-transfer`
4. Настройки:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Нажми **Deploy**
6. Скопируй URL (например `https://nft-transfer.vercel.app`)

### Вариант B: Через CLI

```bash
npm install -g vercel
cd "/media/sanik/SSD512GB/PyProjects/Project NFT"
vercel --prod
```

## Шаг 4: Обновление конфигурации

### 4.1 Обнови MINI_APP_URL на Render

1. Зайди в **Web Service** (`nft-transfer-api`)
2. **Environment** → измени `MINI_APP_URL` на URL Vercel
3. То же самое для **Background Worker** (`nft-transfer-bot`)
4. Render автоматически перезапустится

### 4.2 Обнови tonconnect-manifest.json

В файле `public/tonconnect-manifest.json` замени:

```json
{
  "url": "https://your-app.vercel.app",
  "name": "NFT Transfer",
  "iconUrl": "https://your-app.vercel.app/icon.png",
  "termsOfUseUrl": "https://your-app.vercel.app/terms",
  "privacyPolicyUrl": "https://your-app.vercel.app/privacy"
}
```

Закоммить и запушить изменения.

## Шаг 5: Настройка Mini App в BotFather

1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь команду `/mybots`
3. Выбери своего бота
4. **Bot Settings** → **Menu Button** → **Edit Menu Button**
5. Укажи URL Mini App: `https://your-app.vercel.app`
6. Название кнопки: `Open App` или `🦦 NFT Transfer`

### Опционально: Добавь команды

```
/setcommands

start - Получить ссылку для перевода NFT
help - Помощь по использованию бота
```

## Шаг 6: Тестирование

1. Найди своего бота в Telegram
2. Отправь `/start`
3. Нажми на кнопку меню или открой ссылку
4. Должно открыться Mini App
5. Попробуй подключить кошелёк

## Готово! 🦦

Теперь можешь:
- Отправлять ссылки на аккаунты с NFT
- Переводить NFT одной кнопкой
- Всё работает автоматически

## Troubleshooting

**Бот не отвечает:**
- Проверь что Background Worker запущен на Render
- Проверь логи в Render Dashboard
- Убедись что токен правильный

**Mini App не открывается:**
- Проверь что URL в BotFather правильный
- Проверь что Frontend задеплоен на Vercel
- Открой URL в браузере, должен показаться интерфейс

**NFT не отображаются:**
- Подключи кошелёк где реально есть Telegram NFT
- Проверь что это NFT из официальной Telegram коллекции
- Проверь консоль браузера (Developer Tools)

## Полезные ссылки

- Render Dashboard: https://dashboard.render.com
- Vercel Dashboard: https://vercel.com/dashboard
- TON Connect Docs: https://docs.ton.org/develop/dapps/ton-connect
- Telegram Mini Apps: https://core.telegram.org/bots/webapps
