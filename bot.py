from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN
from handlers import start, join_lottery, handle_message, handle_photo
from admin import handle_admin_actions, draw_winner

app = Application.builder().token(BOT_TOKEN).build()

# User
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(join_lottery, pattern="join"))

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Admin
app.add_handler(CallbackQueryHandler(handle_admin_actions, pattern="^(approve_|reject_)"))
app.add_handler(CommandHandler("draw", draw_winner))

app.run_polling()
