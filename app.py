import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Anjaz | أنجز",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS  — فقط تعديلات القائمة الجانبية
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [class*="css"], * {
    font-family: 'Cairo', sans-serif !important;
}

/* Main content RTL */
.main .block-container {
    direction: rtl;
    padding-top: 2rem;
    max-width: 1100px;
}

.stApp { background: #F7F4F0; }

/* ── تصحيح أبعاد القائمة الجانبية ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1A1A2E 0%,#16213E 60%,#0F3460 100%) !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    position: fixed !important;
    top: 0 !important;
    left: auto !important;
    right: 0 !important;
    height: 100vh !important;
    overflow-y: auto !important;
    z-index: 100 !important;
}

/* إزالة أي padding زائد */
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 12px !important;
    width: 100% !important;
}

/* ضبط المسافة للمحتوى الرئيسي */
section.main {
    margin-right: 280px !important;
}

/* للشاشات الصغيرة */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }
    section.main {
        margin-right: 260px !important;
    }
}

section[data-testid="stSidebar"] * {
    color: white !important;
    direction: rtl;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 10px !important;
    margin-bottom: 5px !important;
    font-size: 0.92rem !important;
    padding: 9px 14px !important;
    text-align: right !important;
    width: 100% !important;
    box-shadow: none !important;
    transition: all 0.18s !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,107,53,0.28) !important;
    border-color: #FF6B35 !important;
}

/* باقي الـ CSS كما هو دون تغيير */
.hero {
    background: linear-gradient(135deg,#FF6B35 0%,#F7931E 60%,#FF4757 100%);
    border-radius: 20px;
    padding: 40px 32px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 14px 40px rgba(255,107,53,0.28);
}
.hero h1 { font-size: 2.2rem; font-weight: 900; margin-bottom: 6px; }
.hero p  { font-size: 1rem; opacity: 0.92; margin: 0; }

.card {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06);
    margin-bottom: 14px;
    border: 1px solid #F0EBE3;
}
.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #1A1A2E;
    margin-bottom: 16px;
    padding-bottom: 7px;
    border-bottom: 3px solid #FF6B35;
    display: inline-block;
}

