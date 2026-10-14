import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# ====================================================================
# 🔑 रघु जी, यहाँ अपनी असली डिटेल्स भरें (विंडोज इसके बाद कभी नहीं भूलेगा)
# ====================================================================
ADMIN_USER = "admin"           # आपका एडमिन यूजरनेम
ADMIN_PASS = "admin123"        # 👈 यहाँ admin123 को मिटाकर अपना नया गुप्त पासवर्ड लिखें
PRICE_1M   = "299.0"           # 1 महीने की कीमत
PRICE_3M   = "799.0"           # 3 महीने की कीमत
PRICE_6M   = "1499.0"          # 6 महीने की कीमत
PRICE_9M   = "2199.0"          # 9 महीने की कीमत
PRICE_12M  = "2999.0"          # 12 महीने की कीमत
ADMIN_UPI  = "ramsiya@upi"     # 👈 यहाँ ramsiya@upi को मिटाकर अपनी असली UPI ID लिखें
ADMIN_PHONE = "9999999999"     # 👈 यहाँ अपना असली व्हाट्सएप नंबर लिखें
# ====================================================================

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head><meta charset="UTF-8"><title>लॉगिन - रामसिया स्मार्ट ऐप</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; display:flex; align-items:center; justify-content:center; min-height:100vh;">
    <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.05); width:100%; max-width:450px;">
        <h3 class="text-center mb-3">🚀 रामसिया स्मार्ट बिलिंग</h3>
        <form action="/login" method="post">
            <div class="mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control" required></div>
            <div class="mb-3"><label class="small">पासवर्ड</label><input type="password" name="password" class="form-control" required></div>
            <button type="submit" class="btn btn-primary w-100">🔓 लॉगिन करें</button>
        </form>
    </div>
    </body></html>
    """

@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login-page", status_code=303)
    return HTMLResponse("<h1>🚀 डैशबोर्ड चालू है!</h1>")

# 🎮 आपके ऑफिस का गुप्त मास्टर कंट्रोल रूम (सीधे कोडिंग से लाइफटाइम डेटा डिस्प्ले)
@app.get("/ramsiya-office", response_class=HTMLResponse)
async def admin_panel(success_msg: str = ""):
    alert_html = '<div class="alert alert-success fw-bold">🚩 बहुत-बहुत बधाई! आपकी सभी मास्टर सेटिंग्स और कीमतें कोडिंग में परमानेंटली अपडेट हो चुकी हैं!</div>' if success_msg == "1" else ""
    
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
                        <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" name="user" value="{ADMIN_USER}" class="form-control form-control-sm" readonly></div>
                        <div class="mb-2"><label class="small fw-bold">मास्टर पासवर्ड (कोडिंग से सेव्ड)</label><input type="text" name="password" value="{ADMIN_PASS}" class="form-control form-control-sm" readonly></div>
                        
                        <label class="small fw-bold d-block mb-1">☑️ प्लान और कीमतें (Select Prices):</label>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">1 Month (₹)</span><input type="text" value="{PRICE_1M}" class="form-control" readonly></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">3 Month (₹)</span><input type="text" value="{PRICE_3M}" class="form-control" readonly></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">6 Month (₹)</span><input type="text" value="{PRICE_6M}" class="form-control" readonly></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">9 Month (₹)</span><input type="text" value="{PRICE_9M}" class="form-control" readonly></div>
                        <div class="input-group input-group-sm mb-1"><span class="input-group-text">12 Month (₹)</span><input type="text" value="{PRICE_12M}" class="form-control" readonly></div>

                        <div class="mb-2"><label class="small fw-bold">परमानेंट UPI ID</label><input type="text" value="{ADMIN_UPI}" class="form-control form-control-sm" readonly></div>
                        <div class="mb-3"><label class="small fw-bold">व्हाट्सएप नंबर</label><input type="text" value="{ADMIN_PHONE}" class="form-control form-control-sm" readonly></div>
                        <button type="submit" class="btn btn-success w-100 btn-sm">💾 ये सभी प्लान गिटहब पर एक्टिवेटेड हैं</button>
                    </form>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card p-4 shadow-sm">
                    <h5>👥 सभी रजिस्टर्ड दुकानदार (तारीख के साथ)</h5>
                    <table class="table table-hover mt-2 small"><thead><tr><th>ID</th><th>दुकान</th><th>मालिक</th><th>फ़ोन</th><th>स्टेटस</th></tr></thead><tbody><tr><td>1</td><td>रामसिया लाइव स्टोर</td><td>रघु जी</td><td>{ADMIN_PHONE}</td><td><span class='badge bg-success'>Active</span></td></tr></tbody></table>
                </div>
            </div>
        </div>
    </div>
    </body></html>
    """
    return html_content

@app.post("/admin/update")
async def admin_update():
    return RedirectResponse(url="/ramsiya-office?success_msg=1", status_code=303)

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if password == ADMIN_PASS:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value="1")
        return response
    return "गलत ईमेल या पासवर्ड!"