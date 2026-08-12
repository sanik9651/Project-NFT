# 🦦 ФИНАЛЬНАЯ НАСТРОЙКА

## ✅ Что уже сделано:
- GitHub: https://github.com/sanik9651/Project-NFT
- Frontend: https://projectnft-eight.vercel.app
- Backend: https://project-nft.onrender.com
- URL'ы обновлены в коде

---

## 🔧 ЧТО НУЖНО СДЕЛАТЬ ПРЯМО СЕЙЧАС:

### 1. Обнови Environment Variables на Render.com

**Зайди сюда:** https://dashboard.render.com/

Найди свой сервис `project-nft` и открой:
- **Environment** tab
- Найди переменную `MINI_APP_URL`
- Измени значение на: `https://projectnft-eight.vercel.app`
- **Save Changes**

Render автоматически перезапустится (подожди 1-2 минуты).

**Если у тебя 2 сервиса (Web Service + Background Worker):**
- Обнови `MINI_APP_URL` в обоих!

---

### 2. Vercel - Redeploy

**Зайди сюда:** https://vercel.com/dashboard

1. Найди проект `projectnft-eight` (или как он называется)
2. Открой **Deployments**
3. Нажми **Redeploy** (или он автоматически задеплоится из GitHub)

Или просто подожди 2 минуты - Vercel видит обновления в GitHub и сам задеплоит.

---

### 3. Настрой Mini App в BotFather

**Открой Telegram:**

1. Найди [@BotFather](https://t.me/BotFather)
2. Отправь: `/mybots`
3. Выбери своего бота (с токеном `8966422942:...`)
4. **Bot Settings**
5. **Menu Button**
6. **Configure Menu Button** или **Edit Menu Button**
7. Введи URL: `https://projectnft-eight.vercel.app`
8. Button text: `🦦 Transfer NFT` или `Open App`

**Готово!**

---

### 4. Настрой команды (опционально)

В BotFather отправь: `/setcommands`

Выбери своего бота и введи:

```
start - Получить ссылку для перевода NFT
help - Помощь по использованию бота
```

---

## 🧪 ТЕСТИРОВАНИЕ

1. **Открой своего бота в Telegram**
2. **Отправь `/start`**
3. **Нажми кнопку меню** (внизу, рядом с полем ввода)
4. **Должно открыться Mini App!**

Если всё работает - увидишь интерфейс с кнопкой "Подключить кошелёк".

---

## 🎯 Что теперь работает:

✅ Бот генерирует ссылки на Mini App
✅ Mini App открывается в Telegram
✅ Можно подключить TON кошелёк
✅ NFT загружаются из кошелька
✅ Транзакции отправляются через TON Connect

---

## 📍 Твои URL'ы:

- **Frontend:** https://projectnft-eight.vercel.app
- **Backend:** https://project-nft.onrender.com
- **GitHub:** https://github.com/sanik9651/Project-NFT
- **Bot Token:** `8966422942:AAGDNLr3ZuLdP9MBiikVKIKAUlvwNLEplFk`

---

🦦 **СДЕЛАЙ ТОЛЬКО 3 ШАГА ВЫШЕ И ВСЁ ЗАРАБОТАЕТ!**
