from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import func
import random

from database import get_db
from models import Ticket, Payment
from config import ADMIN_ID, MAX_TICKETS


def get_next_ticket_number(db):
    last_ticket = db.query(func.max(Ticket.ticket_number)).scalar()
    return (last_ticket or 0) + 1


async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if update.effective_user.id != ADMIN_ID:
        return

    db = get_db()
    data = query.data

    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        ticket_number = get_next_ticket_number(db)

        if ticket_number > MAX_TICKETS:
            await query.edit_message_caption("❌ Lottery Full")
            return

        ticket = Ticket(
            ticket_number=ticket_number,
            user_id=user_id,
            payment_confirmed=True
        )

        db.add(ticket)

        payment = db.query(Payment).filter(Payment.user_id == user_id).first()
        payment.status = "approved"

        db.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Approved! Your ticket: {ticket_number}"
        )

        await query.edit_message_caption(f"✅ Approved\nTicket: {ticket_number}")

    elif data.startswith("reject_"):

        user_id = int(data.split("_")[1])

        payment = db.query(Payment).filter(Payment.user_id == user_id).first()
        payment.status = "rejected"

        db.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment rejected. Try again."
        )

        await query.edit_message_caption("❌ Rejected")


async def draw_winner(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Not authorized")
        return

    db = get_db()

    tickets = db.query(Ticket).all()

    if len(tickets) == 0:
        await update.message.reply_text("No tickets sold.")
        return

    winner = random.choice(tickets)

    await update.message.reply_text(
        f"🎉 Winner!\nTicket: {winner.ticket_number}"
    )

    await context.bot.send_message(
        chat_id=winner.user_id,
        text="🎉 Congratulations! You won!"
    )
