import os
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल फ्रेश और परमानेंट डेटाबेस ताकि हर दुकानदार का खाता पूरी तरह अलग और सुरक्षित रहे
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_dynamic_saas_final_v200.db")

# ====================================================================
# 🔑 रघु जी, आपके हेड ऑफिस की मास्टर डिटेल्स कोडिंग में परमानेंट लॉक हैं!
# ====================================================================
ADMIN_USER = "admin"
ADMIN_PASS = "Ramsiya@3233"      # ✅ आपका सुपर मास्टर पासवर्ड
PRICE_1M   = "99.0"
PRICE_3M   = "299.0"
PRICE_6M   = "599.0"
PRICE_9M   = "899.0"
PRICE_12M  = "1199.0"
ADMIN_UPI  = "Q378404429@ybl"    # ✅ आपकी असली भुगतान UPI ID
ADMIN_PHONE = "9893753232"       # ✅ आपका असली व्हाट्सएप नंबर
# ====================================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS shopkeepers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        email TEXT UNIQUE, 
                        password TEXT, 
                        shop_name TEXT, 
                        owner_name TEXT, 
                        phone TEXT, 
                        address TEXT,
                        selected_plan TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html():
    # ⚡ नोटपैड में कभी न कटने वाला बिल्कुल सीधा और आसान स्ट्रक्चर
    return f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8"><title>रामसिया स्मार्ट ऐप</title>
        <link href="https://jsdelivr.net" rel="stylesheet">
    </head>
    <body style="background: #f4f6f9; padding-top: 50px;">
    <div class="container" style="max-width: 900px;">
        <h2 class="text-center mb-4 fw-bold text-primary">🚀 रामसिया स्मार्ट बिलिंग मुख्य सर्वर</h2>
        <div class="row g-4">
            <div class="col-md-5">
                <div class="card p-4 shadow-sm border-0" style="border-radius: 12px; background: white;">
                    <h4 class="mb-3 text-dark fw-bold">🔓 दुकानदार लॉगिन (Login)</h4><hr>
                    <form action="/login" method="post">
                        <div class="mb-3"><label class="small fw-bold">ईमेल आईडी (Email)</label><input type="email" name="email" class="form-control" required></div>
                        <div class="mb-3"><label class="small fw-bold">पासवर्ड (Password)</label><input type="password" name="password" class="form-control" required></div>
                        <button type="submit" class="btn btn-primary w-100 py-2 fw-bold mt-2">🔓 लॉगिन करें</button>
                    </form>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card p-4 shadow-sm border-0" style="border-radius: 12px; background: white;">
                    <h4 class="mb-3 text-success fw-bold">✨ नया दुकानदार रजिस्ट्रेशन (Register)</h4><hr>
                    <form action="/register" method="post">
                        <div class="row g-2">
                            <div class="col-6 mb-2"><label class="small fw-bold">ईमेल आईडी</label><input type="email" name="email" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">पासवर्ड चुनें</label><input type="password" name="password" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">दुकान का नाम</label><input type="text" name="shop_name" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">मालिक का नाम</label><input type="text" name="owner_name" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">दुकान का पता</label><input type="text" name="address" class="form-control form-control-sm" required></div>
                            <div class="col-12 my-2"><label class="small fw-bold text-secondary">☑️ अपना बेस्ट प्लान चुनें (Select Plan):</label>
                                <select name="selected_plan" class="form-select form-select-sm bg-light fw-bold">
                                    <option value="1m">1 महीना प्लान (₹{PRICE_1M})</option>
                                    <option value="3m">3 महीना प्लान (₹{PRICE_3M})</option>
                                    <option value="6m">6 महीना प्लान (₹{PRICE_6M})</option>
                                    <option value="9m">9 महीना प्लान (₹{PRICE_9M})</option>
                                    <option value="12m">12 महीना प्लान (₹{PRICE_12M})</option>
                                </select>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-success w-100 fw-bold py-2 mt-3">✨ स्टोर एक्टिवेट करें (7 दिन फ्री ट्रायल)</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """

@app.get("/")
async def index(request: Request):
    user_email = request.cookies.get("user_email")
    shop_name = request.cookies.get("shop_name")
    owner_name = request.cookies.get("owner_name")
    if not user_email:
        return RedirectResponse(url="/login-page", status_code=303)
        
    return HTMLResponse(f"""
    <html><head><title>रामसिया सॉफ़्टवेयर</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; padding:40px;"><div class="card p-4 shadow-sm mx-auto" style="max-width:600px; border-radius:12px; background:white;">
        <h2 class="text-success fw-bold">🚩 {shop_name} - बिलिंग काउंटर लाइव है!</h2>
        <h5 class="text-muted mt-2">दुकानदार का नाम: {owner_name} ({user_email})</h5>
        <div class="alert alert-warning my-3">⏳ <strong><b>आपका 7 दिन का फ्री ट्रायल सफलतापूर्वक चालू हो गया है!</b></strong></div>
        <p class="text-dark">आपका बिलिंग काउंटर पूरी तरह अलग और सुरक्षित है। माल बेचें, तरक्की करें!</p><hr>
        <div class="text-muted small">सॉफ़्टवेयर हेड ऑफिस सपोर्ट टीम: +91 {ADMIN_PHONE}</div>
        <a href="/logout" class="btn btn-danger btn-sm mt-3 fw-bold">🔒 लॉगआउट करें (Logout)</a>
    </div></body></html>
    """)

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO shopkeepers (email, password, shop_name, owner_name, phone, address, selected_plan) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (email, password, shop_name, owner_name, phone, address, selected_plan))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "यह ईमेल आईडी पहले से रजिस्टर है!"
    conn.close()
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_email", value=email)
    response.set_cookie(key="shop_name", value=shop_name)
    response.set_cookie(key="owner_name", value=owner_name)
    return response

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if email == "admin@ramsiya.com" and password == ADMIN_PASS:
        return RedirectResponse(url="/ramsiya-office", status_code=303)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT shop_name, owner_name FROM shopkeepers WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_email", value=email)
        response.set_cookie(key="shop_name", value=str(row[0]))
        response.set_cookie(key="owner_name", value=str(row[1]))
        return response
    return HTMLResponse(content='<html><body><script>alert("गलत ईमेल या पासवर्ड! कृपया दोबारा जाँचें।"); window.location.href="/login-page";</script></body></html>')

@app.get("/ramsiya-office", response_class=HTMLResponse)
async def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, shop_name, owner_name, phone, email, selected_plan FROM shopkeepers")
    shops = cursor.fetchall()
    conn.close()
    
    shops_html = ""
    for s in shops:
        shops_html += f"<tr><td>{s[0]}</td><td><strong>{s[1]}</strong></td><td>{s[2]}</td><td>{s[3]}</td><td>{s[4]}</td><td><span class='badge bg-info'>{str(s[5]).upper()}</span></td><td><span class='badge bg-success'>Active</span></td></tr>"
    
    return f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>सुपर एडमिन पैनल</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f8f9fa; padding:30px;"><div class="container-fluid"><h2>🚩 रामसिया सॉफ़्टवेयर हेड ऑफिस (Master Control)</h2><div class="row mt-4">
    <div class="col-md-4"><div class="card p-4 shadow-sm"><h5>⚙️ हेड ऑफिस मास्टर सेटिंग्स</h5><hr>
    <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" value="{ADMIN_USER}" class="form-control" readonly></div>