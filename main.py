import os
import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल फ्रेश डेटाबेस नाम ताकि सारा नया रीडायरेक्ट ढांचा एकदम नया और साफ लोड हो
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_final_perfect_v130.db")

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

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head><meta charset="UTF-8"><title>लॉगिन - रामसिया स्मार्ट ऐप</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; display:flex; align-items:center; justify-content:center; min-height:100vh;">
    <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.05); width:100%; max-width:450px;">
        <h3 class="text-center mb-3">🚀 रामसिया स्मार्ट बिलिंग</h3>
        <ul class="nav nav-tabs mb-3" id="myTab">
            <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#login">लॉगिन</button></li>
            <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#register">रजिस्ट्रेशन</button></li>
        </ul>
        <div class="tab-content">
            <div class="tab-pane fade show active" id="login">
                <form action="/login" method="post">
                    <div class="mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label class="small">पासवर्ड</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-primary w-100">🔓 लॉगिन करें</button>
                </form>
            </div>
            <div class="tab-pane fade" id="register">
                <form action="/register" method="post">
                    <div class="row g-2">
                        <div class="col-6 mb-2"><label class="small">ईमेल</label><input type="email" name="email" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">पासवर्ड</label><input type="password" name="password" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control" required></div>
                        <div class="col-6 mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control" required></div>
                    </div>
                    <button type="submit" class="btn btn-success w-100 btn-sm mt-2">✨ स्टोर एक्टिवेट करें</button>
                </form>
            </div>
        </div>
    </div>
    </body></html>
    """

@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login-page", status_code=303)
    return HTMLResponse("<h1>🚀 रामसिया स्मार्ट बिलिंग मुख्य डैशबोर्ड चालू है!</h1>")

# 🎮 आपके ऑफिस का गुप्त मास्टर कंट्रोल रूम (100% स्वतंत्र कोडिंग)
@app.get("/ramsiya-office", response_class=HTMLResponse)
async def admin_panel(success_msg: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    
    u_name = adm[0] if adm else "admin"
    u_pass = adm[1] if adm else "admin123"
    p1 = adm[2] if adm else 299.0
    p3 = adm[3] if adm else 799.0
    p6 = adm[4] if adm else 1499.0
    p9 = adm[5] if adm else 2199.0
    p12 = adm[6] if adm else 2999.0
    u_upi = adm[7] if adm else "ramsiya@upi"
    u_phone = adm[8] if adm else "9999999999"
    
    cursor.execute("SELECT id, shop_name, owner_name, phone, expiry_date, status FROM users")
    shops = cursor.fetchall()
    conn.close()
    
    shops_html = "".join([f"<tr><td>{s[0]}</td><td><strong>{s[1]}</strong></td><td>{s[2]}</td><td>{s[3]}</td><td><span class='badge bg-warning text-dark'>{s[4]}</span></td><td><span class='badge bg-success'>{s[5]}</span></td></tr>" for s in shops])
    
    alert_html = '<div class="alert alert-success fw-bold">🚩 बहुत-बहुत बधाई! आपकी सभी मास्टर सेटिंग्स और नया पासवर्ड सफलतापूर्वक (SUCCESS) सेव हो चुका है!</div>' if success_msg == "1" else ""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>सुपर एडमिन पैनल</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f8f9fa; padding:30px;">
    <div class="container">
        <h2>🚩 रामसिया सॉफ़्टवेयर हेड ऑफिस (Master Control)</h2>
        {alert_html}
        <div class="row mt-4">
            <div class="col-md-5">
                <div class="card p-4 shadow-sm">
                    <h5>⚙️ मास्टर सेटिंग्स और टिक-बॉक्स प्लान</h5>
                    <form action="/admin/update" method="post">
                        <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" name="user" value="{u_name}" class="form-control form-control-sm" required></div>
                        <div class="mb-2"><label class="small fw-bold">मास्टर पासवर्ड</label><input type="text" name="password" value="{u_pass}" class="form-control form-control-sm" required></div>
                        
                        <label class="small fw-bold d-block mb-1">☑️ प्लान और कीमतें (Select Prices):</label>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">1 Month (₹)</span><input type="number" name="p1" value="{p1}" class="form-control"></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">3 Month (₹)</span><input type="number" name="p3" value="{p3}" class="form-control"></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">6 Month (₹)</span><input type="number" name="p6" value="{p6}" class="form-control"></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">9 Month (₹)</span><input type="number" name="p9" value="{p9}" class="form-control"></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">12 Month (₹)</span><input type="number" name="p12" value="{p12}" class="form-control"></div>

                        <div class="mb-2"><label class="small fw-bold">UPI ID</label><input type="text" name="upi" value="{u_upi}" class="form-control form-control-sm" required></div>
                        <div class="mb-3"><label class="small fw-bold">व्हाट्सएप नंबर</label><input type="text" name="phone" value="{u_phone}" class="form-control form-control-sm" required></div>
                        <button type="submit" class="btn btn-primary w-100 btn-sm">💾 सभी प्लान अपडेट करें</button>
                    </form>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card p-4 shadow-sm">
                    <h5>👥 सभी रजिस्टर्ड दुकानदार (तारीख के साथ)</h5>
                    <table class="table table-hover mt-2 small"><thead><tr><th>ID</th><th>दुकान</th><th>मालिक</th><th>फ़ोन</th><th>एक्सपायरी डेट</th><th>स्टेटस</th></tr></thead><tbody>{shops_html}</tbody></table>
                </div>
            </div>
        </div>
    </div>
    </body></html>
    """
    return html_content

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    trial_expiry = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return "ईमेल आईडी पहले से मौजूद है!"
        cursor.execute("INSERT INTO users (email, password, shop_name, owner_name, phone, address, expiry_date, status, upi_id, selected_plan) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '', '1m')",