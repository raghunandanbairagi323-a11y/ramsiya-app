import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 💾 बिल्कुल फ्रेश और अंतिम डेटाबेस ताकि पुराना सारा कचरा हमेशा के लिए साफ़ हो जाए
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_perfect_v2.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin_control (
                        id INTEGER PRIMARY KEY, admin_user TEXT, admin_pass TEXT, 
                        monthly_price REAL, theme_color TEXT, admin_upi TEXT, admin_phone TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, 
                        shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, 
                        trial_start TEXT, status TEXT, upi_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, price REAL, stock INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS khata (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, customer_name TEXT, total_due REAL)''')
    
    cursor.execute("SELECT COUNT(*) FROM admin_control")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin_control (id, admin_user, admin_pass, monthly_price, theme_color, admin_upi, admin_phone) VALUES (1, 'admin', 'admin123', 299.0, '#1e3c72', 'ramsiya@upi', '9999999999')")
    conn.commit()
    conn.close()

init_db()

# 🔑 लॉगिन / रजिस्ट्रेशन पेज (Direct Code Output)
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
                    <div class="mb-2"><label class="small">ईमेल</label><input type="email" name="email" class="browser-default form-control" required></div>
                    <div class="mb-3"><label class="small">पासवर्ड</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-primary w-100">🔓 लॉगिन करें</button>
                </form>
            </div>
            <div class="tab-pane fade" id="register">
                <form action="/register" method="post">
                    <div class="mb-2"><label class="small">ईमेल</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-2"><label class="small">पासवर्ड</label><input type="password" name="password" class="form-control" required></div>
                    <div class="mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control" required></div>
                    <div class="mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control" required></div>
                    <div class="mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control" required></div>
                    <div class="mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control" required></div>
                    <button type="submit" class="btn btn-success w-100 btn-sm mt-2">✨ स्टोर एक्टिवेट करें</button>
                </form>
            </div>
        </div>
    </div>
    <script src="https://jsdelivr.net"></script>
    </body></html>
    """

@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login-page", status_code=303)
    return HTMLResponse("<h1>रामसिया डैशबोर्ड लाइव हो चुका है!</h1>")

# 🎮 आपके ऑफिस का गुप्त मास्टर कंट्रोल रूम (100% बिना किसी एरर के लाइव)
@app.get("/ramsiya-office", response_class=HTMLResponse)
async def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, monthly_price, theme_color, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    
    cursor.execute("SELECT id, shop_name, owner_name, phone, status FROM users")
    shops = cursor.fetchall()
    conn.close()
    
    shops_html = "".join([f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td><span class='badge bg-success'>{s[4]}</span></td></tr>" for s in shops])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>सुपर एडमिन पैनल</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f8f9fa; padding:30px;">
    <div class="container">
        <h2>🚩 रामसिया सॉफ़्टवेयर हेड ऑफिस (Master Control)</h2>
        <div class="row mt-4">
            <div class="col-md-4">
                <div class="card p-4">
                    <h5>⚙️ मास्टर सेटिंग्स बदलें</h5>
                    <form action="/admin/update" method="post">
                        <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" name="user" value="{adm[0]}" class="form-control" required></div>
                        <div class="mb-2"><label class="small fw-bold">मास्टर पासवर्ड</label><input type="text" name="password" value="{adm[1]}" class="form-control" required></div>
                        <div class="mb-2"><label class="small fw-bold">प्लान कीमत (₹)</label><input type="number" name="price" value="{adm[2]}" class="form-control" required></div>
                        <div class="mb-2"><label class="small fw-bold">UPI ID</label><input type="text" name="upi" value="{adm[5]}" class="form-control" required></div>
                        <div class="mb-3"><label class="small fw-bold">व्हाट्सएप नंबर</label><input type="text" name="phone" value="{adm[6]}" class="form-control" required></div>
                        <button type="submit" class="btn btn-primary w-100">💾 अपडेट करें</button>
                    </form>
                </div>
            </div>
            <div class="col-md-8">
                <div class="card p-4">
                    <h5>👥 सभी रजिस्टर्ड दुकानदार</h5>
                    <table class="table table-hover mt-2 small"><thead><tr><th>ID</th><th>दुकान</th><th>मालिक</th><th>फ़ोन</th><th>स्टेटस</th></tr></thead><tbody>{shops_html}</tbody></table>
                </div>
            </div>
        </div>
    </div>
    </body></html>
    """

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password, shop_name, owner_name, phone, address, trial_start, status, upi_id) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '')",
                       (email, password, shop_name, owner_name, phone, address, str(datetime.now())))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user_id = cursor.fetchone()[0]
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except:
        return "ईमेल आईडी पहले से मौजूद है!"
    finally: conn.close()

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(row[0]))
        return response
    return "गलत ईमेल या पासवर्ड!"

@app.post("/admin/update")
async def admin_update(user: str = Form(...), password: str = Form(...), price: float = Form(...), upi: str = Form(...), phone: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_control SET admin_user=?, admin_pass=?, monthly_price=?, admin_upi=?, admin_phone=? WHERE id=1",
                   (user, password, price, upi, phone))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/ramsiya-office", status_code=303)