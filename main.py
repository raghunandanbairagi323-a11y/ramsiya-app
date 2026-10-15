import os
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल नया फ्रेश डेटाबेस ताकि पुराना अटकाव हमेशा के लिए साफ़ हो जाए
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_final_ultimate_v999.db")

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
                        id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, 
                        shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, selected_plan TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/login-page")
async def login_page_html():
    # ⚡ नोटपैड में कभी न कटने वाला बिल्कुल छोटा और सीधा स्ट्रक्चर
    html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>रामसिया स्मार्ट ऐप</title><link href="https://jsdelivr.net" rel="stylesheet"></head><body style="background:#f4f6f9;padding:50px;"><div class="container" style="max-width:800px;"><h2 class="text-center text-primary mb-4">🚀 रामसिया स्मार्ट बिलिंग मुख्य सर्वर</h2><div class="row g-4"><div class="col-md-5"><div class="card p-4 shadow-sm"><h4>🔓 लॉगिन (Login)</h4><hr><form action="/login" method="post"><div class="mb-3"><label class="small fw-bold">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="mb-3"><label class="small fw-bold">पासवर्ड</label><input type="password" name="password" class="form-control" required></div><button type="submit" class="btn btn-primary w-100 fw-bold">लॉगिन करें</button></form></div></div><div class="col-md-7"><div class="card p-4 shadow-sm"><h4>✨ नया दुकानदार रजिस्ट्रेशन</h4><hr><form action="/register" method="post"><div class="row g-2"><div class="col-6 mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="col-6 mb-2"><label class="small">पासवर्ड चुनें</label><input type="password" name="password" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control" required></div><div class="col-12 my-2"><label class="small fw-bold">☑️ प्लान चुनें:</label><select name="selected_plan" class="form-select bg-light fw-bold"><option value="1m">1 महीना प्लान (₹{PRICE_1M})</option><option value="3m">3 महीना प्लान (₹{PRICE_3M})</option><option value="6m">6 महीना प्लान (₹{PRICE_6M})</option><option value="9m">9 महीना प्लान (₹{PRICE_9M})</option><option value="12m">12 महीना प्लान (₹{PRICE_12M})</option></select></div></div><button type="submit" class="btn btn-success w-100 fw-bold mt-2">✨ स्टोर एक्टिवेट करें (7 दिन फ्री ट्रायल)</button></form></div></div></div></div></body></html>'
    return HTMLResponse(content=html)

@app.get("/")
async def index(request: Request):
    user_email = request.cookies.get("user_email")
    shop_name = request.cookies.get("shop_name")
    owner_name = request.cookies.get("owner_name")
    if not user_email: return RedirectResponse(url="/login-page", status_code=303)
    html = f'<html><head><title>रामसिया सॉफ़्टवेयर</title><link href="https://jsdelivr.net" rel="stylesheet"></head><body style="background:#f4f6f9;padding:40px;"><div class="card p-4 shadow-sm mx-auto" style="max-width:600px;border-radius:12px;background:white;"><h2 class="text-success fw-bold">🚩 {shop_name} - बिलिंग काउंटर लाइव है!</h2><h5 class="text-muted mt-2">owner: {owner_name} ({user_email})</h5><div class="alert alert-warning my-3">⏳ <strong>आपका 7 दिन का फ्री ट्रायल सफलतापूर्वक चालू हो गया है!</strong></div><p class="text-dark">आपका बिलिंग काउंटर सुरक्षित चालू है।</p><hr><div class="text-muted small">सपोर्ट टीम नंबर: +91 {ADMIN_PHONE}</div><a href="/logout" class="btn btn-danger btn-sm mt-3 fw-bold">🔒 लॉगआउट (Logout)</a></div></body></html>'
    return HTMLResponse(content=html)

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO shopkeepers (email, password, shop_name, owner_name, phone, address, selected_plan) VALUES (?, ?, ?, ?, ?, ?, ?)", (email, password, shop_name, owner_name, phone, address, selected_plan))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "ईमेल आईडी पहले से मौजूद है!"
    conn.close()
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_email", value=email)
    response.set_cookie(key="shop_name", value=shop_name)
    response.set_cookie(key="owner_name", value=owner_name)
    return response

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if email == "admin@ramsiya.com" and password == ADMIN_PASS: return RedirectResponse(url="/ramsiya-office", status_code=303)
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
    return HTMLResponse(content='<html><body><script>alert("गलत ईमेल या पासवर्ड!");window.location.href="/login-page";</script></body></html>')

@app.get("/ramsiya-office")
async def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, shop_name, owner_name, phone, email, selected_plan FROM shopkeepers")
    shops = cursor.fetchall()
    conn.close()
    shops_html = "".join([f"<tr><td>{s[0]}</td><td><strong>{s[1]}</strong></td><td>{s[2]}</td><td>{s[3]}</td><td>{s[4]}</td><td><span class='badge bg-info'>{str(s[5]).upper()}</span></td><td><span class='badge bg-success'>Active</span></td></tr>" for s in shops])
    html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>सुपर एडमिन पैनल</title><link href="https://jsdelivr.net" rel="stylesheet"></head><body style="background:#f8f9fa;padding:30px;"><div class="container-fluid"><h2>🚩 रामसिया सॉफ़्टवेयर हेड ऑफिस (Master Control)</h2><div class="row mt-4"><div class="col-md-4"><div class="card p-4 shadow-sm"><h5>⚙️ हेड ऑफिस मास्टर सेटिंग्स</h5><hr><div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" value="{ADMIN_USER}" class="form-control" readonly></div><div class="mb-2"><label class="small fw-bold">MASTER पासवर्ड</label><input type="text" value="{ADMIN_PASS}" class="form-control" readonly></div><div class="mb-2"><label class="small fw-bold">परमानेंट UPI ID</label><input type="text" value="{ADMIN_UPI}" class="form-control" readonly></div><div class="mb-2"><label class="small fw-bold">हेल्पलाइन</label><input type="text" value="{ADMIN_PHONE}" class="form-control" readonly></div></div></div><div class="col-md-8"><div class="card p-4 shadow-sm"><h5>👥 रजिस्टर्ड दुकानदार लिस्ट (Live)</h5><table class="table table-hover mt-2 small"><thead><tr><th>ID</th><th>दुकान का नाम</th><th>मालिक</th><th>फ़ोन</th><th>ईमेल आईडी</th><th>प्लान</th><th>स्टेटस</th></tr></thead><tbody>{shops_html}</tbody></table></div></div></div></div></body></html>'
    return HTMLResponse(content=html)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login-page", status_code=303)
    response.delete_cookie("user_email")
    response.delete_cookie("shop_name")
    response.delete_cookie("owner_name")
    return response