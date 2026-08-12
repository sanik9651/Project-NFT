# 🦦 БЫСТРЫЙ ДЕПЛОЙ - Следуй этим шагам!

## ✅ ШАГ 1: GitHub - ГОТОВО!
Код загружен: https://github.com/sanik9651/Project-NFT

---

## 📦 ШАГ 2: Деплой Backend на Render.com

### 2.1 Web Service (API)

1. **Открой:** https://dashboard.render.com/
2. **Нажми:** `New +` → `Web Service`
3. **Connect Repository:** `sanik9651/Project-NFT`
4. **Заполни форму:**

```
Name: nft-transfer-api
Runtime: Python 3
Branch: main
Root Directory: (оставь пустым)
Build Command: pip install -r requirements.txt
Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. **Environment Variables** - нажми `Add Environment Variable`:

```
TELEGRAM_BOT_TOKEN = 8966422942:AAGDNLr3ZuLdP9MBiikVKIKAUlvwNLEplFk
MINI_APP_URL = https://ТВОЙ-FRONTEND.vercel.app
```

(MINI_APP_URL пока оставь так, обновишь после деплоя frontend)

6. **Instance Type:** `Free`
7. **Нажми:** `Create Web Service`
8. **Дождись деплоя** (2-3 минуты)
9. **Скопируй URL** (например `https://nft-transfer-api.onrender.com`)

---

### 2.2 Background Worker (Bot)

1. **На Render нажми:** `New +` → `Background Worker`
2. **Connect Repository:** `sanik9651/Project-NFT`
3. **Заполни форму:**

```
Name: nft-transfer-bot
Runtime: Python 3
Branch: main
Build Command: pip install -r requirements.txt
Start Command: cd backend && python bot.py
```

4. **Environment Variables:**

```
TELEGRAM_BOT_TOKEN = 8966422942:AAGDNLr3ZuLdP9MBiikVKIKAUlvwNLEplFk
MINI_APP_URL = https://ТВОЙ-FRONTEND.vercel.app
```

5. **Instance Type:** `Free`
6. **Нажми:** `Create Background Worker`

---

## 🚀 ШАГ 3: Деплой Frontend на Vercel

### Вариант A: Через Vercel.com (рекомендуется)

1. **Открой:** https://vercel.com/new
2. **Import Git Repository:** найди `sanik9651/Project-NFT`
3. **Configure Project:**

```
Framework Preset: Vite
Root Directory: ./
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

4. **Нажми:** `Deploy`
5. **Дождись деплоя** (1-2 минуты)
6. **Скопируй URL** (например `https://project-nft-xxx.vercel.app`)

### Вариант B: Через CLI (если есть vercel установленный)

```bash
cd "/media/sanik/SSD512GB/PyProjects/Project NFT"
npm install -g vercel
vercel --prod
```

---

## 🔄 ШАГ 4: Обнови MINI_APP_URL

После того как получишь URL от Vercel:

1. **Зайди на Render Dashboard**
2. **Открой `nft-transfer-api`** → Environment
3. **Измени `MINI_APP_URL`** на реальный URL Vercel
4. **Сохрани** (Render автоматически перезапустится)
5. **То же самое** для `nft-transfer-bot`

Пример:
```
MINI_APP_URL = https://project-nft-abc123.vercel.app
```

---

## 🤖 ШАГ 5: Настрой Mini App в BotFather

1. **Открой Telegram** → найди [@BotFather](https://t.me/BotFather)
2. **Отправь:** `/mybots`
3. **Выбери своего бота** (который с токеном `8966422942:...`)
4. **Bot Settings** → **Menu Button**
5. **Configure Menu Button**
6. **Введи URL:** `https://твой-url.vercel.app`
7. **Button text:** `🦦 Open App` или `Transfer NFT`

### Опционально: Добавь команды

Отправь `/setcommands` и выбери бота, затем:

```
start - Получить ссылку для перевода NFT
help - Помощь по использованию
```

---

## ✅ ШАГ 6: ТЕСТИРОВАНИЕ!

1. **Найди бота в Telegram** (через @BotFather можно узнать username)
2. **Отправь `/start`**
3. **Нажми кнопку меню** или открой ссылку
4. **Должно открыться Mini App!**

---

## 🎯 Что должно работать:

- ✅ Бот отвечает на команды
- ✅ Mini App открывается в Telegram
- ✅ Можно подключить TON кошелёк
- ✅ Видно NFT из кошелька
- ✅ Можно отправить NFT одной кнопкой

---

## 🐛 Если что-то не работает:

**Бот не отвечает:**
- Проверь логи на Render в `nft-transfer-bot`
- Убедись что Background Worker запущен (статус Running)

**Mini App не открывается:**
- Проверь что URL в BotFather правильный
- Открой URL в обычном браузере - должен работать

**NFT не загружаются:**
- Подключи кошелёк где есть реальные Telegram NFT
- Проверь консоль браузера (F12)

---

## 📍 Полезные ссылки:

- **GitHub Repo:** https://github.com/sanik9651/Project-NFT
- **Render Dashboard:** https://dashboard.render.com/
- **Vercel Dashboard:** https://vercel.com/dashboard
- **BotFather:** https://t.me/BotFather

---

🦦 **ПРЕЗИДЕНТ-КАПИБАРА, НАЧИНАЙ С ШАГА 2!** 

Код уже на GitHub, теперь просто зайди на Render.com и Vercel.com и следуй инструкциям выше!
