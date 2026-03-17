from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_db
from models import User
from config import ADMIN_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("Join Lottery", callback_data="join")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚗 Car Lottery\n\n"
        "Ticket price: 2000 Birr\n"
        "Total tickets: 1000\n\n"
        "Press Join Lottery",
        reply_markup=reply_markup
    )

async def join_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "Please send your full name"
    )

    context.user_data["state"] = "name"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    state = context.user_data.get("state")

    if state == "name":
        context.user_data["name"] = update.message.text
        context.user_data["state"] = "phone"

        await update.message.reply_text(
            "Please send your phone number"
        )

    elif state == "phone":

        name = context.user_data["name"]
        phone = update.message.text
        telegram_id = update.message.from_user.id

        user = User(
            telegram_id=telegram_id,
            name=name,
            phone=phone
        )

        db.add(user)
        db.commit()

         # 🔹 Send to admin with buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{telegram_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{telegram_id}")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=f"New Payment\nUser ID: {telegram_id}",
            reply_markup=reply_markup
        )

        await update.message.reply_text(
            "Send payment screenshot after sending 2000 Birr."
        )

        context.user_data["state"] = "payment"

  from models import Payment

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()

    if context.user_data.get("state") == "payment":

        telegram_id = update.message.from_user.id

        photo = update.message.photo[-1].file_id

        payment = Payment(
            user_id=telegram_id,
            screenshot_file_id=photo
        )

        db.add(payment)
        db.commit()

        await update.message.reply_text(
            "Payment received. Waiting for admin approval."
        )
