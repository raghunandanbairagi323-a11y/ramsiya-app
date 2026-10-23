import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल फ्रेश और नया डेटाबेस नाम ताकि पुराना सारा अटकाव हमेशा के लिए साफ़ हो जाए
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_final_perfect_ultimate.db")

# ====================================================================
# 🔑 रघु जी, आपके हेड ऑफिस की मास्टर सेटिंग्स यहाँ लॉक हैं!
# ====================================================================
ADMIN_USER = "admin"
ADMIN_PASS = "Ramsiya@3233"      # ✅ आपका सुपर मास्टर पासवर्ड
PRICE_1M   = "99.0"
PRICE_3M   = "299.0"
PRICE_6M   = "599.0"
PRICE_12M  = "1199.0"
ADMIN_UPI  = "Q378404429@ybl"    # ✅ आपकी असली भुगतान UPI ID
ADMIN_PHONE = "9893753232"       # ✅ आपका असली व्हाट्सएप नंबर
# ====================================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS shopkeepers (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, selected_plan TEXT, reg_date TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS bills (bill_id INTEGER PRIMARY KEY AUTOINCREMENT, shop_email TEXT, customer_name TEXT, customer_phone TEXT, item_name TEXT, amount REAL, bill_date TEXT, payment_mode TEXT, bill_style TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html():
    html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>रामसिया स्मार्ट ऐप</title><link href="https://jsdelivr.net" rel="stylesheet"></head><body style="background:#f4f6f9;padding-top:50px;"><div class="container" style="max-width:850px;"><h2 class="text-center text-primary mb-4 fw-bold">🚀 रामसिया स्मार्ट बिलिंग मुख्य सर्वर</h2><div class="row g-4"><div class="col-md-5"><div class="card p-4 shadow-sm border-0" style="border-radius:12px;"><h4>🔓 लॉगिन (Login)</h4><hr><form action="/login" method="post"><div class="mb-3"><label class="small fw-bold">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="mb-3"><label class="small fw-bold">पासवर्ड</label><input type="password" name="password" class="form-control" required></div><button type="submit" class="btn btn-primary w-100 fw-bold">🔓 लॉगिन करें</button></form></div></div><div class="col-md-7"><div class="card p-4 shadow-sm border-0" style="border-radius:12px;"><h4 class="text-success">✨ नया दुकानदार रजिस्ट्रेशन</h4><hr><form action="/register" method="post"><div class="row g-2"><div class="col-6 mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="col-6 mb-2"><label class="small">पासवर्ड चुनें</label><input type="password" name="password" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control" required></div><div class="col-12 my-2"><label class="small fw-bold">☑️ प्लान चुनें:</label><select name="selected_plan" class="form-select bg-light fw-bold"><option value="1m">1 महीना प्लान (₹{PRICE_1M})</option><option value="3m">3 महीना प्लान (₹{PRICE_3M})</option><option value="6m">6 महीना प्लान (₹{PRICE_6M})</option><option value="12m">12 महीना प्लान (₹{PRICE_12M})</option></select></div></div><button type="submit" class="btn btn-success w-100 fw-bold mt-2">✨ स्टोर एक्टिवेट करें (7 दिन फ्री ट्रायल)</button></form></div></div></div></div></body></html>'
    return html

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_email = request.cookies.get("user_email")
    shop_name = request.cookies.get("shop_name")
    owner_name = request.cookies.get("owner_name")
    if not user_email: return RedirectResponse(url="/login-page", status_code=303)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT phone, address, selected_plan, reg_date FROM shopkeepers WHERE email=?", (user_email,))
    s_info = cursor.fetchone()
    cursor.execute("SELECT bill_id, customer_name, customer_phone, item_name, amount, bill_date, payment_mode, bill_style FROM bills WHERE shop_email=?", (user_email,))
    history = cursor.fetchall()
    conn.close()
    
    phone, address, selected_plan, reg_date = s_info if s_info else ("", "", "1m", "2026-01-01")
    plan_names = {"1m": "1 महीना प्रीमियम", "3m": "3 महीना सुपर", "6m": "6 महीना बम्पर", "12m": "12 महीना लाइफटाइम"}
    plan_prices = {"1m": PRICE_1M, "3m": PRICE_3M, "6m": PRICE_6M, "12m": PRICE_12M}
    
    h_rows = "".join([f"<tr><td>#{b}</td><td>{b}</td><td>{b}</td><td>{b}</td><td class='fw-bold text-primary'>₹{b}</td><td>{b}</td><td><span class='badge bg-dark'>{b}</span></td><td><a href='/view-bill/{b}' target='_blank' class='btn btn-sm btn-outline-secondary py-0'>🖨️ प्रिंट</a></td></tr>" for b in history])