import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# НАСТРОЙКИ БОТА
ADMIN_ID = "6636620529"
TOKEN = "8773682081:AAGdGfefrBQ546rf5fGpNMSWCQAhbrNMFy8"


# ХЕНДЛЕР КОМАНДЫ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['Услуги', 'Техподдержка', 'Профиль']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        text="Приветствуем вас в нашем боте! Выберите, что вы хотите:",
        reply_markup=reply_markup
    )


# ХЕНДЛЕР ТЕКСТОВЫХ СООБЩЕНИЙ (Основная логика)
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = f"@{user.username}" if user.username else "нет username"

    # 👤 ПРОФИЛЬ
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

    # ⬅️ НАЗАД
    elif text == 'Назад':
        await start(update, context)

    # 🛠 ТЕХПОДДЕРЖКА
    elif text == 'Техподдержка':
        await update.message.reply_text(
            f"🛠 Техподдержка: {username}\n"
            f"Тех.Поддержка: @KoeiNG_spectaring"
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
            text="Выберите пакет:",
            reply_markup=reply_markup
        )

    # ⭐️ ПОКУПКИ
    elif text in ['50 звёзд', '100 звёзд', '200 звёзд', '400 звёзд', '500 звёзд']:
        await update.message.reply_text(
            f"💳 Чтобы купить {text}, отправьте оплату на реквизиты.\n"
            f"После оплаты напишите в техподдержку.\n"
            f"Номер карты.\n"
            f"M/O"
        )

        # Уведомление админу (работает строго при покупке)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🛒 НОВАЯ ПОКУПКА!\n"
                f"Пользователь: {username}\n"
                f"ID: {user.id}\n"
                f"Товар: {text}"
            )
        )

    # ЕСЛИ НАПИСАНО ЧТО-ТО ДРУГОЕ
    else:
        await update.message.reply_text("Выберите кнопку из меню 👇")


# ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА БОТА
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    # Исправлено: добавлен await для правильного асинхронного старта
    await app.run_polling()


# ТОЧКА ВХОДА (С правильными отступами)
if __name__ == '__main__':
    main()