import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Состояния разговора
LOGIN, PASSWORD, DONE = range(3)

# Словарь для хранения данных пользователя
user_data = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Для начала введите свой логин:")
    return LOGIN

def login(update: Update, context: CallbackContext):
    user_data['login'] = update.message.text
    update.message.reply_text("Теперь введите пароль:")
    return PASSWORD

def password(update: Update, context: CallbackContext):
    user_data['password'] = update.message.text
    update.message.reply_text("Спасибо! Логин и пароль сохранены.")
    return DONE

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Действие отменено.")
    return ConversationHandler.END

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOGIN: [MessageHandler(Filters.text & ~Filters.command, login)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
