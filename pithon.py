import asyncio
import sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================================================================
# 1. НАСТРОЙКИ И ДАННЫЕ БОТА
# =====================================================================
ADMIN_ID = 6636620529
TOKEN = "8773682081:AAGdGfefrBQ546rf5fGpNMSWCQAhbrNMFy8"

# Создаем приложение бота сразу на верхнем уровне
app = ApplicationBuilder().token(TOKEN).build()


# =====================================================================
# 2. ВСЕ ТВОИ ФУНКЦИИ-ОБРАБОТЧИКИ
# =====================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['Услуги', 'Техподдержка', 'Профиль']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Приветствуем вас в нашем боте! Выберите, что вы хотите:",
        reply_markup=reply_markup
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    username = f"@{user.username}" if user.username else "нет username"

    # 📌 ПРОФИЛЬ
    if text == 'Профиль':
        keyboard = [['Назад']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            f"👤 Профиль:\n"
            f"ID: {user.id}\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}",
            reply_markup=reply_markup
        )

    # 🔙 НАЗАД
    elif text == 'Назад':
        await start(update, context)

    # 🛠 ТЕХПОДДЕРЖКА
    elif text == 'Техподдержка':
        await update.message.reply_text(
            f"🛠 Техподдержка: {username}\nТех.Поддержка: @KoeiNG_spectaring"
        )

    # 🛒 УСЛУГИ
    elif text == 'Услуги':
        keyboard = [
            ['50 звёзд', '100 звёзд'],
            ['200 звёзд', '400 звёзд'],
            ['500 звёзд']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "Выберите пакет:",
            reply_markup=reply_markup
        )

    # ⭐ ПОКУПКИ
    elif text in ['50 звёзд', '100 звёзд', '200 звёзд', '400 звёзд', '500 звёзд']:
        await update.message.reply_text(
            f"💳 Чтобы купить {text}, отправьте оплату на реквизиты.\n"
            f"карта.\n"
            f"M/O/K.\n"
            f"После оплаты напишите в техподдержку."
        )

        # 📩 УВЕДОМЛЕНИЕ АДМИНУ
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🛒 НОВАЯ ПОКУПКА!\n"
                f"Пользователь: {username}\n"
                f"ID: {user.id}\n"
                f"Товар: {text}"
            )
        )

    else:
        await update.message.reply_text("Выберите кнопку из меню 👇")


# =====================================================================
# 3. РЕГИСТРАЦИЯ КОМАНД
# =====================================================================
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))


# =====================================================================
# 4. БРОНЕБОЙНЫЙ АСИНХРОННЫЙ ЗАПУСК ДЛЯ RENDER
# =====================================================================
async def start_bot():
    # Пошагово инициализируем бота без конфликтов встроенных циклов
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    print("Бот успешно запущен и слушает сообщения!")

    # Бесконечный цикл удерживает бота активным в облаке
    while True:
        await asyncio.sleep(3600)


if __name__ == '__main__':
    print("Бот запускается в облаке...")

    # На Linux (Render) настраиваем правильную политику потоков
    if sys.platform != 'win32':
        try:
            import uvloop

            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass

    # Создаем изолированный чистый рабочий цикл событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()