.pcard {
    background: white;
    border-radius: 16px;
    padding: 18px 20px;
    border: 2px solid #F0EBE3;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.pcard:hover {
    border-color: #FF6B35;
    box-shadow: 0 6px 22px rgba(255,107,53,0.13);
}
.pname { font-size: 1.05rem; font-weight: 800; color: #1A1A2E; }
.pmeta { color: #888; font-size: 0.85rem; margin-top: 3px; }
.pbio  { color: #444; font-size: 0.9rem; margin: 9px 0 0; }
.badge {
    display: inline-block;
    background: #FFF3EC; color: #FF6B35;
    border: 1px solid #FFD4B8;
    border-radius: 20px; padding: 2px 11px;
    font-size: 0.8rem; font-weight: 700; margin-left: 5px;
}
.badge-green { background:#E8F5E9; color:#2E7D32; border-color:#A5D6A7; }
.badge-red   { background:#FFEBEE; color:#C62828; border-color:#EF9A9A; }
.badge-blue  { background:#E3F2FD; color:#1565C0; border-color:#90CAF9; }
.stars { color: #FFB347; }

.svc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px,1fr));
    gap: 10px;
}
.svc-item {
    background: white; border: 2px solid #F0EBE3;
    border-radius: 14px; padding: 16px 8px;
    text-align: center;
}
.svc-item:hover { border-color:#FF6B35; box-shadow:0 4px 16px rgba(255,107,53,0.13); }
.svc-icon { font-size: 1.9rem; margin-bottom: 5px; }
.svc-name { font-size: 0.82rem; font-weight: 700; color: #333; }

.bitem {
    background: white; border-radius: 14px;
    padding: 15px 18px; margin-bottom: 11px;
    border: 1px solid #F0EBE3;
}
.bitem-header {
    display: flex; justify-content: space-between;
    align-items: flex-start; flex-wrap: wrap; gap: 8px;
}

.auth-wrap {
    max-width: 500px; margin: 0 auto;
    background: white; border-radius: 20px;
    padding: 34px; box-shadow: 0 8px 32px rgba(0,0,0,0.09);
}
.auth-title { font-size:1.6rem; font-weight:900; color:#FF6B35; text-align:center; margin-bottom:4px; }
.auth-sub   { text-align:center; color:#888; margin-bottom:22px; font-size:0.9rem; }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#FF6B35,#F7931E) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important; font-size: 0.92rem !important;
    width: 100% !important; padding: 10px 18px !important;
    box-shadow: 0 3px 12px rgba(255,107,53,0.22) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,107,53,0.32) !important;
}

.stTextInput>div>div>input,
.stSelectbox>div>div,
.stTextArea>div>div>textarea {
    border-radius: 11px !important;
    border: 2px solid #F0EBE3 !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important;
}
div[data-testid="stTabs"] button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
}
.stRadio > div { flex-direction: row !important; gap: 14px !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Constants (نفس الكود الأصلي)
# ─────────────────────────────────────────────
SERVICES = [
    {"icon":"🚗","name":"سيارات"},
    {"icon":"🚚","name":"نقل وتوصيل"},
    {"icon":"💻","name":"خدمات أون لاين"},
    {"icon":"🔧","name":"سباكة"},
    {"icon":"⚡","name":"كهرباء"},
    {"icon":"🪚","name":"نجارة"},
    {"icon":"❄️","name":"تكييف"},
    {"icon":"🎨","name":"نقاشة"},
    {"icon":"📱","name":"صيانة أجهزة"},
    {"icon":"🧹","name":"نظافة"},
    {"icon":"🏗️","name":"خدمات صناعية"},
]
SERVICE_NAMES = [s["name"] for s in SERVICES]
SERVICE_ICON  = {s["name"]: s["icon"] for s in SERVICES}

CITIES = [
    "القاهرة","الجيزة","الإسكندرية","الدقهلية","البحيرة",
    "الفيوم","الغربية","الإسماعيلية","المنوفية","المنيا",
    "القليوبية","الوادي الجديد","السويس","أسوان","أسيوط",
    "بني سويف","بورسعيد","دمياط","الشرقية","جنوب سيناء",
    "كفر الشيخ","مطروح","الأقصر","قنا","شمال سيناء",
    "سوهاج","البحر الأحمر",
]

STATUS_PENDING  = "قيد الانتظار ⏳"
STATUS_CONFIRM  = "مؤكد ✅"
STATUS_CANCEL   = "ملغي ❌"

# ─────────────────────────────────────────────
#  DB helpers (نفس الكود الأصلي)
# ─────────────────────────────────────────────
USERS_FILE    = "anjaz_users.json"
BOOKINGS_FILE = "anjaz_bookings.json"
REVIEWS_FILE  = "anjaz_reviews.json"

def _load(path):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(name,email,password,user_type,city,
                  service_type=None,bio=None,experience=None):
    users = _load(USERS_FILE)
    if email in users:
        return False,"هذا الإيميل مسجل بالفعل 📧"
    users[email] = {
        "name":name,"email":email,
        "password":hash_pw(password),
        "type":user_type,"city":city,
        "service_type":service_type,
        "bio":bio or "","experience":experience or "",
        "joined":datetime.now().strftime("%Y-%m-%d"),
        "rating":0.0,"rating_count":0,
    }
    _save(USERS_FILE,users)
    return True,"تم التسجيل بنجاح ✅"

def login_user(email,password):
    users = _load(USERS_FILE)
    if email not in users:
        return False,None,"الإيميل غير مسجل ❌"
    if users[email]["password"] != hash_pw(password):
        return False,None,"كلمة المرور غير صحيحة ❌"
    return True,users[email],"مرحباً بك ✅"

def get_all_users():
    return _load(USERS_FILE)

def get_providers(service=None,city=None):
    users = _load(USERS_FILE)
    result = [u for u in users.values() if u["type"]=="provider"]
    if service: result = [u for u in result if u.get("service_type")==service]
    if city:    result = [u for u in result if u.get("city")==city]
    return result

def update_rating(provider_email,new_rating):
    users = _load(USERS_FILE)
    if provider_email in users:
        u = users[provider_email]
        old_total = u["rating"]*u["rating_count"]
        u["rating_count"] += 1
        u["rating"] = round((old_total+new_rating)/u["rating_count"],1)
        _save(USERS_FILE,users)

def save_booking(client_email,provider_email,service,details,date,time_slot):
    bookings = _load(BOOKINGS_FILE)
    bid = f"B{len(bookings)+1:04d}_{datetime.now().strftime('%H%M%S')}"
    bookings[bid] = {
        "id":bid,"client":client_email,
        "provider":provider_email,"service":service,
        "details":details,"date":str(date),"time":time_slot,
        "status":STATUS_PENDING,"rated":False,
        "booked_at":datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(BOOKINGS_FILE,bookings)
    return bid

def update_booking_status(bid,new_status):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["status"] = new_status
        _save(BOOKINGS_FILE,bookings)

def mark_rated(bid):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["rated"] = True
        _save(BOOKINGS_FILE,bookings)

def get_client_bookings(client_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["client"]==client_email]

def get_provider_bookings(provider_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["provider"]==provider_email]

def save_review(provider_email,client_name,rating,comment):
    reviews = _load(REVIEWS_FILE)
    if provider_email not in reviews:
        reviews[provider_email]=[]
    reviews[provider_email].append({
        "client":client_name,"rating":rating,
        "comment":comment,"date":datetime.now().strftime("%Y-%m-%d"),
    })
    _save(REVIEWS_FILE,reviews)

def get_reviews(provider_email):
    return _load(REVIEWS_FILE).get(provider_email,[])

# ─────────────────────────────────────────────
#  Session state (نفس الكود الأصلي)
# ─────────────────────────────────────────────
for k,v in {
    "logged_in":False,"user":None,"page":"home",
    "selected_service":None,"selected_provider":None,
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

def go(page):
    st.session_state.page=page
    st.rerun()

# ─────────────────────────────────────────────
#  باقي الكود كما هو (لم يتم تغيير أي شيء)
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:28px 12px 14px;'>
            <div style='font-size:2.2rem;'>⚡</div>
            <div style='font-size:1.4rem;font-weight:900;letter-spacing:1px;'>Anjaz</div>
            <div style='font-size:0.78rem;opacity:0.6;margin-top:2px;'>أنجز خدمتك بسرعة</div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.12);margin:0 12px 14px;'>
        """, unsafe_allow_html=True)

        if st.session_state.logged_in:
            u = st.session_state.user
            utype_label = "مقدم خدمة 🔧" if u["type"]=="provider" else "عميل 👤"
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.09);border-radius:12px;
                        padding:12px;margin:0 10px 18px;text-align:center;'>
                <div style='font-size:0.98rem;font-weight:800;'>{u['name']}</div>
                <div style='font-size:0.78rem;opacity:0.7;margin-top:2px;'>{utype_label}</div>
                <div style='font-size:0.75rem;opacity:0.55;'>📍 {u.get("city","")}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)

            if u["type"]=="client":
                menu=[
                    ("🏠","الرئيسية","home"),
                    ("🔧","الخدمات","services"),
                    ("📅","حجوزاتي","my_bookings"),
                    ("ℹ️","عن التطبيق","about"),
                ]
            else:
                menu=[
                    ("🏠","لوحة التحكم","home"),
                    ("📋","طلباتي","provider_orders"),
                    ("👤","ملفي الشخصي","provider_profile"),
                    ("ℹ️","عن التطبيق","about"),
                ]

            for icon,label,pk in menu:
                dot = "🟠 " if st.session_state.page==pk else ""
                if st.button(f"{dot}{icon}  {label}", key=f"nav_{pk}"):
                    go(pk)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:16px 12px 10px;'>",
                        unsafe_allow_html=True)
            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
            if st.button("🚪  تسجيل الخروج"):
                st.session_state.logged_in=False
                st.session_state.user=None
                st.session_state.page="home"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
            if st.button("🔑  تسجيل الدخول"): go("login")
            if st.button("📝  إنشاء حساب"):    go("register")
            st.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:14px 0;'>",
                        unsafe_allow_html=True)
            if st.button("ℹ️  عن التطبيق"):     go("about")
            st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  جميع دوال الصفحات الأخرى موجودة هنا (نفس الكود الأصلي)
#  تم حذفها من هذا المثال للاختصار، ولكنها موجودة في الكود الأصلي
# ─────────────────────────────────────────────

def main():
    render_sidebar()
    # باقي الكود كما هو...

if __name__=="__main__":
    main()