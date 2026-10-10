import os
import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल फ्रेश डेटाबेस नाम ताकि भाषा और प्लान का नया ढांचा सही लोड हो
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_final_v12.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin_control (
                        id INTEGER PRIMARY KEY, admin_user TEXT, admin_pass TEXT, 
                        price_1m REAL, price_3m REAL, price_6m REAL, price_9m REAL, price_12m REAL,
                        admin_upi TEXT, admin_phone TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, 
                        shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, 
                        expiry_date TEXT, status TEXT, upi_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, price REAL, stock INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS khata (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, customer_name TEXT, total_due REAL)''')
    
    cursor.execute("SELECT COUNT(*) FROM admin_control")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO admin_control (id, admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone) VALUES (1, 'admin', 'admin123', 299.0, 799.0, 1499.0, 2199.0, 2999.0, 'ramsiya@upi', '9999999999')")
    conn.commit()
    conn.close()

init_db()

# 🌐 भाषा शब्दकोश (Hindi / English Dictionary)
LANG_DATA = {
    "hi": {
        "title": "रामसिया स्मार्ट बिलिंग", "login": "लॉगिन", "register": "नया दुकानदार रजिस्ट्रेशन",
        "email": "ईमेल आईडी", "pass": "पासवर्ड", "shop": "दुकान का नाम", "owner": "मालिक का नाम",
        "phone": "मोबाइल नंबर", "address": "दुकान का पता", "btn_reg": "✨ स्टोर एक्टिवेट करें",
        "btn_log": "🔓 लॉगिन करें", "dash_title": "डैशボード लाइव है", "exp_msg": "आपका प्लान खत्म होने की तारीख:",
        "stock_title": "📦 स्टॉक एंट्री", "p_name": "सामान का नाम", "p_price": "कीमत (₹)", "p_qty": "मात्रा (Qty)",
        "btn_save": "💾 स्टॉक में सेव करें", "bill_title": "🛒 न्यू बिल काउंटर", "cust_name": "ग्राहक का नाम"
    },
    "en": {
        "title": "Ramsiya Smart Billing", "login": "Login", "register": "New Shop Registration",
        "email": "Email ID", "pass": "Password", "shop": "Shop Name", "owner": "Owner Name",
        "phone": "Mobile Number", "address": "Shop Address", "btn_reg": "✨ Activate Store",
        "btn_log": "🔓 Login Now", "dash_title": "Dashboard is Live", "exp_msg": "Your Plan Expiry Date:",
        "stock_title": "📦 Stock Entry", "p_name": "Product Name", "p_price": "Price (₹)", "p_qty": "Quantity",
        "btn_save": "💾 Save to Stock", "bill_title": "🛒 New Bill Counter", "cust_name": "Customer Name"
    }
}

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html(request: Request):
    lang = request.cookies.get("lang", "hi")
    L = LANG_DATA.get(lang, LANG_DATA["hi"])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head><meta charset="UTF-8"><title>{L['title']}</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; display:flex; align-items:center; justify-content:center; min-height:100vh;">
    <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.05); width:100%; max-width:450px;">
        
        <div class="text-end mb-2">
            <a href="/change-lang/hi" class="btn btn-sm btn-outline-dark">हिंदी</a>
            <a href="/change-lang/en" class="btn btn-sm btn-outline-dark">English</a>
        </div>

        <h3 class="text-center mb-3">🚀 {L['title']}</h3>
        <ul class="nav nav-tabs mb-3" id="myTab">
            <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#login">{L['login']}</button></li>
            <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#register">{L['register']}</button></li>
        </ul>
        <div class="tab-content">
            <div class="tab-pane fade show active" id="login">
                <form action="/login" method="post">
                    <div class="mb-2"><label class="small">{L['email']}</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label class="small">{L['pass']}</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-primary w-100">{L['btn_log']}</button>
                </form>
            </div>
            <div class="tab-pane fade" id="register">
                <form action="/register" method="post">
                    <div class="row g-2">
                        <div class="col-6 mb-2"><label class="small">{L['email']}</label><input type="email" name="email" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">{L['pass']}</label><input type="password" name="password" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">{L['shop']}</label><input type="text" name="shop_name" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">{L['owner']}</label><input type="text" name="owner_name" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">{L['phone']}</label><input type="text" name="phone" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">{L['address']}</label><input type="text" name="address" class="form-control" required></div>
                    </div>
                    <button type="submit" class="btn btn-success w-100 btn-sm mt-2">{L['btn_reg']}</button>
                </form>
            </div>
        </div>
    </div>
    <script src="https://jsdelivr.net"></script>
    </body></html>
    """
    return html_content

@app.get("/change-lang/{lang}")
async def change_lang(lang: str):
    response = RedirectResponse(url="/login-page", status_code=303)
    response.set_cookie(key="lang", value=lang)
    return response

@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login-page", status_code=303)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT shop_name, expiry_date, status FROM users WHERE id=?", (user_id,))
    u = cursor.fetchone()
    conn.close()
    
    if not u:
        return RedirectResponse(url="/login-page", status_code=303)
        
    lang = request.cookies.get("lang", "hi")
    L = LANG_DATA.get(lang, LANG_DATA["hi"])
    
    exp_date = datetime.strptime(u[1], "%Y-%m-%d")
    if datetime.now() > exp_date:
        return HTMLResponse(f"<div style='text-align:center; padding:50px;'><h2>🔒 आपका प्लान समाप्त (Expired) हो गया है!</h2><p>कृपया रिन्यू करने के लिए ऑफिस से संपर्क करें।</p></div>")
        
    return HTMLResponse(f"""
    <body style='font-family:sans-serif; background:#f4f6f9; padding:30px;'>
        <div style='background:white; padding:20px; border-radius:10px; max-width:600px; margin:auto; box-shadow:0 4px 10px rgba(0,0,0,0.05);'>
            <h2>🚀 {u[0]} - {L['dash_title']}</h2>
            <div class='alert alert-warning' style='background:#fff3cd; padding:10px; border-radius:5px; margin:15px 0;'>
                <strong>{L['exp_msg']}</strong> {u[1]}
            </div>
            <hr>
            <h3>{L['stock_title']}</h3>
            <p>{L['p_name']}: <input type='text' class='form-control'></p>
            <p>{L['p_price']}: <input type='number' class='form-control'></p>
            <button style='background:green; color:white; border:none; padding:10px 20px; border-radius:5px;'>{L['btn_save']}</button>
        </div>
    </body>
    """)

@app.get("/ramsiya-office", response_class=HTMLResponse)
async def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    
    cursor.execute("SELECT id, shop_name, owner_name, phone, expiry_date, status FROM users")
    shops = cursor.fetchall()
    conn.close()
    
    shops_html = "".join([f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td><span class='badge bg-info'>{s[4]}</span></td><td>{s[5]}</td></tr>" for s in shops])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>सुपर एडमिन पैनल</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f8f9fa; padding:30px;">
    <div class="container">
        <h2>🚩 रामसिया सॉफ़्टवेयर हेड ऑफिस (Master Control)</h2>
        <div class="row mt-4">
            <div class="col-md-5">
                <div class="card p-4">
                    <h5>⚙️ मास्टर सेटिंग्स और टिक-बॉक्स प्लान</h5>
                    <form action="/admin/update" method="post">
                        <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" name="user" value="{adm[0]}" class="form-control" required></div>