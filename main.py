import os
import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
# 💾 फ्रेश डेटाबेस नाम ताकि पुराना सारा अटकाव परमानेंट साफ़ हो जाए
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_saas_multiplan.db")

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
    cursor.execute("SELECT monthly_price, theme_color, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    admin_data = {"price": adm[0], "color": adm[1], "upi": adm[2], "phone": adm[3]}
    
    cursor.execute("SELECT shop_name, owner_name, phone, address, expiry_date, status, upi_id FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return RedirectResponse(url="/login-page", status_code=303)
        
    shop_data = {"shop_name": user[0], "owner_name": user[1], "phone": user[2], "address": user[3], "upi_id": user[6]}
    lang = request.cookies.get("lang", "hi")
    
    exp_date = datetime.strptime(user[4], "%Y-%m-%d")
    is_locked = datetime.now() > exp_date or user[5] == "locked"
    days_left = max(0, (exp_date - datetime.now()).days)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "shop": shop_data, "is_locked": is_locked, 
        "days_left": days_left, "admin": admin_data, "lang": lang, "products": [], "khatas": []
    })

@app.get("/ramsiya-office")
async def admin_panel(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, price_1m, price_3m, price_6m, price_9m, price_12m, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    admin_data = {"user": adm[0], "pass": adm[1], "p1": adm[2], "p3": adm[3], "p6": adm[4], "p9": adm[5], "p12": adm[6], "upi": adm[7], "phone": adm[8]}
    
    cursor.execute("SELECT id, shop_name, owner_name, phone, expiry_date, status FROM users")
    shops = [{"id": r[0], "shop_name": r[1], "owner_name": r[2], "phone": r[3], "expiry_date": r[4], "status": r[5]} for r in cursor.fetchall()]
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "admin": admin_data, "shops": shops})

@app.post("/register")
async def register_user(request: Request, email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form("1m")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    days_map = {"1m": 30, "3m": 90, "6m": 180, "9m": 270, "12m": 365}
    days = days_map.get(selected_plan, 30)
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    
    try:
        cursor.execute("INSERT INTO users (email, password, shop_name, owner_name, phone, address, expiry_date, status, upi_id, selected_plan) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '', ?)",
                       (email, password, shop_name, owner_name, phone, address, expiry_date, selected_plan))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user_id = cursor.fetchone()[0]
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except sqlite3.IntegrityError:
        return templates.TemplateResponse("login.html", {"request": request, "lang": "hi", "error": "ईमेल आईडी पहले से रजिस्टर है!"})
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
    return RedirectResponse(url="/ramsiya-office", status_code=303)