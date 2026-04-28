import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعدادات النظام الأساسية
# =========================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

# تعريف هيكل البيانات لضمان عدم تداخل الأعمدة (حل مشكلة البيانات العشوائية)
DB_CONFIG = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

def load_data(key):
    config = DB_CONFIG[key]
    if not os.path.exists(config["file"]):
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    df = pd.read_csv(config["file"], encoding="utf-8-sig")
    # التأكد من مطابقة الأعمدة تماماً للهيكل المعتمد
    df = df.reindex(columns=config["cols"]).fillna("")
    return df

def save_data(df, key):
    config = DB_CONFIG[key]
    df.to_csv(config["file"], index=False, encoding="utf-8-sig")

# =========================
# نظام الدخول
# =========================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            u = st.text_input("اسم المستخدم").strip()
            p = st.text_input("كلمة المرور", type="password").strip()
            if st.button("دخول بالنظام", use_container_width=True):
                if u.upper() == "ASSAF" and p == "7734":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("❌ بيانات الدخول خاطئة")
    st.stop()

# =========================
# تهيئة متغيرات الحالة (لحل مشكلة Reset الحقول)
# =========================
if 'reset_trigger' not in st.session_state: st.session_state.reset_trigger = False

def clear_fields():
    for key in ['name', 'age', 'grade', 'id', 'phone', 'email']:
        st.session_state[f'val_{key}'] = ""

# القوائم المنسدلة
stages = ["", "الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "متوسط", "ثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]

# =========================
# القائمة الجانبية
# =========================
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 تسجيل البيانات", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة تسجيل البيانات ---
if menu == "🏠 تسجيل البيانات":
    st.header("📝 تسجيل بيانات طالب جديد")
    bio_df = load_data("bio")
    
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("الاسم الثلاثي")
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("العمر", ages)
            grade = st.selectbox("الصف", stages)
        with c2:
            s_id = st.selectbox("الرقم التسلسلي", ids)
            phone = st.selectbox("رقم الهاتف", phones)
        email = st.selectbox("البريد الإلكتروني", emails)
        
        if st.form_submit_button("✅ حفظ وإضافة جديد"):
            if name and s_id:
                new_row = pd.DataFrame([[name, s_id, age, grade, phone, email]], columns=DB_CONFIG["bio"]["cols"])
                updated_df = pd.concat([bio_df, new_row], ignore_index=True)
                save_data(updated_df, "bio")
                st.success(f"✔️ تم حفظ الطالب {name} بنجاح!")
                st.rerun()
            else:
                st.warning("⚠️ يرجى ملء الاسم والرقم التسلسلي على الأقل")

# --- 2. شاشة رصد الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد درجات الطلاب")
    bio = load_data("bio")
    grades_df = load_data("grades")
    
    if bio.empty:
        st.info("💡 لا يوجد طلاب مسجلين حالياً. يرجى تسجيل الطلاب أولاً.")
    else:
        with st.form("grades_form", clear_on_submit=True):
            st_name = st.selectbox("اختر الطالب", [""] + bio['الاسم'].tolist())
            c1, c2 = st.columns(2)
            q = c1.number_input("القرآن (50%)", 0, 100)
            f = c1.number_input("الفقه", 0, 100)
            h = c2.number_input("الحديث", 0, 100)
            s = c2.number_input("السيرة", 0, 100)
            
            if st.form_submit_button("🚀 ترحيل الدرجة"):
                if st_name:
                    avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                    if avg >= 90: تقدير = "ممتاز"
                    elif avg >= 80: تقدير = "جيد جداً"
                    elif avg >= 70: تقدير = "جيد"
                    else: تقدير = "مقبول"
                    
                    new_g = pd.DataFrame([[st_name, q, f, h, s, round(avg, 2), تقدير]], columns=DB_CONFIG["grades"]["cols"])
                    updated_g = pd.concat([grades_df[grades_df['الاسم'] != st_name], new_g], ignore_index=True)
                    save_data(updated_g, "grades")
                    st.success(f"✅ تم ترحيل درجة {st_name} بمعدل {round(avg,2)}% ({تقدير})")
                    st.rerun()

# --- 3. السجل العام (حل مشكلة التنسيق) ---
elif menu == "📋 السجل العام":
    st.header("📋 قواعد البيانات المركزية")
    tab1, tab2 = st.tabs(["👥 سجل الطلاب", "📊 سجل الدرجات"])
    
    with tab1:
        st.subheader("🗂️ بيانات الطلاب المسجلة")
        st.dataframe(load_data("bio"), use_container_width=True)
        
    with tab2:
        st.subheader("📈 نتائج الاختبارات")
        st.dataframe(load_data("grades"), use_container_width=True)

    if st.sidebar.button("🧹 تصفير النظام"):
        if os.path.exists("db_bio.csv"): os.remove("db_bio.csv")
        if os.path.exists("db_grades.csv"): os.remove("db_grades.csv")
        st.sidebar.success("تم مسح البيانات بنجاح")
        st.rerun()
