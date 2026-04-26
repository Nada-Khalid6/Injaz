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
#  CSS  — Sidebar fixed, no overlap, proper dimensions
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
}

/* Main content area - RTL with proper spacing */
.main .block-container {
    direction: rtl;
    padding: 2rem 2rem 2rem 2rem !important;
    max-width: 1200px;
    margin-right: auto;
    margin-left: auto;
}

/* Fix main content position when sidebar exists */
section.main > div {
    padding-left: 0 !important;
}

.stApp {
    background: #F7F4F0;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%) !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    border-left: none !important;
}

/* Sidebar content padding */
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 12px !important;
}

/* Sidebar text colors */
section[data-testid="stSidebar"] *:not(button) {
    color: white !important;
}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span {
    direction: rtl;
}

/* Sidebar buttons styling */
section[data-testid="stSidebar"] .stButton button {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    margin-bottom: 6px !important;
    width: 100% !important;
    text-align: right !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255, 107, 53, 0.3) !important;
    border-color: #FF6B35 !important;
    transform: translateX(-2px) !important;
}

/* Sidebar horizontal rule */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.1);
    margin: 15px 0;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 60%, #FF4757 100%);
    border-radius: 24px;
    padding: 40px 36px;
    color: white;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 15px 45px rgba(255, 107, 53, 0.25);
}

.hero h1 {
    font-size: 2.3rem;
    font-weight: 900;
    margin-bottom: 10px;
}

.hero p {
    font-size: 1rem;
    opacity: 0.92;
    margin: 0;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
    border: 1px solid #EFE8E0;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #1A1A2E;
    margin-bottom: 20px;
    padding-bottom: 8px;
    border-bottom: 3px solid #FF6B35;
    display: inline-block;
}

/* ── Provider card ── */
.pcard {
    background: white;
    border-radius: 18px;
    padding: 20px 24px;
    border: 1px solid #EFE8E0;
    margin-bottom: 16px;
    transition: all 0.2s;
}

.pcard:hover {
    border-color: #FF6B35;
    box-shadow: 0 8px 28px rgba(255, 107, 53, 0.12);
}

.pname {
    font-size: 1.1rem;
    font-weight: 800;
    color: #1A1A2E;
}

.pmeta {
    color: #888;
    font-size: 0.85rem;
    margin-top: 4px;
}

.pbio {
    color: #555;
    font-size: 0.9rem;
    margin: 12px 0 0;
}

.badge {
    display: inline-block;
    background: #FFF3EC;
    color: #FF6B35;
    border: 1px solid #FFD4B8;
    border-radius: 30px;
    padding: 3px 14px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-left: 8px;
}

.badge-green {
    background: #E8F5E9;
    color: #2E7D32;
    border-color: #A5D6A7;
}

.badge-red {
    background: #FFEBEE;
    color: #C62828;
    border-color: #EF9A9A;
}

.badge-blue {
    background: #E3F2FD;
    color: #1565C0;
    border-color: #90CAF9;
}

.stars {
    color: #FFB347;
    font-size: 0.9rem;
}

/* ── Service grid ── */
.svc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
}

.svc-item {
    background: white;
    border: 2px solid #EFE8E0;
    border-radius: 18px;
    padding: 18px 12px;
    text-align: center;
    transition: all 0.2s;
    cursor: pointer;
}

.svc-item:hover {
    border-color: #FF6B35;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.12);
}

.svc-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.svc-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: #333;
}

/* ── Booking item ── */
.bitem {
    background: white;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 14px;
    border: 1px solid #EFE8E0;
    transition: box-shadow 0.2s;
}

.bitem:hover {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.bitem-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
}

/* ── Auth forms ── */
.auth-wrap {
    max-width: 550px;
    margin: 40px auto;
    background: white;
    border-radius: 28px;
    padding: 40px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
}

.auth-title {
    font-size: 1.8rem;
    font-weight: 900;
    color: #FF6B35;
    text-align: center;
    margin-bottom: 8px;
}

.auth-sub {
    text-align: center;
    color: #888;
    margin-bottom: 28px;
    font-size: 0.9rem;
}

