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
    # Очищаем состояние ожидания фото при перезапуске
    context.user_data['waiting_for_photo'] = False

    # Проверяем, какой язык выбран. Если не выбран — ставим русский по умолчанию
    lang = context.user_data.get('lang', 'ru')

    if lang == 'uz':
        keyboard = [['Xizmatlar', 'Texnik yordam', 'Profil'], ['Tilni tanlash']]
        text = "Botimizga xush kelibsiz! O'zingizga kerakli bo'limni tanlang:"
    else:
        keyboard = [['Услуги', 'Техподдержка', 'Профиль'], ['Выбрать язык']]
        text = "Приветствуем вас в нашем боте! Выберите, что вы хотите:"

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=reply_markup)


# Обработчик текстовых сообщений и кнопок
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = f"@{user.username}" if user.username else "нет username"

    # Узнаем текущий язык пользователя
    lang = context.user_data.get('lang', 'ru')

    # 🌐 МЕНЮ ВЫБОРА ЯЗЫКА
    if text in ['Выбрать язык', 'Tilni tanlash']:
        keyboard = [['Русский 🇷🇺', 'O\'zbekcha 🇺🇿'], ['Назад' if lang == 'ru' else 'Orqaga']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        msg = "Выберите язык бота:" if lang == 'ru' else "Bot tilini tanlang:"
        await update.message.reply_text(msg, reply_markup=reply_markup)

    # УСТАНОВКА РУССКОГО ЯЗЫКА
    elif text == 'Русский 🇷🇺':
        context.user_data['lang'] = 'ru'
        await update.message.reply_text("Язык бота успешно изменен на Русский! 🇷🇺")
        await start(update, context)

    # УСТАНОВКА УЗБЕКСКОГО ЯЗЫКА
    elif text == "O'zbekcha 🇺🇿":
        context.user_data['lang'] = 'uz'
        await update.message.reply_text("Bot tili O'zbekchaga muvaffaqiyatli o'zgartirildi! 🇺🇿")
        await start(update, context)

    # 👤 ПРОФИЛЬ (Profil)
    elif text in ['Профиль', 'Profil']:
        back_btn = 'Назад' if lang == 'ru' else 'Orqaga'
        keyboard = [[back_btn]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if lang == 'uz':
            msg = f"👤 Profil:\nID: {user.id}\nIsm: {user.first_name}\nUsername: {username}"
        else:
            msg = f"👤 Профиль:\nID: {user.id}\nИмя: {user.first_name}\nUsername: {username}"

        await update.message.reply_text(msg, reply_markup=reply_markup)

    # 🔙 НАЗАД / ORQAGA
    elif text in ['Назад', 'Orqaga']:
        await start(update, context)

    # 🛠 ТЕХПОДДЕРЖКА (Texnik yordam)
    elif text in ['Техподдержка', 'Texnik yordam']:
        if lang == 'uz':
            msg = f"🛠 Texnik yordam: {username}\nTex.Yordam: @KoeiNG_spectaring"
        else:
            msg = f"🛠 Техподдержка: {username}\nТех.Поддержка: @KoeiNG_spectaring"
        await update.message.reply_text(msg)

    # 🛒 УСЛУГИ / XIZMATLAR
    elif text in ['Услуги', 'Xizmatlar']:
        back_btn = 'Назад' if lang == 'ru' else 'Orqaga'
        keyboard = [
            ['Stars', 'Premium' if lang == 'uz' else 'Премиум'],
            [back_btn]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        msg = "Что именно вас интересует? Выберите категорию:" if lang == 'ru' else "Sizni nima qiziqtiradi? Bo'limni tanlang:"
        await update.message.reply_text(msg, reply_markup=reply_markup)

    # ⭐ STARS (Пакеты звёзд для обоих языков)
    elif text == 'Stars':
        back_btn = 'Назад' if lang == 'ru' else 'Orqaga'
        keyboard = [
            ['50 звёзд', '190 звёзд'],
            ['200 звёзд', '300 звёзд'],
            ['400 звёзд', '500 звёзд'],
            [back_btn]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        msg = "Выберите желаемый пакет Stars:" if lang == 'ru' else "Kerakli Stars paketini tanlang:"
        await update.message.reply_text(msg, reply_markup=reply_markup)

    # 💎 ПРЕМИУМ / PREMIUM
    elif text in ['Премиум', 'Premium']:
        back_btn = 'Назад' if lang == 'ru' else 'Orqaga'
        if lang == 'uz':
            keyboard = [['Premium 3 oyga'], ['Premium 6 oyga'], ['Premium 1 yilga'], [back_btn]]
            msg = "Telegram Premium obuna tarifini tanlang:"
        else:
            keyboard = [['Премиум на 3 месяца'], ['Премиум на 6 месяцев'], ['Премиум на 1 год'], [back_btn]]
            msg = "Выберите тариф подписки Telegram Premium:"

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(msg, reply_markup=reply_markup)

    # 💳 ВЫБРАЛИ КОНКРЕТНЫЙ ТОВАР (Звёзды или Премиум на любом языке)
    elif text in [
        '50 звёзд', '190 звёзд', '200 звёзд', '300 звёзд', '400 звёзд', '500 звёзд',
        'Премиум на 3 месяца', 'Премиум на 6 месяцев', 'Премиум на 1 год',
        'Premium 3 oyga', 'Premium 6 oyga', 'Premium 1 yilga'
    ]:
        context.user_data['selected_item'] = text
        context.user_data['waiting_for_photo'] = True

        back_btn = 'Назад' if lang == 'ru' else 'Orqaga'
        keyboard = [[back_btn]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if lang == 'uz':
            msg = (
                f"💳 {text} sotib olish uchun ko'rsatilgan rekvizitlarga to'lovni yuboring.\n"
                f"karta.\n"
                f"M/O/K.\n\n"
                f"❗ TO'LOVDAN SO'NG CHEK SKRINShOTINI (FOTO) SHU YERGA CHATGA YUBORING."
            )
        else:
            msg = (
                f"💳 Чтобы купить {text}, отправьте оплату на реквизиты.\n"
                f"карта.\n"
                f"M/O/K.\n\n"
                f"❗ ПОСЛЕ ОПЛАТЫ ОТПРАВЬТЕ СКРИНШОТ (ФОТО) ПРЯМО СЮДА В ЧАТ."
            )

        await update.message.reply_text(msg, reply_markup=reply_markup)

    else:
        msg = "Выберите кнопку из меню 👇" if lang == 'ru' else "Menyudan tugmani tanlang 👇"
        await update.message.reply_text(msg)


# 📷 ОБРАБОТЧИК ФОТОГРАФИЙ
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    lang = context.user_data.get('lang', 'ru')

    if context.user_data.get('waiting_for_photo'):
        selected_item = context.user_data.get('selected_item', 'Неизвестный товар')
        photo_file_id = update.message.photo[-1].file_id

        # Ответ пользователю в зависимости от языка
        if lang == 'uz':
            user_msg = "✅ Skrinshootingiz qabul qilindi! Texnik yordam to'lovni tekshirib, siz bilan bog'lanadi."
        else:
            user_msg = "✅ Ваш скриншот получен! Техподдержка проверит оплату и свяжется с вами."

        await update.message.reply_text(user_msg)
        await start(update, context)

        # ОТПРАВКА АДМИНУ (Всегда приходит в одном понятном формате)
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file_id,
            caption=(
                f"🛒 НОВАЯ ПОКУПКА СО СКРИНШОТОМ!\n\n"
                f"👤 Пользователь: {username}\n"
                f"🆔 ID: {user.id}\n"
                f"🛍 Товар: {selected_item}\n"
                f"🌐 Язык бота у юзера: {lang.upper()}"
            )
        )
    else:
        msg = "Сначала выберите пакет услуг в меню, чтобы отправить чек." if lang == 'ru' else "Chek yuborishdan oldin menyudan xizmatni tanlang."
        await update.message.reply_text(msg)


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