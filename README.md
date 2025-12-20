# 📉 Price Pal — Amazon Price Tracker

Price Pal is a full-stack Amazon price tracking application that lets users monitor product prices and receive email notifications when the price drops below a desired value.

Users can create an account, add Amazon product links, set a target price, and get notified automatically when the price reduces.

## 🚀 Features

- 🔐 Email-based user authentication
- 🛒 Add Amazon product URLs for tracking
- 💰 Set target price per product
- ⏱️ Automated price checking using web scraping (scheduler)
- 📬 Email notifications when price drops
- 📊 Persistent product & user data (Firebase)
- 🌐 Clean web-based UI (React + Tailwind + shadcn)

## 🧠 How It Works (User Flow)

1. User registers / logs in using email
2. User adds an Amazon product link
3. User sets a target price
4. Backend periodically scrapes Amazon price
5. When price ≤ target price: an email notification is sent
6. User can track or remove products anytime

## 🛠️ Tech Stack

Frontend
- React (Vite)
- TypeScript
- Tailwind CSS
- shadcn/ui

Backend
- FastAPI (Python)
- BeautifulSoup (scraping)
- APScheduler (background jobs)
- Firebase (data storage)
- SMTP (email notifications)
## ⚙️ Installation & Setup

### Prerequisites

- Node.js (v18+ recommended)
- Python 3.10+
- Git

### Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate
# Bash/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Environment variables (create `.env` in `backend/` or set in your shell):

```
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
GOOGLE_APPLICATION_CREDENTIALS=./backend/serviceAccountKey.json
```

Note: place your Firebase service account JSON at `backend/serviceAccountKey.json` (do not commit real credentials).

Run the backend:

```bash
uvicorn main:app --reload
# or: python main.py
```

Backend API: http://localhost:8000 — Open docs at http://localhost:8000/docs

### Frontend Setup (React)

From the repository root:

```bash
npm install
npm run dev
```

Frontend dev server (Vite): http://localhost:5173

### Running Both Together

Open two terminals:

- Terminal A: backend (see backend steps)
- Terminal B: frontend (`npm run dev`)

## Helpful Commands

- Install frontend deps: `npm install`
- Start frontend: `npm run dev`
- Build frontend: `npm run build`
- Start backend (dev):

```bash
cd backend
uvicorn main:app --reload
```

- Run backend directly (debug): `python backend/main.py`