/* ── Main button styling ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 11px 20px !important;
    transition: all 0.2s !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(255, 107, 53, 0.35) !important;
}

/* Form inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    border-radius: 14px !important;
    border: 2px solid #EFE8E0 !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    padding: 10px 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
}

/* Radio buttons */
.stRadio > div {
    flex-direction: row !important;
    gap: 20px !important;
}

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    background: #FAF8F5 !important;
    border-radius: 12px !important;
}

/* Slider */
div[data-testid="stSlider"] {
    padding: 10px 0 !important;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Responsive */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }
    .hero {
        padding: 25px 20px;
    }
    .hero h1 {
        font-size: 1.6rem;
    }
    .auth-wrap {
        padding: 25px;
        margin: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
SERVICES = [
    {"icon": "🚗", "name": "سيارات"},
    {"icon": "🚚", "name": "نقل وتوصيل"},
    {"icon": "💻", "name": "خدمات أون لاين"},
    {"icon": "🔧", "name": "سباكة"},
    {"icon": "⚡", "name": "كهرباء"},
    {"icon": "🪚", "name": "نجارة"},
    {"icon": "❄️", "name": "تكييف"},
    {"icon": "🎨", "name": "نقاشة"},
    {"icon": "📱", "name": "صيانة أجهزة"},
    {"icon": "🧹", "name": "نظافة"},
    {"icon": "🏗️", "name": "خدمات صناعية"},
]

SERVICE_NAMES = [s["name"] for s in SERVICES]
SERVICE_ICON = {s["name"]: s["icon"] for s in SERVICES}

# All Egyptian governorates
CITIES = [
    "القاهرة", "الجيزة", "الإسكندرية", "الدقهلية", "البحيرة",
    "الفيوم", "الغربية", "الإسماعيلية", "المنوفية", "المنيا",
    "القليوبية", "الوادي الجديد", "السويس", "أسوان", "أسيوط",
    "بني سويف", "بورسعيد", "دمياط", "الشرقية", "جنوب سيناء",
    "كفر الشيخ", "مطروح", "الأقصر", "قنا", "شمال سيناء",
    "سوهاج", "البحر الأحمر",
]

STATUS_PENDING = "قيد الانتظار ⏳"
STATUS_CONFIRM = "مؤكد ✅"
STATUS_CANCEL = "ملغي ❌"

# ─────────────────────────────────────────────
#  Database helpers
# ─────────────────────────────────────────────
USERS_FILE = "anjaz_users.json"
BOOKINGS_FILE = "anjaz_bookings.json"
REVIEWS_FILE = "anjaz_reviews.json"

def _load(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(name, email, password, user_type, city,
                  service_type=None, bio=None, experience=None):
    users = _load(USERS_FILE)
    if email in users:
        return False, "هذا الإيميل مسجل بالفعل 📧"
    
    users[email] = {
        "name": name,
        "email": email,
        "password": hash_pw(password),
        "type": user_type,
        "city": city,
        "service_type": service_type,
        "bio": bio or "",
        "experience": experience or "",
        "joined": datetime.now().strftime("%Y-%m-%d"),
        "rating": 0.0,
        "rating_count": 0,
    }
    _save(USERS_FILE, users)
    return True, "تم التسجيل بنجاح ✅"

def login_user(email, password):
    users = _load(USERS_FILE)
    if email not in users:
        return False, None, "الإيميل غير مسجل ❌"
    if users[email]["password"] != hash_pw(password):
        return False, None, "كلمة المرور غير صحيحة ❌"
    return True, users[email], "مرحباً بك ✅"

def get_all_users():
    return _load(USERS_FILE)

def get_providers(service=None, city=None):
    users = _load(USERS_FILE)
    result = [u for u in users.values() if u["type"] == "provider"]
    if service:
        result = [u for u in result if u.get("service_type") == service]
    if city:
        result = [u for u in result if u.get("city") == city]
    return result

def update_rating(provider_email, new_rating):
    users = _load(USERS_FILE)
    if provider_email in users:
        u = users[provider_email]
        old_total = u["rating"] * u["rating_count"]
        u["rating_count"] += 1
        u["rating"] = round((old_total + new_rating) / u["rating_count"], 1)
        _save(USERS_FILE, users)

def save_booking(client_email, provider_email, service, details, date, time_slot):
    bookings = _load(BOOKINGS_FILE)
    bid = f"B{len(bookings)+1:04d}_{datetime.now().strftime('%H%M%S')}"
    bookings[bid] = {
        "id": bid,
        "client": client_email,
        "provider": provider_email,
        "service": service,
        "details": details,
        "date": str(date),
        "time": time_slot,
        "status": STATUS_PENDING,
        "rated": False,
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(BOOKINGS_FILE, bookings)
    return bid

def update_booking_status(bid, new_status):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["status"] = new_status
        _save(BOOKINGS_FILE, bookings)

def mark_rated(bid):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["rated"] = True
        _save(BOOKINGS_FILE, bookings)

def get_client_bookings(client_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["client"] == client_email]

def get_provider_bookings(provider_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["provider"] == provider_email]

def save_review(provider_email, client_name, rating, comment):
    reviews = _load(REVIEWS_FILE)
    if provider_email not in reviews:
        reviews[provider_email] = []
    reviews[provider_email].append({
        "client": client_name,
        "rating": rating,
        "comment": comment,
        "date": datetime.now().strftime("%Y-%m-%d"),
    })
    _save(REVIEWS_FILE, reviews)

def get_reviews(provider_email):
    return _load(REVIEWS_FILE).get(provider_email, [])

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
for k, v in {
    "logged_in": False,
    "user": None,
    "page": "home",
    "selected_service": None,
    "selected_provider": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo area
        st.markdown(
            """
            <div style="text-align: center; padding: 30px 12px 20px;">
                <div style="font-size: 2.5rem;">⚡</div>
                <div style="font-size: 1.5rem; font-weight: 900; letter-spacing: 1px; margin-top: 5px;">Anjaz</div>
                <div style="font-size: 0.8rem; opacity: 0.65; margin-top: 5px;">أنجز خدمتك بسرعة</div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 0 8px 20px;">
            """,
            unsafe_allow_html=True
        )

        if st.session_state.logged_in:
            u = st.session_state.user
            utype_label = "مقدم خدمة 🔧" if u["type"] == "provider" else "عميل 👤"
            
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.08); border-radius: 16px;
                            padding: 15px; margin: 0 0 20px; text-align: center;">
                    <div style="font-size: 1rem; font-weight: 800;">{u['name']}</div>
                    <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 4px;">{utype_label}</div>
                    <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 4px;">📍 {u.get('city', '')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if u["type"] == "client":
                menu = [
                    ("🏠", "الرئيسية", "home"),
                    ("🔧", "الخدمات", "services"),
                    ("📅", "حجوزاتي", "my_bookings"),
                    ("ℹ️", "عن التطبيق", "about"),
                ]
            else:
                menu = [
                    ("🏠", "لوحة التحكم", "home"),
                    ("📋", "طلباتي", "provider_orders"),
                    ("👤", "ملفي الشخصي", "provider_profile"),
                    ("ℹ️", "عن التطبيق", "about"),
                ]

            for icon, label, pk in menu:
                is_active = st.session_state.page == pk
                active_class = "🟠 " if is_active else ""
                if st.button(f"{active_class}{icon}  {label}", key=f"nav_{pk}"):
                    go(pk)

            st.markdown(
                "<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0 15px;'>",
                unsafe_allow_html=True
            )
            
            if st.button("🚪  تسجيل الخروج", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()

        else:
            if st.button("🔑  تسجيل الدخول", key="login_btn"):
                go("login")
            if st.button("📝  إنشاء حساب", key="register_btn"):
                go("register")
            
            st.markdown(
                "<hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0;'>",
                unsafe_allow_html=True
            )
            
            if st.button("ℹ️  عن التطبيق", key="about_btn"):
                go("about")

# ─────────────────────────────────────────────
#  Auth pages
# ─────────────────────────────────────────────
def page_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">⚡ تسجيل الدخول</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">أهلاً بك مجدداً في Anjaz</div>', unsafe_allow_html=True)

    email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="li_e")
    pw = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="li_p")
    
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("دخول ⚡", key="btn_login"):
        if email and pw:
            ok, user, msg = login_user(email.strip().lower(), pw)
            if ok:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error(msg)
        else:
            st.warning("ادخل الإيميل وكلمة المرور ⚠️")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 0.85rem;'>مش عندك حساب؟</div>",
        unsafe_allow_html=True
    )
    
    if st.button("إنشاء حساب جديد 📝", key="go_reg"):
        go("register")
    
    st.markdown('</div>', unsafe_allow_html=True)

def page_register():
    st.markdown('<div class="auth-wrap" style="max-width: 600px;">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📝 حساب جديد</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">اختار نوع حسابك أولاً</div>', unsafe_allow_html=True)

    user_type_raw = st.radio(
        "نوع الحساب",
        ["👤 عميل — أبحث عن خدمة", "🔧 مقدم خدمة — أقدم خدمة"],
        key="reg_type"
    )
    is_provider = "مقدم" in user_type_raw

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 الاسم كامل", placeholder="محمد أحمد", key="rn")
        pw = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="rp")
    with col2:
        email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="re")
        pw2 = st.text_input("🔒 تأكيد كلمة المرور", type="password", placeholder="••••••••", key="rp2")

    city = st.selectbox("📍 المحافظة", CITIES, key="rc")

    service_type = bio = experience = None
    if is_provider:
        st.markdown("---")
        st.markdown("**🔧 معلومات الخدمة**")
        service_type = st.selectbox("نوع الخدمة التي تقدمها", SERVICE_NAMES, key="rs")
        bio = st.text_area(
            "📝 نبذة عنك",
            placeholder="اكتب نبذة عن خبرتك وما تقدمه للعملاء...",
            height=90,
            key="rb"
        )
        experience = st.text_input("📅 سنوات الخبرة", placeholder="مثلاً: 5 سنوات", key="rx")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("إنشاء الحساب 🚀", key="btn_reg"):
        if name and email and pw and pw2 and city:
            if pw != pw2:
                st.error("كلمتا المرور غير متطابقتين ❌")
            elif len(pw) < 6:
                st.error("كلمة المرور أقل من 6 أحرف ❌")
            else:
                utype = "provider" if is_provider else "client"
                ok, msg = register_user(
                    name.strip(), email.strip().lower(), pw,
                    utype, city, service_type, bio, experience
                )
                if ok:
                    ok2, user, _ = login_user(email.strip().lower(), pw)
                    if ok2:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.page = "home"
                        st.rerun()
                else:
                    st.error(msg)
        else:
            st.warning("اكمل جميع الحقول ⚠️")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("عندي حساب بالفعل 🔑", key="go_login"):
        go("login")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Landing (not logged in)
