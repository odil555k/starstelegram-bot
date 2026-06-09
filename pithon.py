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

# Главное меню (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Очищаем состояние ожидания фото, если пользователь вернулся в начало
    context.user_data.clear()

    keyboard = [
        ['Услуги', 'Техподдержка', 'Профиль']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Приветствуем вас в нашем боте! Выберите, что вы хотите:",
        reply_markup=reply_markup
    )


# Обработчик текстовых сообщений и кнопок
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

    # 🔙 НАЗАД
    elif text == 'Назад':
        await start(update, context)

    # 🛠 ТЕХПОДДЕРЖКА
    elif text == 'Техподдержка':
        await update.message.reply_text(
            f"🛠 Техподдержка: {username}\nТех.Поддержка: @KoeiNG_spectaring"
        )

    # 🛒 УСЛУГИ (Выбор между Stars и Премиум)
    elif text == 'Услуги':
        keyboard = [
            ['Stars', 'Премиум'],
            ['Назад']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Что именно вас интересует? Выберите категорию:",
            reply_markup=reply_markup
        )

    # ⭐ НАЖАЛИ STARS (Пакеты звёзд)
    elif text == 'Stars':
        keyboard = [
            ['50 звёзд', '190 звёзд'],
            ['200 звёзд', '300 звёзд'],
            ['400 звёзд', '500 звёзд'],
            ['Назад']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Выберите желаемый пакет Stars:",
            reply_markup=reply_markup
        )

    # 💎 НАЖАЛИ ПРЕМИУМ (Добавили кнопки на 3, 6 месяцев и 1 год)
    elif text == 'Premium' or text == 'Премиум':
        keyboard = [
            ['Премиум на 3 месяца'],
            ['Премиум на 6 месяцев'],
            ['Премиум на 1 год'],
            ['Назад']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Выберите тариф подписки Telegram Premium:",
            reply_markup=reply_markup
        )

    # 💳 ВЫБРАЛИ КОНКРЕТНЫЙ ТОВАР (Звёзды или Любой Премиум)
    elif text in [
        '50 звёзд', '190 звёзд', '200 звёзд', '300 звёзд', '400 звёзд', '500 звёзд',
        'Премиум на 3 месяца', 'Премиум на 6 месяцев', 'Премиум на 1 год'
    ]:
        # Запоминаем, какой товар выбрал пользователь
        context.user_data['selected_item'] = text
        # Включаем режим ожидания скриншота
        context.user_data['waiting_for_photo'] = True

        keyboard = [['Назад']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            f"💳 Чтобы купить {text}, отправьте оплату на реквизиты.\n"
            f"карта.\n"
            f"M/O/K.\n\n"
            f"❗ ПОСЛЕ ОПЛАТЫ ОТПРАВЬТЕ СКРИНШОТ (ФОТО) ПРЯМО СЮДА В ЧАТ.",
            reply_markup=reply_markup
        )

    else:
        await update.message.reply_text("Выберите кнопку из меню 👇")


# 📷 ОБРАБОТЧИК ФОТОГРАФИЙ (Прием чеков и пересылка админу)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "нет username"

    # Проверяем, ждем ли мы фото от этого пользователя
    if context.user_data.get('waiting_for_photo'):
        selected_item = context.user_data.get('selected_item', 'Неизвестный товар')

        # Получаем ID фотографии
        photo_file_id = update.message.photo[-1].file_id

        # 1. Говорим пользователю, что всё принято
        await update.message.reply_text(
            "✅ Ваш скриншот получен! Техподдержка проверит оплату и свяжется с вами.",
        )
        # Сразу возвращаем его в главное меню
        await start(update, context)

        # 2. ОТПРАВЛЯЕМ ФОТО + ТЕКСТ ТЕБЕ (АДМИНУ)
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file_id,
            caption=(
                f"🛒 НОВАЯ ПОКУПКА СО СКРИНШОТОМ!\n\n"
                f"👤 Пользователь: {username}\n"
                f"🆔 ID: {user.id}\n"
                f"🛍 Товар: {selected_item}"
            )
        )
    else:
        await update.message.reply_text("Сначала выберите пакет услуг в меню, чтобы отправить чек.")


# =====================================================================
# 3. РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ В БОТЕ
# =====================================================================
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))


# =====================================================================
# 4. БРОНЕБОЙНЫЙ АСИНХРОННЫЙ ЗАПУСК ДЛЯ RENDER
# =====================================================================
async def start_bot():
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    print("Бот успешно запущен и слушает сообщения!")

    while True:
        await asyncio.sleep(3600)


if __name__ == '__main__':
    print("Бот запускается в облаке...")

    if sys.platform != 'win32':
        try:
            import uvloop

            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()