import os
import sqlite3
import urllib.parse
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_qr_final.db")

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
                        expiry_date TEXT, status TEXT, upi_id TEXT, selected_plan TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM admin_control")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO admin_control (id, admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone) VALUES (1, 'admin', 'admin123', 299.0, 799.0, 1499.0, 2199.0, 2999.0, 'ramsiya@upi', '9999999999')")
    conn.commit()
    conn.close()

init_db()

@app.get("/login-page")
async def login_page_html(request: Request):
    lang = request.cookies.get("lang", "hi")
    return templates.TemplateResponse("login.html", {"request": request, "lang": lang, "error": ""})

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
    cursor.execute("SELECT price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    
    cursor.execute("SELECT shop_name, expiry_date, status, selected_plan FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return RedirectResponse(url="/login-page", status_code=303)
        
    shop_name, expiry_date, status, selected_plan = user[0], user[1], user[2], user[3]
    prices = {"1m": adm[0], "3m": adm[1], "6m": adm[2], "9m": adm[3], "12m": adm[4]}
    final_price = prices.get(selected_plan, adm[0])
    admin_upi = adm[5]
    
    exp_date = datetime.strptime(expiry_date, "%Y-%m-%d")
    is_locked = datetime.now() > exp_date or status == "locked"
    days_left = max(0, (exp_date - datetime.now()).days)
    
    if is_locked:
        pay_url = f"upi://pay?pa={admin_upi}&pn=RamsiyaOffice&am={final_price}&cu=INR&tn=Activate_Store_{user_id}"
        qr_api_url = f"https://qrserver.com{urllib.parse.quote(pay_url)}"
        
        return HTMLResponse(f"""
        <html><head><title>🔒 स्टोर लॉक है</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
        <body style="background:#f8f9fa; padding:50px;" class="text-center">
            <div class="card p-5 shadow mx-auto" style="max-width:550px; border-radius:15px;">
                <h2 class="text-danger fw-bold">⚠️ आपका फ्री ट्रायल समाप्त (Expired) हो चुका है!</h2>
                <p class="text-muted mt-2">दुकान का काउंटर दोबारा चालू करने के लिए कृपया नीचे दिए गए QR कोड को किसी भी ऐप से स्कैन करके पेमेंट पूरा करें।</p>
                <div class="alert alert-info my-3"><strong>चुना गयापन:</strong> {selected_plan.upper()} | <strong>भुगतान राशि:</strong> ₹{final_price}</div>
                <div class="my-3"><img src="{qr_api_url}" alt="Payment QR" class="img-fluid border p-2 bg-white shadow-sm" style="border-radius:10px;"></div>
                <div class="fw-bold text-primary mb-3">📍 हमारी UPI ID: {admin_upi}</div>
                <form action="/admin/auto-unlock/{user_id}" method="post">
                    <input type="hidden" name="plan" value="{selected_plan}">
                    <button type="submit" class="btn btn-success w-100 fw-bold py-2">✅ पेमेंट कर दिया है, काउंटर अनलॉक करें</button>
                </form>
            </div>
        </body></html>
        """)
        
    return HTMLResponse(f"""
    <html><head><title>रामसिया सॉफ़्टवेयर</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; padding:40px;">
        <div class="card p-4 shadow-sm mx-auto" style="max-width:700px;">
            <h2 class="text-success">🚀 {shop_name} - बिलिंग काउंटर चालू है!</h2>
            <div class="alert alert-warning my-3">⏳ <strong>आपके प्लान की वैधता बाकी है:</strong> {days_left} दिन (एक्सपायरी डेट: {expiry_date})</div>
            <hr><h3>🛒 न्यू बिल एंट्री</h3><p>काउंटर पूरी तरह काम कर रहा है। माल बेचें, तरक्की करें!</p>
            <a href="/logout" class="btn btn-danger btn-sm mt-3">🔒 लॉगआउट करें</a>
        </div>
    </body></html>
    """)

@app.post("/admin/auto-unlock/{user_id}")
async def auto_unlock_shop(user_id: int, plan: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    days_map = {"1m": 30, "3m": 90, "6m": 180, "9m": 270, "12m": 365}
    days = days_map.get(plan, 30)
    new_expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    cursor.execute("UPDATE users SET expiry_date=?, status='active' WHERE id=?", (new_expiry, user_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/ramsiya-office")
async def admin_panel(request: Request, success_msg: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    
    admin_data = {
        "user": adm[0] if adm else "admin", 
        "pass": adm[1] if adm else "admin123", 
        "p1": adm[2] if adm else 299.0, 
        "p3": adm[3] if adm else 799.0, 
        "p6": adm[4] if adm else 1499.0, 
        "p9": adm[5] if adm else 2199.0, 
        "p12": adm[6] if adm else 2999.0, 
        "upi": adm[7] if adm else "ramsiya@upi", 
        "phone": adm[8] if adm else "9999999999"
    }
    
    cursor.execute("SELECT id, shop_name, owner_name, phone, expiry_date, status FROM users")
    shops = [{"id": r[0], "shop_name": r[1], "owner_name": r[2], "phone": r[3], "expiry_date": r[4], "status": r[5]} for r in cursor.fetchall()]
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "admin": admin_data, "shops": shops, "success_msg": success_msg})

@app.post("/register")
async def register_user(request: Request, email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form("1m")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    trial_expiry = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    try:
        cursor.execute("INSERT INTO users (email, password, shop_name, owner_name, phone, address, expiry_date, status, upi_id, selected_plan) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '', ?)",
                       (email, password, shop_name, owner_name, phone, address, trial_expiry, selected_plan))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user_id = cursor.fetchone()[0]
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except sqlite3.IntegrityError:
        return templates.TemplateResponse("login.html", {"request": request, "lang": "hi", "error": "यह ईमेल आईडी पहले से रजिस्टर है!"})
    finally: conn.close()

@app.post("/login")
async def login_user(request: Request, email: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(row[0]))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "lang": "hi", "error": "गलत ईमेल या पासवर्ड!"})

@app.post("/admin/update")
async def admin_update(user: str = Form(...), password: str = Form(...), p1: float = Form(...), p3: float = Form(...), p6: float = Form(...), p9: float = Form(...), p12: float = Form(...), upi: str = Form(...), phone: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_control SET admin_user=?, admin_pass=?, price_1m=?, price_3m=?, price_6m=?, price_9m=?, price_12m=?, admin_upi=?, admin_phone=? WHERE id=1",
                   (user, password, p1, p3, p6, p9, p12, upi, phone))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/ramsiya-office?success_msg=1", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login-page", status_code=303)
    response.delete_cookie("user_id")
    return response