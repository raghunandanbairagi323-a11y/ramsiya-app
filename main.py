import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, "ramsiya_ultimate_billing_v9.db")

ADMIN_USER = "admin"
ADMIN_PASS = "Ramsiya@3233"      # ✅ आपका सुपर मास्टर पासवर्ड
ADMIN_UPI  = "Q378404429@ybl"    # ✅ आपकी असली भुगतान UPI ID
ADMIN_PHONE = "9893753232"       # ✅ आपका असली व्हाट्सएप नंबर

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS shopkeepers (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, shop_name TEXT, owner_name TEXT, phone TEXT, address TEXT, selected_plan TEXT, reg_date TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS bills (bill_id INTEGER PRIMARY KEY AUTOINCREMENT, shop_email TEXT, customer_name TEXT, customer_phone TEXT, item_name TEXT, amount REAL, bill_date TEXT, payment_mode TEXT, bill_style TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.get("/login-page")
async def login_page_html():
    # ⚡ ट्रिपल कोटेशन का झंझट हमेशा के लिए खत्म - फ्लैट पार्ट्स लिस्ट
    parts = [
        '<!DOCTYPE html><html lang="hi"><head><meta charset="UTF-8"><title>रामसिया स्मार्ट ऐप</title><link href="https://jsdelivr.net" rel="stylesheet"></head>',
        '<body style="background:#f4f6f9;padding-top:50px;"><div class="container" style="max-width:850px;"><h2 class="text-center text-primary mb-4 fw-bold">🚀 रामसिया स्मार्ट बिलिंग मुख्य सर्वर</h2><div class="row g-4">',
        '<div class="col-md-5"><div class="card p-4 shadow-sm border-0" style="border-radius:12px;"><h4>🔓 लॉगिन (Login)</h4><hr><form action="/login" method="post"><div class="mb-3"><label class="small fw-bold">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="mb-3"><label class="small fw-bold">पासवर्ड</label><input type="password" name="password" class="form-control" required></div><button type="submit" class="btn btn-primary w-100 fw-bold">🔓 लॉगिन करें</button></form></div></div>',
        '<div class="col-md-7"><div class="card p-4 shadow-sm border-0" style="border-radius:12px;"><h4 class="text-success">✨ नया दुकानदार रजिस्ट्रेशन</h4><hr><form action="/register" method="post"><div class="row g-2"><div class="col-6 mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div><div class="col-6 mb-2"><label class="small">पासवर्ड चुनें</label><input type="password" name="password" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control" required></div><div class="col-6 mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control" required></div><div class="col-6 mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control" required></div><div class="col-12 my-2"><label class="small fw-bold">☑️ प्लान चुनें:</label><select name="selected_plan" class="form-select bg-light fw-bold"><option value="1m">1 महीना प्लान (₹99.0)</option><option value="3m">3 महीना प्लान (₹299.0)</option><option value="6m">6 महीना प्लान (₹599.0)</option><option value="12m">12 महीना प्लान (₹1199.0)</option></select></div></div><button type="submit" class="btn btn-success w-100 fw-bold mt-2">✨ स्टोर एक्टिवेट करें (7 दिन फ्री ट्रायल)</button></form></div></div>',
        '</div></div></body></html>'
    ]
    return HTMLResponse(content="".join(parts))

@app.get("/")
async def index(request: Request):
    user_email = request.cookies.get("user_email")
    if not user_email: return RedirectResponse(url="/login-page", status_code=303)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT shop_name, owner_name, phone, address, selected_plan, reg_date FROM shopkeepers WHERE email=?", (user_email,))
    s_info = cursor.fetchone()
    cursor.execute("SELECT bill_id, customer_name, customer_phone, item_name, amount, bill_date, payment_mode, bill_style FROM bills WHERE shop_email=?", (user_email,))
    history = cursor.fetchall()
    conn.close()
    shop_name, owner_name, phone, address, selected_plan, reg_date = s_info if s_info else ("रामसिया स्टोर", "दुकानदार", "", "", "1m", "2026-01-01")
    plan_names = {"1m": "1 महीना प्रीमियम", "3m": "3 महीना सुपर", "6m": "6 महीना बम्पर", "12m": "12 महीना लाइफटाइम"}
    plan_prices = {"1m": "99.0", "3m": "299.0", "6m": "599.0", "12m": "1199.0"}
    h_rows = "".join([f"<tr><td>#{b[0]}</td><td>{b[1]}</td><td>{b[2]}</td><td>{b[3]}</td><td class='fw-bold text-primary'>₹{b[4]}</td><td>{b[5]}</td><td><span class='badge bg-dark'>{b[6]}</span></td><td><a href='/view-bill/{b[0]}' target='_blank' class='btn btn-sm btn-outline-secondary py-0'>🖨️ प्रिंट</a></td></tr>" for b in history])
    parts = [
        f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{shop_name}</title><link href="https://jsdelivr.net" rel="stylesheet"></head><body>',
        f'<nav class="navbar px-4 py-2 shadow-sm d-flex justify-content-between style" style="background:#4e73df;color:white;"><span class="navbar-brand mb-0 h1 fw-bold text-white">🚩 {shop_name} - स्मार्ट बिलिंग रूम</span><div class="text-white small fw-bold">👤 मालिक: {owner_name} | ⏳ 7 दिन ट्रायल लाइव | <a href="/logout" class="btn btn-sm btn-danger fw-bold ms-2">🔒 लॉगआउट</a></div></nav>',
        '<div class="container-fluid mt-4"><div class="row"><div class="col-md-4"><div class="card p-4 shadow-sm border-0 mb-4" style="border-radius:12px;"><h5>🛒 न्यू bill एंट्री</h5><hr><form action="/create-bill" method="post"><div class="mb-2"><label class="small fw-bold">ग्राहक का नाम</label><input type="text" name="c_name" class="form-control form-control-sm" required></div><div class="mb-2"><label class="small fw-bold">ग्राहक का मोबाइल</label><input type="text" name="c_phone" class="form-control form-control-sm" required></div><div class="mb-2"><label class="small fw-bold">सामान का विवरण</label><input type="text" name="item" class="form-control form-control-sm" required></div><div class="mb-2"><label class="small fw-bold">कुल राशि (₹)</label><input type="number" step="0.01" name="amount" class="form-control form-control-sm" required></div><div class="mb-3"><label class="small fw-bold">पेमेंट मोड</label><select name="pay_mode" class="form-select form-select-sm"><option value="Cash">Cash</option><option value="UPI">UPI</option><option value="Udhaar">Udhaar</option></select></div><div class="mb-3"><label class="small fw-bold text-success">🎨 बिल थीम (6 डिज़ाइन)</label><select name="bill_style" class="form-select form-select-sm bg-light fw-bold text-success"><option value="classic">Classic Blue</option><option value="emerald">Emerald Green</option><option value="royal">Royal Purple</option><option value="sunset">Sunset Orange</option><option value="charcoal">Charcoal Dark</option><option value="crimson">Crimson Red</option></select></div><button type="submit" class="btn btn-primary w-100 fw-bold">✨ बिल जनरेट करें</button></form></div></div>',
        f'<div class="col-md-5"><div class="card p-4 shadow-sm border-0 mb-4" style="border-radius:12px; min-height: 480px;"><h5>👤 ग्राहक प्रोफ़ाइल और पेमेंट इतिहास</h5><hr><div class="table-responsive small"><table class="table table-hover align-middle"><thead><tr><th>ID</th><th>ग्राहक</th><th>सामान</th><th>राशी</th><th>माध्यम</th><th>एक्शन</th></tr></thead><tbody>{h_rows if h_rows else "<tr><td colspan='6' class='text-center text-muted'>कोई एंट्री नहीं। पहला बिल बनाएं!</td></tr>"}</tbody></table></div></div></div>',
        f'<div class="col-md-3"><div class="card shadow-sm border-0 mb-4" style="border-radius:12px;"><div class="card-header fw-bold text-primary">⚙️ प्रोफाइल सेटिंग्स</div><div class="card-body small"><form action="/update-profile" method="post"><div class="mb-2"><label class="fw-bold text-muted">दुकान</label><input type="text" name="s_name" value="{shop_name}" class="form-control form-control-sm" required></div><div class="mb-2"><label class="fw-bold text-muted">मालिक</label><input type="text" name="o_name" value="{owner_name}" class="form-control form-control-sm" required></div><div class="mb-2"><label class="fw-bold text-muted">फ़ोन</label><input type="text" name="s_phone" value="{phone}" class="form-control form-control-sm" required></div><div class="mb-3"><label class="fw-bold text-muted">पता</label><input type="text" name="s_addr" value="{address}" class="form-control form-control-sm" required></div><button type="submit" class="btn btn-sm btn-success w-100 fw-bold">💾 अपडेट करें</button></form></div></div>',
        f'<div class="card shadow-sm border-0" style="border-radius:12px;"><div class="card-header fw-bold text-success">📜 खरीदे गए पैक हिस्ट्री</div><div class="card-body small"><div class="p-2 bg-light rounded border"><div class="d-flex justify-content-between mb-1"><strong>पैक:</strong> <span class="text-primary fw-bold">{plan_names.get(selected_plan, "फ्री ट्रायल")}</span></div><div class="d-flex justify-content-between mb-1"><strong>कीमत:</strong> <span class="fw-bold text-success">₹{plan_prices.get(selected_plan, "0.0")}</span></div><div class="d-flex justify-content-between mb-1"><strong>तिथि:</strong> <span>{reg_date}</span></div><div class="d-flex justify-content-between"><strong>स्थिति:</strong> <span class="badge bg-success">एक्टिवेटेड</span></div></div></div></div></div></div></div></body></html>'
    ]
    return HTMLResponse(content="".join(parts))

@app.post("/update-profile")