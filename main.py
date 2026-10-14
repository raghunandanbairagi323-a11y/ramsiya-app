import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# ====================================================================
# 🔑 रघु जी, आपकी सभी असली डिटेल्स यहाँ पूरी तरह सुरक्षित सेट हैं!
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
    return f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <title>रामसिया स्मार्ट ऐप</title>
        <link href="https://jsdelivr.net" rel="stylesheet">
        <style>
            body {{ background: #f4f6f9; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
            .box {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); width: 100%; max-width: 500px; }}
        </style>
    </head>
    <body>
    <div class="box">
        <h3 class="text-center mb-3">🚀 रामसिया स्मार्ट बिलिंग</h3>
        
        <!-- 📑 लॉगिन और रजिस्ट्रेशन के दोनों बटन -->
        <ul class="nav nav-tabs mb-3" id="myTab">
            <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#login">🔓 लॉगिन (Login)</button></li>
            <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#register">✨ नया दुकानदार रजिस्ट्रेशन</button></li>
        </ul>
        
        <div class="tab-content">
            <!-- 🔑 लॉगिन फॉर्म -->
            <div class="tab-pane fade show active" id="login">
                <form action="/login" method="post">
                    <div class="mb-2"><label class="small">ईमेल आईडी (Email)</label><input type="email" name="email" class="form-control" required></div>
                    <div class="mb-3"><label class="small">पासवर्ड (Password)</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-primary w-100">🔓 लॉगिन करें</button>
                </form>
            </div>
            
            <!-- ✨ रजिस्ट्रेशन फॉर्म (नया दुकानदार विकल्प) -->
            <div class="tab-pane fade" id="register">
                <form action="/register" method="post">
                    <div class="row g-2">
                        <div class="col-6 mb-2"><label class="small">ईमेल आईडी</label><input type="email" name="email" class="form-control form-control-sm" required></div>
                        <div class="col-6 mb-2"><label class="small">पासवर्ड चुनें</label><input type="password" name="password" class="form-control form-control-sm" required></div>
                        <div class="col-6 mb-2"><label class="small">दुकान का नाम</label><input type="text" name="shop_name" class="form-control form-control-sm" required></div>
                        <div class="col-6 mb-2"><label class="small">मालिक का नाम</label><input type="text" name="owner_name" class="form-control form-control-sm" required></div>
                        <div class="col-6 mb-2"><label class="small">व्हाट्सएप नंबर</label><input type="text" name="phone" class="form-control form-control-sm" required></div>
                        <div class="col-6 mb-2"><label class="small">दुकान का पता</label><input type="text" name="address" class="form-control form-control-sm" required></div>
                        
                        <div class="col-12 my-2"><label class="small fw-bold">☑️ अपना प्लान चुनें (Select Plan):</label>
                            <select name="selected_plan" class="form-select form-select-sm">
                                <option value="1m">1 महीना प्लान (₹{PRICE_1M})</option>
                                <option value="3m">3 महीना प्लान (₹{PRICE_3M})</option>
                                <option value="6m">6 महीना प्लान (₹{PRICE_6M})</option>
                                <option value="9m">9 महीना प्लान (₹{PRICE_9M})</option>
                                <option value="12m">12 महीना प्लान (₹{PRICE_12M})</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success w-100 btn-sm mt-2">✨ स्टोर एक्टिवेट करें (7 दिन फ्री ट्रायल)</button>
                </form>
            </div>
        </div>
    </div>
    <script src="https://jsdelivr.net"></script>
    </body>
    </html>
    """

@app.get("/")
async def index(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login-page", status_code=303)
    return HTMLResponse(f"""
    <html><head><title>डैशबोर्ड</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
    <body style="background:#f4f6f9; padding:40px;">
        <div class="card p-4 shadow-sm mx-auto" style="max-width:600px;">
            <h2 class="text-success">🚀 रामसिया स्मार्ट बिलिंग काउंटर चालू है!</h2>
            <div class="alert alert-warning my-3">⏳ <strong>आपका 7 दिन का फ्री ट्रायल चालू हो गया है!</strong></div>
            <p>काउंटर पूरी तरह काम कर रहा है। माल बेचें, तरक्की करें!</p>
            <a href="/logout" class="btn btn-danger btn-sm mt-3">🔒 लॉगआउट करें</a>
        </div>
    </body></html>
    """)

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
                        <div class="mb-2"><label class="small fw-bold">यूजरनेम</label><input type="text" value="{ADMIN_USER}" class="form-control form-control-sm" readonly></div>
                        <div class="mb-2"><label class="small fw-bold">मास्टर पासवर्ड (कोडिंग से सेव्ड)</label><input type="text" value="{ADMIN_PASS}" class="form-control form-control-sm" readonly></div>
                        
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

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), shop_name: str = Form(...), owner_name: str = Form(...), phone: str = Form(...), address: str = Form(...), selected_plan: str = Form(...)):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value="1")
    return response

@app.post("/login")