# ─────────────────────────────────────────────
def page_landing():
    st.markdown(
        """
        <div class="hero">
            <h1>⚡ Anjaz | أنجز</h1>
            <p>المنصة الأولى لخدمات الصيانة والمنازل بالعربي</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="card">
                <div style="font-size: 1.1rem; font-weight: 800; color: #CC3300; margin-bottom: 12px;">😩 المشكلة</div>
                <ul style="list-style: none; padding: 0; line-height: 2.2; color: #444;">
                    <li>❌ صعوبة إيجاد عمال موثوقين</li>
                    <li>❌ ضياع الوقت في البحث</li>
                    <li>❌ أسعار غير واضحة</li>
                    <li>❌ لا توجد تقييمات</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="card">
                <div style="font-size: 1.1rem; font-weight: 800; color: #00796B; margin-bottom: 12px;">✅ الحل</div>
                <ul style="list-style: none; padding: 0; line-height: 2.2; color: #444;">
                    <li>✅ منصة تجمع كل الخدمات</li>
                    <li>✅ بحث حسب المحافظة والخدمة</li>
                    <li>✅ تقييمات حقيقية من عملاء</li>
                    <li>✅ حجز سريع وسهل</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 الخدمات المتاحة</div>', unsafe_allow_html=True)
    
    svc_html = '<div class="svc-grid">'
    for s in SERVICES:
        svc_html += f'<div class="svc-item"><div class="svc-icon">{s["icon"]}</div><div class="svc-name">{s["name"]}</div></div>'
    svc_html += '</div>'
    st.markdown(svc_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔑 سجّل دخولك وابدأ الآن ⚡", key="landing_cta"):
            go("login")

# ─────────────────────────────────────────────
#  CLIENT — Home
# ─────────────────────────────────────────────
def page_client_home():
    u = st.session_state.user
    bookings = get_client_bookings(u["email"])

    st.markdown(
        f"""
        <div class="hero">
            <h1>أهلاً {u['name'].split()[0]}! 👋</h1>
            <p>محتاج إيه النهارده؟ اختار الخدمة وإحنا نجيبلك أحسن متخصص</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    stats = [
        (col1, "📅 حجوزاتي", str(len(bookings))),
        (col2, "📍 مدينتي", u.get("city", "—")),
        (col3, "🏆 عضويتي", "مميز ⭐"),
    ]
    
    for col, label, val in stats:
        with col:
            st.markdown(
                f"""
                <div class="card" style="text-align: center;">
                    <div style="font-size: 1.6rem; font-weight: 900; color: #FF6B35;">{val}</div>
                    <div style="font-size: 0.85rem; color: #666; margin-top: 6px;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 ابدأ من هنا</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, svc in enumerate(SERVICES):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="svc-item">
                    <div class="svc-icon">{svc['icon']}</div>
                    <div class="svc-name">{svc['name']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("عرض", key=f"hs_{i}"):
                st.session_state.selected_service = svc["name"]
                go("services")

# ─────────────────────────────────────────────
#  CLIENT — Services
# ─────────────────────────────────────────────
def page_services():
    st.markdown('<div class="section-title">🔧 تصفح مقدمي الخدمة</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        default_idx = (SERVICE_NAMES.index(st.session_state.selected_service) + 1
                       if st.session_state.selected_service else 0)
        filter_svc = st.selectbox("نوع الخدمة", ["الكل"] + SERVICE_NAMES,
                                  index=default_idx, key="fs")
    with col2:
        filter_city = st.selectbox("المحافظة", ["الكل"] + CITIES, key="fc")

    svc_q = None if filter_svc == "الكل" else filter_svc
    city_q = None if filter_city == "الكل" else filter_city
    providers = get_providers(svc_q, city_q)

    if not providers:
        st.info("🔍 لا يوجد مقدمو خدمة بهذا الاختيار حتى الآن.")
        return

    providers_sorted = sorted(providers, key=lambda x: -x.get("rating", 0))
    st.markdown(
        f"<p style='color: #888; margin-bottom: 16px;'>تم إيجاد <strong>{len(providers_sorted)}</strong> مقدم خدمة</p>",
        unsafe_allow_html=True
    )

    for p in providers_sorted:
        rating = p.get("rating", 0)
        r_count = p.get("rating_count", 0)
        stars = "⭐" * round(rating) if rating else "لا يوجد تقييم بعد"
        icon = SERVICE_ICON.get(p.get("service_type", ""), "🔧")
        reviews = get_reviews(p["email"])
        bio_text = p.get('bio', '') or 'لم تتم إضافة نبذة.'

        st.markdown(
            f"""
            <div class="pcard">
                <div class="bitem-header">
                    <div>
                        <div class="pname">{icon} {p['name']}</div>
                        <div class="pmeta">📍 {p.get('city', '—')} &nbsp;|&nbsp; 🔧 {p.get('service_type', '—')}</div>
                        <div class="pmeta">⏱️ خبرة: {p.get('experience', 'غير محدد')}</div>
                    </div>
                    <div>
                        <span class="badge">{p.get('service_type', '')}</span>
                        <span class="badge badge-green">✅ متاح</span>
                        <div style="margin-top: 6px;">
                            <span class="stars">{stars}</span>
                            <span style="color: #aaa; font-size: 0.8rem;"> ({r_count} تقييم)</span>
                        </div>
                    </div>
                </div>
                <div class="pbio">{bio_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_r, col_b = st.columns([2, 1])
        with col_r:
            if reviews:
                with st