import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعدادات النظام الأساسية
# =========================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

# تعريف هيكل البيانات الصارم لكل شاشة (لمنع تداخل الأعمدة)
DB_CONFIG = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

def load_data(key):
    config = DB_CONFIG[key]
    if not os.path.exists(config["file"]):
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    df = pd.read_csv(config["file"], encoding="utf-8-sig")
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
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ خطأ في البيانات")
    st.stop()

# =========================
# القوائم الثابتة
# =========================
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]
att_status = ["حاضر", "غائب", "متأخر", "معتذر"]
eval_list = ["ممتاز", "جيد جداً", "جيد", "مقبول", "يحتاج متابعة"]
parts = [str(i) for i in range(1, 31)]

# =========================
# القائمة الجانبية
# =========================
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 تسجيل الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة تسجيل الطلاب ---
if menu == "🏠 تسجيل الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    df = load_data("bio")
    with st.form("bio_form", clear_on_submit=True):
        name = st.text_input("الاسم الثلاثي")
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("العمر", ages)
            grade = st.selectbox("الصف الدراسي", stages)
        with c2:
            s_id = st.selectbox("الرقم التسلسلي", ids)
            phone = st.selectbox("رقم الهاتف", phones)
        email = st.selectbox("البريد الإلكتروني", emails)
        if st.form_submit_button("✅ حفظ البيانات"):
            if name and s_id:
                new_row = pd.DataFrame([[name, s_id, age, grade, phone, email]], columns=DB_CONFIG["bio"]["cols"])
                save_data(pd.concat([df, new_row], ignore_index=True), "bio")
                st.success("✔️ تم الحفظ وتفريغ الحقول")
                st.rerun()

# --- 2. شاشة التحضير (عادت للعمل) ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ سجل الحضور والغياب")
    bio = load_data("bio")
    att_df = load_data("att")
    with st.form("att_form", clear_on_submit=True):
        date_val = st.date_input("التاريخ", datetime.today())
        student = st.selectbox("اختر الطالب", [""] + bio['الاسم'].tolist())
        status = st.selectbox("الحالة", att_status)
        if st.form_submit_button("💾 حفظ التحضير"):
            if student:
                new_att = pd.DataFrame([[date_val.strftime("%Y-%m-%d"), student, status]], columns=DB_CONFIG["att"]["cols"])
                save_data(pd.concat([att_df, new_att], ignore_index=True), "att")
                st.success(f"✔️ تم تحضير {student}")
                st.rerun()

# --- 3. شاشة الحفظ (عادت للعمل) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio = load_data("bio")
    hifz_df = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        with c1:
            part = st.selectbox("الجزء", parts)
            surah = st.text_input("السورة")
        with c2:
            pages = st.number_input("عدد الصفحات", 1, 20)
            evaluation = st.selectbox("التقييم", eval_list)
        if st.form_submit_button("💾 حفظ السجل"):
            if student and surah:
                new_h = pd.DataFrame([[student, part, surah, pages, evaluation]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz_df, new_h], ignore_index=True), "hifz")
                st.success("✔️ تم حفظ بيانات الحفظ")
                st.rerun()

# --- 4. شاشة الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات النهائية")
    bio = load_data("bio")
    grades_df = load_data("grades")
    with st.form("grade_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q = c1.number_input("القرآن", 0, 100)
        f = c1.number_input("الفقه", 0, 100)
        h = c2.number_input("الحديث", 0, 100)
        s = c2.number_input("السيرة", 0, 100)
        if st.form_submit_button("🚀 ترحيل"):
            if student:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                if avg >= 90: t = "ممتاز"
                elif avg >= 80: t = "جيد جداً"
                elif avg >= 70: t = "جيد"
                else: t = "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), t]], columns=DB_CONFIG["grades"]["cols"])
                save_data(pd.concat([grades_df[grades_df['الاسم'] != student], new_g], ignore_index=True), "grades")
                st.success("✔️ تم رصد الدرجة")
                st.rerun()

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير العامة")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    with t1: st.dataframe(load_data("bio"), use_container_width=True)
    with t2: st.dataframe(load_data("att"), use_container_width=True)
    with t3: st.dataframe(load_data("hifz"), use_container_width=True)
    with t4: st.dataframe(load_data("grades"), use_container_width=True)
