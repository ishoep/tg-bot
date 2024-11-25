from django.core.management.base import BaseCommand
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7795385929:AAF98EsKowGgpg9wgEN91qpZZh5x5tLHTcM")

LANGUAGE_SELECTION_IMAGE = "bot/management/commands/images/lang.jpg"
MAIN_MENU_IMAGE = "bot/management/commands/images/menu.jpg"
GAME_MENU_IMAGE = "bot/management/commands/images/games.jpg"

WEBHOOK_URL = f"https://slvdev.pythonanywhere.com/telegram/"

# Асинхронные функции бота
async def delete_previous_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if isinstance(update.callback_query, CallbackQuery):
        chat_id = update.callback_query.message.chat_id

    previous_message_id = context.user_data.get("previous_message_id")
    if previous_message_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=previous_message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    if isinstance(update.callback_query, CallbackQuery):
        try:
            await update.callback_query.message.delete()
        except Exception as e:
            print(f"Error deleting callback message: {e}")

def get_text(context, ru_text, en_text):
    return ru_text if context.user_data.get("language") == "ru" else en_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await delete_previous_message(update, context)

    language_keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)

    with open(LANGUAGE_SELECTION_IMAGE, "rb") as photo:
        message = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="Выберите язык / Choose your language:",
            reply_markup=reply_markup,
        )
        context.user_data["previous_message_id"] = message.message_id

async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await delete_previous_message(update, context)

    if query.data == 'lang_ru':
        context.user_data['language'] = 'ru'
    else:
        context.user_data['language'] = 'en'

    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await delete_previous_message(update, context)
    
    menu_text = get_text(context, "Добро пожаловать в главное меню!", "Welcome to the main menu!")

    main_menu_keyboard = [
        [InlineKeyboardButton(get_text(context, "🎮 Играть", "🎮 Play"), callback_data='play')],
        [InlineKeyboardButton(get_text(context, "👥 Канал", "👥 Channel"), url="https://t.me/txitNGBrugg5MTRi")],
        [InlineKeyboardButton(get_text(context, "🌐 Сменить язык", "🌐 Change Language"), callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    with open(MAIN_MENU_IMAGE, 'rb') as photo:
        message = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=menu_text,
            reply_markup=reply_markup
        )
        context.user_data['previous_message_id'] = message.message_id

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await delete_previous_message(update, context)

    if context.user_data.get('done_subscribing', False):
        await show_games_menu(query, context)
    else:
        message = await query.message.reply_text(
            get_text(
                context,
                "Пожалуйста, отправьте запрос на вступление в наш канал и нажмите 'Готово', чтобы продолжить.",
                "Please send a request to join our channel and click 'Done' to continue."
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(context, "Перейти в канал", "Go to Channel"), url="https://t.me/+txitNGBrugg5MTRi")],
                [InlineKeyboardButton(get_text(context, "Готово", "Done"), callback_data='continue_after_subscribe')],
                [InlineKeyboardButton(get_text(context, "Назад", "Back"), callback_data='show_main_menu')]
            ])
        )
        context.user_data['previous_message_id'] = message.message_id

async def continue_after_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await delete_previous_message(update, context)

    context.user_data['done_subscribing'] = True
    message = await query.message.reply_text(
        get_text(
            context,
            "Спасибо! Теперь вы можете продолжить.",
            "Thank you! You can now continue."
        )
    )
    context.user_data['previous_message_id'] = message.message_id
    
    await asyncio.sleep(2)
    await show_games_menu(query, context)

async def show_games_menu(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = query.message.chat.id
    previous_message_id = context.user_data.get('previous_message_id')
    if previous_message_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=previous_message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    games_keyboard = [
        [
            InlineKeyboardButton("✈️ Aviator", callback_data='game_1'),
            InlineKeyboardButton("🚀 LuckyJet", callback_data='game_2'),
            InlineKeyboardButton("🚗 Speed&Cash", callback_data='game_3')
        ],
        [
            InlineKeyboardButton("💣 Mines", callback_data='game_4'),
            InlineKeyboardButton("👑 Royal Mines", callback_data='game_5'),
            InlineKeyboardButton("🪦 Brawl Pirates", callback_data='game_6')
        ],
        [
            InlineKeyboardButton(get_text(context, "Назад", "Back"), callback_data='show_main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(games_keyboard)

    with open(GAME_MENU_IMAGE, 'rb') as photo:
        message = await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=get_text(context, "Выберите игру:", "Choose a game:"),
            reply_markup=reply_markup
        )
        context.user_data['previous_message_id'] = message.message_id
        
async def game_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await delete_previous_message(update, context)

    selected_game = query.data.split('_')[-1]

    # Имитация проверки на регистрацию
    registration_message = get_text(
        context,
        "👋 Здравствуйте!, Чтобы получить максимальную эффективность от использования данного бота, необходимо выполнить следующие шаги:\n"
        "1. Зарегистрируйте новый аккаунт - если у Вас уже есть аккаунт, пожалуйста, покиньте его и зарегистрируйте новый.\n"
        "2. Используйте промокод ABUZNIK24 при регистрации нового аккаунта. Это важно, так как наш ИИ работает только с новыми аккаунтами.\n"
        "3. После регистрации нажмите на кнопку “Проверить регистрацию”.\n"
        "4. Если Вы не выполните эти шаги, наш бот не сможет добавить Ваш аккаунт в свою базу данных, и предоставляемые им сигналы могут не подойти.\n"
        "Спасибо за понимание!",
        "👋 Hello!, To get the most out of this bot, you need to follow these steps:\n"
        "1. Register a new account - if you already have an account, please leave it and register a new one.\n"
        "2. Use the promo code ABUZNIK24 when registering a new account. This is important, as our AI only works with new accounts.\n"
        "3. After registration, click on the “Check registration” button.\n"
        "4. If you do not follow these steps, our bot will not be able to add your account to its database, and the signals it provides may not be suitable.\n"
        "Thank you for your understanding!"
    )
    registration_keyboard = [
        [InlineKeyboardButton(get_text(context, "Регистрация", "Register"), url="https://1wzvro.top/?open=register&p=pc54")],
        [InlineKeyboardButton(get_text(context, "Проверить регистрацию", "Check Registration"), callback_data='check_registration')],
        [InlineKeyboardButton(get_text(context, "Назад", "Back"), callback_data='go_back')]
    ]
    reply_markup = InlineKeyboardMarkup(registration_keyboard)

    await query.message.reply_text(
        registration_message,
        reply_markup=reply_markup
    )

async def check_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    not_registered_message = get_text(
        context,
        "Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, чтобы продолжить.",
        "You are not registered. Please register to continue."
    )
    
    await query.message.reply_text(not_registered_message)

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await delete_previous_message(update, context)
    await show_games_menu(query, context)

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await delete_previous_message(update, context)
    await start(update, context)

class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **kwargs):
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(language_selected, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_change$"))
        application.add_handler(CallbackQueryHandler(play, pattern="^play$"))
        application.add_handler(CallbackQueryHandler(go_back, pattern="^go_back$"))
        application.add_handler(CallbackQueryHandler(game_selected, pattern="^game_"))
        application.add_handler(CallbackQueryHandler(start, pattern="^start$"))
        application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^show_main_menu$"))
        application.add_handler(CallbackQueryHandler(check_registration, pattern="^check_registration$"))
        application.add_handler(CallbackQueryHandler(continue_after_subscribe, pattern="^continue_after_subscribe$"))

        application.run_polling()

async def set_webhook(application):
    """Устанавливает вебхук для бота."""
    await application.bot.set_webhook(WEBHOOK_URL)