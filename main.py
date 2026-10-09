import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_master.db")

# 💾 मास्टर डेटाबेस और टेबल सेटअप (SaaS Architecture)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 1. आपके ऑफिस की कंट्रोल टेबल (थीम, दाम, आपका QR)
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin_control (
                        id INTEGER PRIMARY KEY, admin_user TEXT, admin_pass TEXT, 
                        monthly_price REAL, theme_color TEXT, admin_upi TEXT, admin_phone TEXT)''')
    
    # 2. दुकानदारों के लॉगिन और अकाउंट की टेबल
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, 
                        shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, 
                        trial_start TEXT, status TEXT, upi_id TEXT)''')
    
    # 3. सामान (Inventory) की टेबल (हर दुकानदार का सामान उसकी user_id से जुड़ेगा)
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, price REAL, stock INTEGER)''')
    
    # 4. उधारी खाता (Khata) की टेबल
    cursor.execute('''CREATE TABLE IF NOT EXISTS khata (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, customer_name TEXT, total_due REAL)''')
    
    # यदि पहली बार चालू हो रहा है, तो डिफ़ॉल्ट ऑफिस सेटिंग डालना (जिसे आप कभी भी बदल सकते हैं)
    cursor.execute("SELECT COUNT(*) FROM admin_control")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin_control (id, admin_user, admin_pass, monthly_price, theme_color, admin_upi, admin_phone) VALUES (1, 'admin', 'admin123', 299.0, '#1e3c72', 'ramsiya@upi', '9999999999')")
        
    conn.commit()
    conn.close()

init_db()

# 🚀 मुख्य रूट: यदि लॉगिन नहीं है तो लॉगिन पेज, नहीं तो सीधे दुकानदार का डैशबोर्ड
@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ऑफिस की सेटिंग्स (कलर, आपका QR आदि) निकालना
    cursor.execute("SELECT monthly_price, theme_color, admin_upi, admin_phone FROM admin_control WHERE id=1")
    admin = cursor.fetchone()
    admin_data = {"price": admin[0], "color": admin[1], "upi": admin[2], "phone": admin[3]}
    
    # दुकानदार का डेटा निकालना
    cursor.execute("SELECT shop_name, owner_name, phone, address, trial_start, status, upi_id FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        response = RedirectResponse(url="/logout", status_code=303)
        response.delete_cookie("user_id")
        return response
        
    shop_data = {"shop_name": user[0], "owner_name": user[1], "phone": user[2], "address": user[3], "upi_id": user[6]}
    
    # ⏳ 7 दिन का ऑटोमैटिक लॉक चेक
    is_locked = False
    days_left = 7
    if user[5] == "locked":
        is_locked = True
        days_left = 0
    else:
        try:
            start_date = datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = (datetime.now() - start_date).days
            days_left = 7 - elapsed
            if days_left <= 0:
                cursor.execute("UPDATE users SET status='locked' WHERE id=?", (user_id,))
                conn.commit()
                is_locked = True
                days_left = 0
        except: pass

    # सिर्फ इस दुकानदार का स्टॉक निकालना
    cursor.execute("SELECT name, price, stock FROM products WHERE user_id=?", (user_id,))
    products = [{"name": r[0], "price": r[1], "stock": r[2]} for r in cursor.fetchall()]
    
    # सिर्फ इस दुकानदार का खाता निकालना
    cursor.execute("SELECT customer_name, total_due FROM khata WHERE user_id=? AND total_due > 0", (user_id,))
    khatas = [{"customer_name": r[0], "total_due": r[1]} for r in cursor.fetchall()]
    
    conn.close()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "shop": shop_data, "products": products, "khatas": khatas, "is_locked": is_locked, "days_left": days_left, "admin": admin_data}
    )

# 🏢 दुकानदार का रजिस्ट्रेशन (Sign Up)
@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), upi_id: str = Form("")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password, shop_name, owner_name, phone, address, trial_start, status, upi_id) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)",
                       (email, password, shop_name, owner_name, phone, address, str(datetime.now()), upi_id))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user_id = cursor.fetchone()[0]
        conn.close()
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    except sqlite3.IntegrityError:
        conn.close()
        return templates.TemplateResponse("login.html", {"request": request, "error": "यह ईमेल आईडी पहले से रजिस्टर है!"})

# 🔑 दुकानदार लॉगिन
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
    return templates.TemplateResponse("login.html", {"request": request, "error": "गलत ईमेल या पासवर्ड!"})

# 🎮 आपके ऑफिस का सीक्रेट एडमिन पैनल रूट
@app.get("/ramsiya-office")
async def admin_panel(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_user, admin_pass, monthly_price, theme_color, admin_upi, admin_phone FROM admin_control WHERE id=1")
    adm = cursor.fetchone()
    cursor.execute("SELECT id, shop_name, owner_name, phone, status, trial_start FROM users")
    shops = [{"id": r[0], "shop_name": r[1], "owner_name": r[2], "phone": r[3], "status": r[4], "start": r[5]} for r in cursor.fetchall()]
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "admin": adm, "shops": shops})

# ⚙️ आपके ऑफिस द्वारा सेटिंग्स बदलना (पासवर्ड, रंग, दाम आदि)
@app.post("/admin/update")
async def admin_update(user: str = Form(...), password: str = Form(...), price: float = Form(...), color: str = Form(...), upi: str = Form(...), phone: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_control SET admin_user=?, admin_pass=?, monthly_price=?, theme_color=?, admin_upi=?, admin_phone=? WHERE id=1",
                   (user, password, price, color, upi, phone))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/ramsiya-office", status_code=303)

# 🔒 किसी भी दुकानदार को मैन्युअली लॉक/अनलॉक करना
@app.get("/admin/toggle/{shop_id}")
async def toggle_shop(shop_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE id=?", (shop_id,))
    current_status = cursor.fetchone()[0]
    new_status = "locked" if current_status == "active" else "active"
    cursor.execute("UPDATE users SET status=?, trial_start=? WHERE id=?", (new_status, str(datetime.now()), shop_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/ramsiya-office", status_code=303)

@app.post("/add-product")
async def add_product(request: Request, name: str = Form(...), price: float = Form(...), stock: int = Form(...)):
    user_id = request.cookies.get("user_id")
    if user_id:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (user_id, name, price, stock) VALUES (?, ?, ?, ?)", (user_id, name, price, stock))
        conn.commit()
        conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_id")
    return response