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
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}
.stApp { background: #F7F4F0; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%) !important;
    border-left: none !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    text-align: right !important;
    border-radius: 10px !important;
    margin-bottom: 4px !important;
    font-size: 0.95rem !important;
    padding: 10px 16px !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,107,53,0.3) !important;
    border-color: #FF6B35 !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 60%, #FF4757 100%);
    border-radius: 20px; padding: 48px 36px;
    color: white; text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 16px 48px rgba(255,107,53,0.3);
}
.hero h1 { font-size: 2.6rem; font-weight: 900; margin-bottom: 8px; }
.hero p  { font-size: 1.05rem; opacity: 0.92; }

/* ── Cards ── */
.card {
    background: white; border-radius: 16px; padding: 24px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    margin-bottom: 16px; border: 1px solid #F0EBE3;
}
.section-title {
    font-size: 1.35rem; font-weight: 800; color: #1A1A2E;
    margin-bottom: 18px; padding-bottom: 8px;
    border-bottom: 3px solid #FF6B35; display: inline-block;
}

/* ── Provider Card ── */
.provider-card {
    background: white; border-radius: 16px; padding: 20px;
    border: 2px solid #F0EBE3; margin-bottom: 14px;
    transition: all 0.2s; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.provider-card:hover {
    border-color: #FF6B35;
    box-shadow: 0 8px 28px rgba(255,107,53,0.15);
    transform: translateY(-2px);
}
.provider-name { font-size: 1.1rem; font-weight: 800; color: #1A1A2E; }
.provider-meta { color: #888; font-size: 0.88rem; margin-top: 4px; }
.provider-bio  { color: #444; font-size: 0.92rem; margin: 10px 0; }
.badge {
    display: inline-block; background: #FFF3EC; color: #FF6B35;
    border: 1px solid #FFD4B8; border-radius: 20px;
    padding: 3px 12px; font-size: 0.82rem; font-weight: 700; margin-left: 6px;
}
.badge-green { background: #E8F5E9; color: #2E7D32; border-color: #A5D6A7; }
.stars { color: #FFB347; font-size: 1rem; }

/* ── Service grid ── */
.svc-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:12px; }
.svc-item {
    background: white; border: 2px solid #F0EBE3;
    border-radius: 14px; padding: 18px 10px;
    text-align: center; transition: all 0.2s;
}
.svc-item:hover { border-color:#FF6B35; box-shadow:0 6px 20px rgba(255,107,53,0.15); }
.svc-icon { font-size: 2rem; margin-bottom: 6px; }
.svc-name { font-size: 0.85rem; font-weight: 700; color: #333; }

/* ── Auth ── */
.auth-wrap {
    max-width: 480px; margin: 0 auto; background: white;
    border-radius: 20px; padding: 36px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.1);
}
.auth-title { font-size:1.7rem; font-weight:900; color:#FF6B35; text-align:center; margin-bottom:6px; }
.auth-sub   { text-align:center; color:#888; margin-bottom:24px; font-size:0.95rem; }

/* ── Booking item ── */
.booking-item {
    background:white; border-radius:14px; padding:16px 20px;
    margin-bottom:12px; border:1px solid #F0EBE3;
    display:flex; justify-content:space-between; align-items:center;
}
.status-badge {
    background:#E8F5E9; color:#2E7D32; border-radius:20px;
    padding:4px 14px; font-size:0.8rem; font-weight:700;
}

/* ── Streamlit overrides ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#FF6B35,#F7931E) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-family:'Cairo',sans-serif !important;
    font-weight:700 !important; font-size:0.95rem !important;
    width:100% !important; padding:11px 20px !important;
    box-shadow:0 4px 14px rgba(255,107,53,0.25) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 24px rgba(255,107,53,0.38) !important;
}
.stTextInput>div>div>input,
.stSelectbox>div>div,
.stTextArea>div>div>textarea {
    border-radius:12px !important; border:2px solid #F0EBE3 !important;
    font-family:'Cairo',sans-serif !important; direction:rtl !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color:#FF6B35 !important;
    box-shadow:0 0 0 3px rgba(255,107,53,0.12) !important;
}
div[data-testid="stTabs"] button { font-family:'Cairo',sans-serif !important; font-weight:700 !important; }
.stRadio>div { flex-direction:row !important; gap:16px !important; }
footer { visibility:hidden; }
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
SERVICE_ICON  = {s["name"]: s["icon"] for s in SERVICES}

CITIES = ["القاهرة", "الجيزة", "الإسكندرية", "الأقصر", "أسوان",
          "المنصورة", "طنطا", "الزقازيق", "السويس", "الإسماعيلية",
          "بورسعيد", "شرم الشيخ", "الغردقة", "أسيوط", "المنيا"]

# ─────────────────────────────────────────────
#  DB helpers
# ─────────────────────────────────────────────
USERS_FILE    = "anjaz_users.json"
BOOKINGS_FILE = "anjaz_bookings.json"
REVIEWS_FILE  = "anjaz_reviews.json"

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
        "name": name, "email": email,
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

def get_providers(service=None, city=None):
    users = _load(USERS_FILE)
    result = [u for u in users.values() if u["type"] == "provider"]
    if service:
        result = [u for u in result if u.get("service_type") == service]
    if city:
        result = [u for u in result if u.get("city") == city]
    return result

def get_all_users():
    return _load(USERS_FILE)

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
    bid = f"{client_email}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    bookings[bid] = {
        "id": bid, "client": client_email,
        "provider": provider_email, "service": service,
        "details": details, "date": str(date), "time": time_slot,
        "status": "قيد المعالجة ⏳", "rated": False,
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(BOOKINGS_FILE, bookings)
    return bid

def get_client_bookings(client_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["client"] == client_email]

def get_provider_bookings(provider_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["provider"] == provider_email]

def mark_rated(bid):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["rated"] = True
        _save(BOOKINGS_FILE, bookings)

def save_review(provider_email, client_name, rating, comment):
    reviews = _load(REVIEWS_FILE)
    if provider_email not in reviews:
        reviews[provider_email] = []
    reviews[provider_email].append({
        "client": client_name, "rating": rating,
        "comment": comment, "date": datetime.now().strftime("%Y-%m-%d"),
    })
    _save(REVIEWS_FILE, reviews)

def get_reviews(provider_email):
    return _load(REVIEWS_FILE).get(provider_email, [])

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
for k, v in {
    "logged_in": False, "user": None, "page": "home",
    "selected_service": None, "selected_provider": None,
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
        st.markdown("""
        <div style='text-align:center; padding:24px 0 16px;'>
            <div style='font-size:2.4rem;'>⚡</div>
            <div style='font-size:1.5rem; font-weight:900; letter-spacing:1px;'>Anjaz</div>
            <div style='font-size:0.82rem; opacity:0.65; margin-top:2px;'>أنجز خدمتك بسرعة</div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.1); margin:0 0 16px;'>
        """, unsafe_allow_html=True)

        if st.session_state.logged_in:
            u = st.session_state.user
            utype_label = "مقدم خدمة 🔧" if u["type"] == "provider" else "عميل 👤"
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.08); border-radius:12px;
                        padding:14px; margin-bottom:20px; text-align:center;'>
                <div style='font-size:1rem; font-weight:800;'>{u['name']}</div>
                <div style='font-size:0.8rem; opacity:0.7; margin-top:2px;'>{utype_label}</div>
                <div style='font-size:0.78rem; opacity:0.6;'>📍 {u.get('city','')}</div>
            </div>""", unsafe_allow_html=True)

            if u["type"] == "client":
                menu = [
                    ("🏠", "الرئيسية",    "home"),
                    ("🔧", "الخدمات",     "services"),
                    ("📅", "حجوزاتي",    "my_bookings"),
                    ("ℹ️", "عن التطبيق",  "about"),
                ]
            else:
                menu = [
                    ("🏠", "لوحة التحكم",   "home"),
                    ("📋", "طلباتي",        "provider_orders"),
                    ("👤", "ملفي الشخصي",  "provider_profile"),
                    ("ℹ️", "عن التطبيق",    "about"),
                ]

            for icon, label, page_key in menu:
                active = "🟠 " if st.session_state.page == page_key else ""
                if st.button(f"{active}{icon} {label}", key=f"nav_{page_key}"):
                    go(page_key)

            st.markdown("<hr style='border-color:rgba(255,255,255,0.1); margin:20px 0 12px;'>",
                        unsafe_allow_html=True)
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()
        else:
            st.markdown("**ابدأ الآن**")
            if st.button("🔑 تسجيل الدخول"):  go("login")
            if st.button("📝 إنشاء حساب"):    go("register")
            st.markdown("<hr style='border-color:rgba(255,255,255,0.1); margin:20px 0 12px;'>",
                        unsafe_allow_html=True)
            if st.button("ℹ️ عن التطبيق"):     go("about")

# ─────────────────────────────────────────────
#  AUTH pages
# ─────────────────────────────────────────────
def page_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">⚡ تسجيل الدخول</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">أهلاً بك مجدداً في Anjaz</div>', unsafe_allow_html=True)

    email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="li_e")
    pw    = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="li_p")
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
    st.markdown("<div style='text-align:center; color:#888; font-size:0.9rem;'>مش عندك حساب؟</div>",
                unsafe_allow_html=True)
    if st.button("إنشاء حساب جديد 📝", key="go_reg"):
        go("register")
    st.markdown('</div>', unsafe_allow_html=True)


def page_register():
    st.markdown('<div class="auth-wrap" style="max-width:580px;">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📝 حساب جديد</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">اختار نوع حسابك أولاً</div>', unsafe_allow_html=True)

    user_type_raw = st.radio(
        "نوع الحساب",
        ["👤 عميل — أبحث عن خدمة", "🔧 مقدم خدمة — أقدم خدمة"],
        key="reg_type"
    )
    is_provider = "مقدم" in user_type_raw

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        name  = st.text_input("👤 الاسم كامل", placeholder="محمد أحمد", key="rn")
        pw    = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="rp")
    with c2:
        email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="re")
        pw2   = st.text_input("🔒 تأكيد كلمة المرور", type="password", placeholder="••••••••", key="rp2")

    city = st.selectbox("📍 المدينة", CITIES, key="rc")

    service_type = bio = experience = None
    if is_provider:
        st.markdown("---")
        st.markdown("**🔧 معلومات الخدمة**")
        service_type = st.selectbox("نوع الخدمة التي تقدمها", SERVICE_NAMES, key="rs")
        bio = st.text_area("📝 نبذة عنك",
            placeholder="اكتب نبذة عن خبرتك وما تقدمه للعملاء...",
            height=100, key="rb")
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
                ok, msg = register_user(name.strip(), email.strip().lower(), pw,
                                        utype, city, service_type, bio, experience)
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
#  LANDING (not logged in)
# ─────────────────────────────────────────────
def page_landing():
    st.markdown("""<div class="hero">
        <h1>⚡ Anjaz | أنجز</h1>
        <p>المنصة الأولى لخدمات الصيانة والمنازل بالعربي</p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="card">
        <div style="font-size:1.1rem;font-weight:800;color:#CC3300;margin-bottom:12px;">😩 المشكلة</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>❌ صعوبة إيجاد عمال موثوقين</li>
            <li>❌ ضياع الوقت في البحث</li>
            <li>❌ أسعار غير واضحة</li>
            <li>❌ لا توجد تقييمات</li>
        </ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
        <div style="font-size:1.1rem;font-weight:800;color:#00796B;margin-bottom:12px;">✅ الحل</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>✅ منصة تجمع كل الخدمات</li>
            <li>✅ بحث حسب المدينة والخدمة</li>
            <li>✅ تقييمات حقيقية</li>
            <li>✅ حجز سريع وسهل</li>
        </ul></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 الخدمات المتاحة</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="svc-grid">' +
        "".join(f'<div class="svc-item"><div class="svc-icon">{s["icon"]}</div>'
                f'<div class="svc-name">{s["name"]}</div></div>' for s in SERVICES) +
        '</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔑 سجّل دخولك وابدأ الآن ⚡", key="landing_login"):
            go("login")

# ─────────────────────────────────────────────
#  CLIENT pages
# ─────────────────────────────────────────────
def page_client_home():
    u = st.session_state.user
    bookings = get_client_bookings(u["email"])

    st.markdown(f"""<div class="hero">
        <h1>أهلاً {u['name'].split()[0]}! 👋</h1>
        <p>محتاج إيه النهارده؟ اختار الخدمة وإحنا نجيبلك أحسن متخصص</p>
    </div>""", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    for col, label, val in [
        (s1, "📅 حجوزاتي",  str(len(bookings))),
        (s2, "📍 مدينتي",   u.get("city","—")),
        (s3, "🏆 عضويتي",   "مميز ⭐"),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:900;color:#FF6B35;">{val}</div>
                <div style="font-size:0.88rem;color:#666;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 ابدأ من هنا</div>', unsafe_allow_html=True)
    st.markdown("اضغط على أي خدمة لتصفح مقدمي الخدمة المتاحين:")

    cols = st.columns(4)
    for i, svc in enumerate(SERVICES):
        with cols[i % 4]:
            st.markdown(f"""<div class="svc-item">
                <div class="svc-icon">{svc['icon']}</div>
                <div class="svc-name">{svc['name']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("عرض", key=f"hs_{i}"):
                st.session_state.selected_service = svc["name"]
                go("services")


def page_services():
    st.markdown('<div class="section-title">🔧 الخدمات المتاحة</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        default_idx = (SERVICE_NAMES.index(st.session_state.selected_service) + 1
                       if st.session_state.selected_service else 0)
        filter_svc = st.selectbox("نوع الخدمة", ["الكل"] + SERVICE_NAMES,
                                  index=default_idx, key="fs")
    with c2:
        filter_city = st.selectbox("المدينة", ["الكل"] + CITIES, key="fc")

    svc_q  = None if filter_svc  == "الكل" else filter_svc
    city_q = None if filter_city == "الكل" else filter_city

    providers = get_providers(svc_q, city_q)

    if not providers:
        st.info("🔍 لا يوجد مقدمو خدمة بهذا الاختيار حتى الآن.")
        return

    st.markdown(f"<p style='color:#888; margin-bottom:16px;'>تم إيجاد "
                f"<strong>{len(providers)}</strong> مقدم خدمة</p>", unsafe_allow_html=True)

    for p in sorted(providers, key=lambda x: -x.get("rating", 0)):
        rating    = p.get("rating", 0)
        r_count   = p.get("rating_count", 0)
        stars_str = "⭐" * round(rating) if rating else "لا يوجد تقييم بعد"
        svc_icon  = SERVICE_ICON.get(p.get("service_type",""), "🔧")
        reviews   = get_reviews(p["email"])

        st.markdown(f"""
        <div class="provider-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                <div>
                    <div class="provider-name">{svc_icon} {p['name']}</div>
                    <div class="provider-meta">📍 {p.get('city','—')} &nbsp;|&nbsp; 🔧 {p.get('service_type','—')}</div>
                    <div class="provider-meta">⏱️ خبرة: {p.get('experience','غير محدد')}</div>
                </div>
                <div style="text-align:left;">
                    <span class="badge">{p.get('service_type','')}</span>
                    <span class="badge badge-green">✅ متاح</span>
                    <div style="margin-top:6px;">
                        <span class="stars">{stars_str}</span>
                        <span style="color:#aaa;font-size:0.82rem;"> ({r_count} تقييم)</span>
                    </div>
                </div>
            </div>
            <div class="provider-bio">{p.get('bio','') or 'لم تتم إضافة نبذة.'}</div>
        </div>""", unsafe_allow_html=True)

        col_r, col_b = st.columns([2, 1])
        with col_r:
            if reviews:
                with st.expander(f"💬 التقييمات ({len(reviews)})"):
                    for r in reviews[-5:]:
                        st.markdown(f"""
                        <div style="border-right:3px solid #FF6B35;padding:8px 14px;margin-bottom:8px;
                                    background:#FFFAF7;border-radius:8px;">
                            <strong>{r['client']}</strong> &nbsp; {'⭐'*r['rating']}
                            <br><span style="color:#555;font-size:0.88rem;">{r['comment']}</span>
                            <br><span style="color:#bbb;font-size:0.78rem;">{r['date']}</span>
                        </div>""", unsafe_allow_html=True)
        with col_b:
            if st.button("📅 احجز الآن", key=f"bk_{p['email']}"):
                st.session_state.selected_provider = p
                go("booking")


def page_booking():
    p = st.session_state.selected_provider
    if not p:
        go("services")
        return

    svc_icon = SERVICE_ICON.get(p.get("service_type",""), "🔧")
    st.markdown(f"""<div class="hero" style="padding:32px;">
        <h1 style="font-size:1.8rem;">{svc_icon} حجز مع {p['name']}</h1>
        <p>📍 {p.get('city','—')} &nbsp;|&nbsp; 🔧 {p.get('service_type','—')}</p>
    </div>""", unsafe_allow_html=True)

    with st.form("bform"):
        c1, c2 = st.columns(2)
        with c1:
            date = st.date_input("📅 تاريخ الخدمة", min_value=datetime.today())
        with c2:
            time_slot = st.selectbox("🕐 الوقت المناسب",
                ["صباحاً 8:00 - 10:00", "صباحاً 10:00 - 12:00",
                 "ظهراً 12:00 - 2:00",   "عصراً 2:00 - 4:00",
                 "مساءً 4:00 - 6:00",   "مساءً 6:00 - 8:00"])

        details = st.text_area("📝 وصف المشكلة",
            placeholder="اشرح المشكلة بالتفصيل...", height=110)
        address = st.text_input("📍 العنوان التفصيلي",
            placeholder="الشارع، رقم المبنى، الدور...")
        submitted = st.form_submit_button("✅ تأكيد الحجز")

    if submitted:
        if details and address:
            u = st.session_state.user
            save_booking(u["email"], p["email"], p.get("service_type",""),
                         f"{details} | العنوان: {address}", date, time_slot)
            st.success(f"🎉 تم تأكيد الحجز مع {p['name']} ليوم {date}!")
            st.session_state.selected_provider = None
            go("my_bookings")
        else:
            st.warning("ادخل تفاصيل المشكلة والعنوان ⚠️")

    if st.button("← رجوع للخدمات"):
        st.session_state.selected_provider = None
        go("services")


def page_my_bookings():
    u = st.session_state.user
    bookings = get_client_bookings(u["email"])
    all_users = get_all_users()

    st.markdown('<div class="section-title">📅 حجوزاتي</div>', unsafe_allow_html=True)

    if not bookings:
        st.info("مفيش حجوزات لحد دلوقتي. اذهب إلى الخدمات وابدأ! ⚡")
        if st.button("🔧 تصفح الخدمات"):
            go("services")
        return

    for b in sorted(bookings, key=lambda x: x["booked_at"], reverse=True):
        provider = all_users.get(b["provider"], {})
        provider_name = provider.get("name", b["provider"])
        svc_icon = SERVICE_ICON.get(b["service"], "🔧")

        st.markdown(f"""
        <div class="booking-item">
            <div>
                <div style="font-weight:800;color:#333;">{svc_icon} {b['service']}</div>
                <div style="color:#666;font-size:0.87rem;margin-top:2px;">
                    مع <strong>{provider_name}</strong>
                </div>
                <div style="color:#aaa;font-size:0.82rem;">📅 {b['date']} | 🕐 {b['time']}</div>
            </div>
            <span class="status-badge">{b['status']}</span>
        </div>""", unsafe_allow_html=True)

        if not b.get("rated"):
            with st.expander(f"⭐ قيّم {provider_name}"):
                rating  = st.slider("تقييمك من 5", 1, 5, 5, key=f"rt_{b['id']}")
                comment = st.text_area("تعليقك", placeholder="شاركنا تجربتك...",
                                       key=f"cm_{b['id']}", height=80)
                if st.button("إرسال التقييم ⭐", key=f"sb_{b['id']}"):
                    update_rating(b["provider"], rating)
                    save_review(b["provider"], u["name"], rating, comment)
                    mark_rated(b["id"])
                    st.success("شكراً على تقييمك! ⭐")
                    st.rerun()

# ─────────────────────────────────────────────
#  PROVIDER pages
# ─────────────────────────────────────────────
def page_provider_home():
    u = st.session_state.user
    orders    = get_provider_bookings(u["email"])
    all_users = get_all_users()
    rating    = u.get("rating", 0)
    r_count   = u.get("rating_count", 0)
    svc_icon  = SERVICE_ICON.get(u.get("service_type",""), "🔧")

    st.markdown(f"""<div class="hero">
        <h1>{svc_icon} أهلاً {u['name'].split()[0]}!</h1>
        <p>لوحة التحكم — {u.get('service_type','')}</p>
    </div>""", unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    for col, label, val in [
        (s1, "📋 الطلبات",   str(len(orders))),
        (s2, "⭐ تقييمي",    f"{rating:.1f} / 5"),
        (s3, "💬 عدد التقييمات", str(r_count)),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div style="font-size:1.6rem;font-weight:900;color:#FF6B35;">{val}</div>
                <div style="font-size:0.88rem;color:#666;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 آخر الطلبات</div>', unsafe_allow_html=True)

    if not orders:
        st.info("لم تصلك طلبات بعد. بمجرد حجز أحد ستظهر هنا.")
    else:
        for b in sorted(orders, key=lambda x: x["booked_at"], reverse=True)[:5]:
            client = all_users.get(b["client"], {})
            client_name = client.get("name", b["client"])
            st.markdown(f"""
            <div class="booking-item">
                <div>
                    <div style="font-weight:800;color:#333;">👤 {client_name}</div>
                    <div style="color:#aaa;font-size:0.82rem;">📅 {b['date']} | 🕐 {b['time']}</div>
                    <div style="color:#555;font-size:0.85rem;margin-top:4px;">{b['details'][:70]}...</div>
                </div>
                <span class="status-badge">{b['status']}</span>
            </div>""", unsafe_allow_html=True)


def page_provider_orders():
    u = st.session_state.user
    orders    = get_provider_bookings(u["email"])
    all_users = get_all_users()

    st.markdown('<div class="section-title">📋 جميع الطلبات</div>', unsafe_allow_html=True)

    if not orders:
        st.info("لم تصلك طلبات بعد.")
        return

    for b in sorted(orders, key=lambda x: x["booked_at"], reverse=True):
        client = all_users.get(b["client"], {})
        client_name = client.get("name", b["client"])
        client_city = client.get("city", "—")

        st.markdown(f"""
        <div class="provider-card">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                <div>
                    <div class="provider-name">👤 {client_name}</div>
                    <div class="provider-meta">📍 {client_city} | 📅 {b['date']} | 🕐 {b['time']}</div>
                </div>
                <span class="status-badge">{b['status']}</span>
            </div>
            <div class="provider-bio" style="margin-top:10px;">{b['details']}</div>
            <div style="font-size:0.78rem;color:#bbb;margin-top:6px;">تم الحجز: {b['booked_at']}</div>
        </div>""", unsafe_allow_html=True)


def page_provider_profile():
    u = st.session_state.user
    svc_icon = SERVICE_ICON.get(u.get("service_type",""), "🔧")
    rating   = u.get("rating", 0)
    r_count  = u.get("rating_count", 0)
    stars    = "⭐" * round(rating) if rating else "لا يوجد تقييم بعد"
    reviews  = get_reviews(u["email"])

    st.markdown('<div class="section-title">👤 ملفي الشخصي</div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="card">
        <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap;">
            <div style="font-size:3.5rem;">{svc_icon}</div>
            <div>
                <div style="font-size:1.3rem;font-weight:900;color:#1A1A2E;">{u['name']}</div>
                <div style="color:#888;font-size:0.9rem;">📍 {u.get('city','—')} &nbsp;|&nbsp; 🔧 {u.get('service_type','—')}</div>
                <div style="color:#888;font-size:0.9rem;">⏱️ خبرة: {u.get('experience','غير محدد')}</div>
                <div style="margin-top:6px;">
                    <span class="stars">{stars}</span>
                    <span style="color:#aaa;font-size:0.85rem;"> ({r_count} تقييم)</span>
                </div>
            </div>
        </div>
        <div style="margin-top:16px;padding-top:16px;border-top:1px solid #F0EBE3;
                    color:#444;font-size:0.95rem;">
            {u.get('bio','لم تتم إضافة نبذة.')}
        </div>
    </div>""", unsafe_allow_html=True)

    if reviews:
        st.markdown('<div class="section-title">💬 تقييمات العملاء</div>', unsafe_allow_html=True)
        for r in reversed(reviews):
            st.markdown(f"""
            <div style="border-right:3px solid #FF6B35;padding:10px 16px;margin-bottom:10px;
                        background:white;border-radius:10px;box-shadow:0 1px 8px rgba(0,0,0,0.05);">
                <strong>{r['client']}</strong> &nbsp; {'⭐'*r['rating']}
                <br><span style="color:#555;font-size:0.9rem;">{r['comment']}</span>
                <br><span style="color:#bbb;font-size:0.78rem;">{r['date']}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("لم تصلك تقييمات بعد ⭐")

# ─────────────────────────────────────────────
#  About
# ─────────────────────────────────────────────
def page_about():
    st.markdown("""<div class="hero">
        <h1>⚡ Anjaz | أنجز</h1>
        <p>وسيط بين العميل ومقدم الخدمة</p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="card">
        <div style="font-size:1.1rem;font-weight:800;color:#FF6B35;margin-bottom:12px;">🎯 الفئة المستهدفة</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>👨‍👩‍👧 الأسر</li>
            <li>🧑 الشباب</li>
            <li>🏢 أصحاب الشقق</li>
            <li>👤 أي شخص يحتاج خدمة</li>
        </ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
        <div style="font-size:1.1rem;font-weight:800;color:#FF6B35;margin-bottom:12px;">💰 نموذج الربح</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>💸 عمولة على كل طلب</li>
            <li>📢 إعلانات ممولة</li>
            <li>🏆 اشتراكات لمقدمي الخدمة</li>
        </ul></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="card" style="text-align:center;">
        <div style="font-size:1rem;color:#555;line-height:2;">
            Anjaz — فكرة بسيطة، قابلة للتنفيذ، وتخدم المجتمع ❤️<br>
            <strong style="color:#FF6B35;">Anjaz © 2025</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Router
# ─────────────────────────────────────────────
def main():
    render_sidebar()
    page   = st.session_state.page
    logged = st.session_state.logged_in
    u      = st.session_state.user

    if not logged:
        if   page == "login":    page_login()
        elif page == "register": page_register()
        elif page == "about":    page_about()
        else:                    page_landing()
        return

    if u["type"] == "client":
        if   page == "home":         page_client_home()
        elif page == "services":     page_services()
        elif page == "booking":      page_booking()
        elif page == "my_bookings":  page_my_bookings()
        elif page == "about":        page_about()
        else:                        page_client_home()
    else:
        if   page == "home":              page_provider_home()
        elif page == "provider_orders":   page_provider_orders()
        elif page == "provider_profile":  page_provider_profile()
        elif page == "about":             page_about()
        else:                             page_provider_home()


if __name__ == "__main__":
    main()
