import random
from database import get_db
from models import Ticket

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
