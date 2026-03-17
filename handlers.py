from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_db
from models import User, Payment, Ticket
from config import ADMIN_ID, MAX_TICKETS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("Join Lottery", callback_data="join")]
    ]

    await update.message.reply_text(
        "🚗 Car Lottery\n\n"
        "Ticket price: 2000 Birr\n"
        "Total tickets: 1000\n\n"
        "Press Join Lottery",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def join_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    db = get_db()

    total_tickets = db.query(Ticket).count()

    if total_tickets >= MAX_TICKETS:
        await query.message.reply_text("❌ Lottery is full.")
        return

    await query.message.reply_text("Enter your full name:")
    context.user_data["state"] = "name"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db = get_db()
    state = context.user_data.get("state")

    if state == "name":
        context.user_data["name"] = update.message.text
        context.user_data["state"] = "phone"
        await update.message.reply_text("Enter your phone number:")

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

        await update.message.reply_text(
            "Send payment screenshot after paying 2000 Birr."
        )

        context.user_data["state"] = "payment"


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

        keyboard = [[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{telegram_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{telegram_id}")
        ]]

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=f"Payment from user {telegram_id}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text("Payment sent for approval.")
