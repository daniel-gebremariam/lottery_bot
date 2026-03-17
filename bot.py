from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN
from handlers import start, join_lottery, handle_message, handle_photo

from admin import handle_admin_actions

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(join_lottery, pattern="join"))

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.add_handler(CallbackQueryHandler(handle_admin_actions, pattern="^(approve_|reject_)"))

app.run_polling()
