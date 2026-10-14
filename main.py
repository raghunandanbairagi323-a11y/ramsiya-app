import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# ====================================================================
# 🔑 रघु जी, आपकी सभी असली डिटेल्स यहाँ कोडिंग में परमानेंट सेट हैं!
# ====================================================================
ADMIN_USER = "admin"
ADMIN_PASS = "Ramsiya@3233"      # ✅ आपका गुप्त पासवर्ड
PRICE_1M   = "99.0"              # ✅ 1 महीने की कीमत
PRICE_3M   = "299.0"             # ✅ 3 महीने की कीमत
PRICE_6M   = "599.0"             # ✅ 6 महीने की कीमत
PRICE_9M   = "899.0"             # ✅ 9 महीने की कीमत
PRICE_12M  = "1199.0"            # ✅ 12 महीने की कीमत
ADMIN_UPI  = "Q378404429@ybl"    # ✅ आपकी असली भुगतान UPI ID
ADMIN_PHONE = "9893753232"       # ✅ आपका असली व्हाट्सएप नंबर
# ====================================================================

@app.get("/login-page", response_class=HTMLResponse)
async def login_page_html():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <title>रामसिया स्मार्ट ऐप</title>
        <link href="https://jsdelivr.net" rel="stylesheet">
    </head>
    <body style="background: #f4f6f9; padding-top: 50px;">
    <div class="container" style="max-width: 900px;">
        <h2 class="text-center mb-4 fw-bold text-primary">🚀 रामसिया स्मार्ट बिलिंग मुख्य सर्वर</h2>
        <div class="row g-4">
            
            <!-- 🔑 लॉगिन फॉर्म (बायाँ बॉक्स) -->
            <div class="col-md-5">
                <div class="card p-4 shadow-sm border-0" style="border-radius: 12px; background: white;">
                    <h4 class="mb-3 text-dark fw-bold">🔓 दुकानदार लॉगिन (Login)</h4>
                    <hr>
                    <form action="/login" method="post">
                        <div class="mb-3"><label class="small fw-bold">ईमेल आईडी (Email)</label><input type="email" name="email" class="form-control" required></div>
                        <div class="mb-3"><label class="small fw-bold">पासवर्ड (Password)</label><input type="password" name="password" class="form-control" required></div>
                        <button type="submit" class="btn btn-primary w-100 py-2 fw-bold mt-2">🔓 लॉगिन करें</button>
                    </form>
                </div>
            </div>
            
            <!-- ✨ रजिस्ट्रेशन फॉर्म (दायाँ बड़ा बॉक्स) -->
            <div class="col-md-7">
                <div class="card p-4 shadow-sm border-0" style="border-radius: 12px; background: white;">
                    <h4 class="mb-3 text-success fw-bold">✨ नया दुकानदार रजिस्ट्रेशन (Register)</h4>
                    <hr>
                    <form action="/register" method="post">
                        <div class="row g-2">
                            <div class="col-6 mb-2"><label class="small fw-bold">ईमेल आईडी</label><input type="email" name="email" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">पासवर्ड चुनें</label><input type="password" name="password" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">दुकान का नाम</label><input type="text" name="shop_name" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">मालिक का नाम</label><input type="text" name="owner_name" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control form-control-sm" required></div>
                            <div class="col-6 mb-2"><label class="small fw-bold">दुकान का पता</label><input type="text" name="address" class="form-control form-control-sm" required></div>
                            
                            <div class="col-12 my-2">
                                <label class="small fw-bold text-secondary">☑️ अपना बेस्ट प्लान चुनें (Select Plan):</label>
                                <select name="selected_plan" class="form-select form-select-sm bg-light fw-bold">
                                    <option value="1m">1 महीना प्लान (₹{PRICE_1M})</option>
                                    <option value="3m">3 महीना推 प्लान (₹{PRICE_3M})</option>
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
    return HTMLResponse(content=html_content)

@app.get("/")
async def index(request: Request):
    html_dashboard = f"""
    <html><head><title>रामसिया सॉफ़्टवेयर</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; padding:40px;">
        <div class="card p-4 shadow-sm mx-auto" style="max-width:600px; border-radius:12px; background:white;">
            <h2 class="text-success fw-bold">🚀 रामसिया स्मार्ट बिलिंग</h2>
            <div class="alert alert-warning my-3">⏳ <strong>आपका 7 दिन का फ्री ट्रायल सफलतापूर्वक चालू हो गया है!</strong></div>
            <p class="text-dark">आपका बिलिंग काउंटर पूरी तरह लाइव है। माल बेचें, तरक्की करें!</p>
            <hr>
            <div class="text-muted small">सॉफ़्टवेयर हेड ऑफिस सपोर्ट टीम: +91 {ADMIN_PHONE}</div>
            <a href="/login-page" class="btn btn-danger btn-sm mt-3 fw-bold">🔒 लॉगआउट करें (Logout)</a>
        </div>
    </body></html>
    """
    return HTMLResponse(content=html_dashboard)

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form(...)):
    html_redirect = """
    <html><head><script>window.location.href="/";</script></head><body></body></html>
    """
    return HTMLResponse(content=html_redirect)

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if password == ADMIN_PASS:
        html_redirect = """
        <html><head><script>window.location.href="/";</script></head><body></body></html>
        """
        return HTMLResponse(content=html_redirect)
    return "गलत ईमेल या पासवर्ड!"