import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعدادات النظام الأساسية
# =========================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

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
    return df.reindex(columns=config["cols"]).fillna("")

def save_data(df, key):
    config = DB_CONFIG[key]
    df.to_csv(config["file"], index=False, encoding="utf-8-sig")

# =========================
# دالة توليد المعرف تلقائياً (ID)
# =========================
def generate_auto_id(df):
    if df.empty:
        return "ID-100"
    try:
        # استخراج الأرقام فقط من الـ ID وتحويلها لانتجر
        last_id = df['الرقم'].str.extract('(\d+)').astype(int).max().iloc[0]
        return f"ID-{last_id + 1}"
    except:
        return "ID-100"

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

# القوائم الثابتة
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]
att_status = ["حاضر", "غائب", "متأخر", "معتذر"]
parts = [str(i) for i in range(1, 31)]

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة إدارة الطلاب (تعديل، حذف، ID تلقائي) ---
if menu == "🏠 إدارة الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    df = load_data("bio")
    
    # اختيار وضع: إضافة جديد أو تعديل موجود
    student_list = ["➕ إضافة طالب جديد"] + df['الاسم'].tolist()
    choice = st.selectbox("🎯 اختر إجراءً:", student_list)

    # تجهيز القيم الافتراضية
    if choice == "➕ إضافة طالب جديد":
        v_name, v_age, v_grade, v_phone, v_email = "", "", "", "", ""
        v_id = generate_auto_id(df)
        btn_label = "✅ حفظ الطالب الجديد"
    else:
        row = df[df['الاسم'] == choice].iloc[0]
        v_name, v_id, v_age, v_grade, v_phone, v_email = row['الاسم'], row['الرقم'], str(row['العمر']), str(row['الصف']), str(row['الهاتف']), str(row['الإيميل'])
        btn_label = "💾 تحديث البيانات"

    with st.form("bio_form", clear_on_submit=(choice == "➕ إضافة طالب جديد")):
        st.info(f"🆔 المعرف (ID): {v_id}")
        name = st.text_input("الاسم الثلاثي", value=v_name)
        c1, c2 = st.columns(2)
        with c1:
            age = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade = st.selectbox("الصف", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        with c2:
            phone = st.selectbox("رقم الهاتف", phones, index=phones.index(v_phone) if v_phone in phones else 0)
            email = st.selectbox("البريد الإلكتروني", emails, index=emails.index(v_email) if v_email in emails else 0)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn2:
            submitted = st.form_submit_button(btn_label)
        
        if submitted:
            if name:
                # حذف القديم إذا كان تعديل
                updated_df = df[df['الاسم'] != choice] if choice != "➕ إضافة طالب جديد" else df
                new_row = pd.DataFrame([[name, v_id, age, grade, phone, email]], columns=DB_CONFIG["bio"]["cols"])
                save_data(pd.concat([updated_df, new_row], ignore_index=True), "bio")
                st.success("✔️ تم الحفظ بنجاح")
                st.rerun()

    if choice != "➕ إضافة طالب جديد":
        if st.button("🗑️ حذف هذا الطالب نهائياً"):
            save_data(df[df['الاسم'] != choice], "bio")
            st.warning("🚮 تم حذف الطالب من السجلات")
            st.rerun()

# --- 2. شاشة التحضير ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ سجل الحضور والغياب")
    bio, att_df = load_data("bio"), load_data("att")
    with st.form("att_form", clear_on_submit=True):
        date_val = st.date_input("التاريخ", datetime.today())
        student = st.selectbox("اختر الطالب", [""] + bio['الاسم'].tolist())
        status = st.selectbox("الحالة", att_status)
        if st.form_submit_button("💾 حفظ التحضير"):
            if student:
                new_att = pd.DataFrame([[date_val.strftime("%Y-%m-%d"), student, status]], columns=DB_CONFIG["att"]["cols"])
                save_data(pd.concat([att_df, new_att], ignore_index=True), "att")
                st.success("✔️ تم التحضير")
                st.rerun()

# --- 3. شاشة الحفظ (تقييم آلي بناءً على عدد الصفحات) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio, hifz_df = load_data("bio"), load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        part = st.selectbox("الجزء", parts)
        surah = st.text_input("السورة")
        pages = st.number_input("عدد الصفحات", 1, 20)
        
        if st.form_submit_button("💾 حفظ سجل الحفظ"):
            if student and surah:
                # --- معادلة التقييم الآلية ---
                if pages >= 5: eval_val = "ممتاز"
                elif pages >= 3: eval_val = "جيد جداً"
                elif pages >= 2: eval_val = "جيد"
                else: eval_val = "مقبول"
                
                new_h = pd.DataFrame([[student, part, surah, pages, eval_val]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz_df, new_h], ignore_index=True), "hifz")
                st.success(f"✔️ تم الحفظ بنجاح | التقييم الآلي: {eval_val}")
                st.rerun()

# --- 4. شاشة الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات النهائية")
    bio, grades_df = load_data("bio"), load_data("grades")
    with st.form("grade_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q, f = c1.number_input("القرآن", 0, 100), c1.number_input("الفقه", 0, 100)
        h, s = c2.number_input("الحديث", 0, 100), c2.number_input("السيرة", 0, 100)
        if st.form_submit_button("🚀 ترحيل الدرجة"):
            if student:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                t = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), t]], columns=DB_CONFIG["grades"]["cols"])
                save_data(pd.concat([grades_df[grades_df['الاسم'] != student], new_g], ignore_index=True), "grades")
                st.success("✔️ تم الترحيل")
                st.rerun()

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير العامة")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    with t1: st.dataframe(load_data("bio"), use_container_width=True)
    with t2: st.dataframe(load_data("att"), use_container_width=True)
    with t3: st.dataframe(load_data("hifz"), use_container_width=True)
    with t4: st.dataframe(load_data("grades"), use_container_width=True)
