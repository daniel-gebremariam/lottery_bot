import random
from database import get_db
from models import Ticket, Paymetnt
from telegram import Update
from telegram.ext import ContextTypes

def generate_ticket(user_id):

    db = get_db()

    ticket_number = random.randint(1, 1000)

    ticket = Ticket(
        ticket_number=ticket_number,
        user_id=user_id,
        payment_confirmed=True
    )

    db.add(ticket)
    db.commit()

    return ticket_number

def draw_winner():

    db = get_db()

    tickets = db.query(Ticket).all()

    winner = random.choice(tickets)

    return winner.ticket_number

async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    db = get_db()

    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        # Generate unique ticket
        ticket_number = random.randint(1, 1000)

        ticket = Ticket(
            ticket_number=ticket_number,
            user_id=user_id,
            payment_confirmed=True
        )

        db.add(ticket)

        # Update payment status
        payment = db.query(Payment).filter(Payment.user_id == user_id).first()
        payment.status = "approved"

        db.commit()

        # Notify user
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment Approved\nYour ticket: {ticket_number}"
        )

        await query.edit_message_caption("✅ Approved")

    elif data.startswith("reject_"):

        user_id = int(data.split("_")[1])

        payment = db.query(Payment).filter(Payment.user_id == user_id).first()
        payment.status = "rejected"

        db.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment Rejected. Please try again."
        )

        await query.edit_message_caption("❌ Rejected")
