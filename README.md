# 🚗 Telegram Car Lottery Bot

A professional Telegram bot that manages a **car lottery system** where users purchase tickets, submit payment proof, and participate in a fair draw.

---

## 📌 Features

* ✅ User registration (name + phone)
* ✅ Payment screenshot submission
* ✅ Admin approval / rejection system
* ✅ Unique ticket generation (no duplicates)
* ✅ Ticket limit (1000 users)
* ✅ Winner draw system
* ✅ Telegram inline buttons for smooth UX

---

## 🧠 How It Works

1. User starts the bot
2. User joins lottery
3. User submits:

   * Full name
   * Phone number
4. User sends payment screenshot
5. Admin reviews payment:

   * ✅ Approve → Ticket assigned
   * ❌ Reject → User notified
6. System assigns **unique ticket (1–1000)**
7. Admin runs `/draw`
8. Winner is selected 🎉

---

## 🏗️ Project Structure

```
car_lottery_bot/
│
├── bot.py          # Main bot runner
├── config.py       # Configuration (token, DB, admin)
├── database.py     # Database connection
├── models.py       # Database tables
├── handlers.py     # User logic
├── admin.py        # Admin logic
├── init_db.py      # Create tables
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Project

```bash
git clone https://github.com/daniel-gebremariam/car-lottery-bot.git
cd car-lottery-bot
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Project

Edit `config.py`:

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_ID = 123456789 # your telegram id (admin)
DATABASE_URL = "postgresql://user:password@localhost/lotterydb"
```

---

### 5. Setup Database

Run once:

```bash
python init_db.py
```

---

### 6. Run Bot

```bash
python bot.py
```

---

## 🗄️ Database Design

### Users Table

| Field       | Description    |
| ----------- | -------------- |
| telegram_id | Unique user ID |
| name        | Full name      |
| phone       | Phone number   |

---

### Tickets Table

| Field             | Description     |
| ----------------- | --------------- |
| ticket_number     | Unique (1–1000) |
| user_id           | Owner           |
| payment_confirmed | True/False      |

---

### Payments Table

| Field              | Description                   |
| ------------------ | ----------------------------- |
| user_id            | User                          |
| screenshot_file_id | Telegram file                 |
| status             | pending / approved / rejected |

---

## 🔐 Security Features

* ✅ Admin-only actions (approve, draw)
* ✅ Unique ticket generation
* ✅ Ticket limit enforcement
* ⚠️ Manual payment verification

---

## 🎯 Commands

### User Commands

```
/start
```

---

### Admin Commands

```
/draw   # Select winner
```

---

## ⚠️ Important Notes

* This system uses **manual payment verification**
* Ensure compliance with local lottery laws
* Recommended to integrate payment APIs for automation

---

## 🚀 Future Improvements

* 🔹 Transparent lottery (hash-based draw)
* 🔹 Admin web dashboard
* 🔹 Payment API integration (Telebirr, CBE)
* 🔹 Real-time ticket counter
* 🔹 Multi-lottery support

---

## 💡 Business Idea

This project can be turned into a **Lottery SaaS Platform**:

* Create lotteries for cars, houses, phones
* Charge platform fee (e.g. 5%)
* Scale to multiple clients

---

## 👨‍💻 Author

**Daniel Gebremariam**

* Telegram Bot Developer
* Backend Developer
* Automation Enthusiast

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🛠️ Improve features
* 💬 Share feedback

---

## 📜 License

MIT License
