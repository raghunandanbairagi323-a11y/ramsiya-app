import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# ⚠️ रेंडर सर्वर के लिए बिल्कुल सटीक रास्ता सेट करना
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_data.db")

# --- 💾 डेटाबेस की फाइल और टेबल बनाने का सिस्टम ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS shop (
                        id INTEGER PRIMARY KEY, shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, trial_start TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, stock INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS khata (
                        customer_name TEXT PRIMARY KEY, total_due REAL)''')
    conn.commit()
    conn.close()

init_db()

# 🚀 मुख्य रूट जो रेंडर सर्वर पर 100% सही लोड होगा
@app.get("/")
async def dashboard(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT shop_name, owner_name, phone, address, trial_start FROM shop WHERE id=1")
    shop_row = cursor.fetchone()
    shop = None
    is_locked = False
    days_left = 7
    
    if shop_row:
        shop = {
            "shop_name": shop_row[0],
            "owner_name": shop_row[1],
            "phone": shop_row[2],
            "address": shop_row[3]
        }
        try:
            start_date = datetime.strptime(shop_row[4], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = (datetime.now() - start_date).days
            days_left = 7 - elapsed
            if days_left <= 0:
                is_locked = True
                days_left = 0
        except:
            pass
            
    cursor.execute("SELECT name, price, stock FROM products")
    products = [{"name": r[0], "price": r[1], "stock": r[2]} for r in cursor.fetchall()]
    
    cursor.execute("SELECT customer_name, total_due FROM khata WHERE total_due > 0")
    khatas = {r[0]: r[1] for r in cursor.fetchall()}
    
    conn.close()
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "shop": shop,
            "products": products,
            "khatas": khatas,
            "is_locked": is_locked,
            "days_left": days_left
        }
    )

@app.post("/save-shop")
async def save_shop(shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shop WHERE id=1")
    cursor.execute("INSERT INTO shop (id, shop_name, owner_name, phone, address, trial_start) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, shop_name, owner_name, phone, address, str(datetime.now())))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/add-product")
async def add_product(name: str = Form(...), price: float = Form(...), stock: int = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/add-to-khata")
async def add_to_khata(c_name: str = Form(...), amount: float = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT total_due FROM khata WHERE customer_name=?", (c_name,))
    row = cursor.fetchone()
    if row:
        new_due = row[0] + amount
        cursor.execute("UPDATE khata SET total_due=? WHERE customer_name=?", (new_due, c_name))
    else:
        cursor.execute("INSERT INTO khata (customer_name, total_due) VALUES (?, ?)", (c_name, amount))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/clear-khata")
async def clear_khata(c_name: str = Form(...), amount: float = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT total_due FROM khata WHERE customer_name=?", (c_name,))
    row = cursor.fetchone()
    if row:
        new_due = row[0] - amount
        if new_due < 0: new_due = 0
        cursor.execute("UPDATE khata SET total_due=? WHERE customer_name=?", (new_due, c_name))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)