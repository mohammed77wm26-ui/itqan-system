import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعدادات ثابتة
# =========================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

DB_FILES = {
    "bio": ("db_bio.csv", ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']),
    "att": ("db_att.csv", ['التاريخ', 'الاسم', 'الحالة']),
    "hifz": ("db_hifz.csv", ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم']),
    "grades": ("db_grades.csv", ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])
}

def load_data(key):
    file, cols = DB_FILES[key]
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False, encoding="utf-8-sig")
    df = pd.read_csv(file, encoding="utf-8-sig")
    for col in cols:
        if col not in df.columns: df[col] = ""
    return df

def save_data(df, key):
    file, _ = DB_FILES[key]
    df.to_csv(file, index=False, encoding="utf-8-sig")

# =========================
# نظام الدخول
# =========================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# =========================
# القوائم المنسدلة (طلبك الأساسي)
# =========================
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids_list = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones_list = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails_list = ["", "student@itqan.com", "admin@itqan.com", "user@itqan.com"]

# =========================
# القائمة الجانبية
# =========================
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة البيانات ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    bio_df = load_data("bio")
    
    student_list = ["➕ إضافة طالب جديد"] + bio_df['الاسم'].tolist()
    selected_name = st.selectbox("🎯 اختر الاسم لتعديله أو أضف جديداً", student_list)

    v_name, v_age, v_grade, v_id, v_phone, v_email = "", "", "", "", "", ""
    if selected_name != "➕ إضافة طالب جديد":
        row = bio_df[bio_df['الاسم'] == selected_name].iloc[0]
        v_name, v_age, v_grade, v_id, v_phone, v_email = str(row['الاسم']), str(row['العمر']), str(row['الصف']), str(row['الرقم']), str(row['الهاتف']), str(row['الإيميل'])

    with st.form("bio_form"):
        name = st.text_input("الاسم الثلاثي", value=v_name)
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade = st.selectbox("الصف", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", ids_list, index=ids_list.index(v_id) if v_id in ids_list else 0)
            phone = st.selectbox("الهاتف", phones_list, index=phones_list.index(v_phone) if v_phone in phones_list else 0)
        email = st.selectbox("الإيميل", emails_list, index=emails_list.index(v_email) if v_email in emails_list else 0)
        
        if st.form_submit_button("حفظ البيانات"):
            if name and s_id:
                new_data = bio_df[bio_df['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else bio_df
                new_row = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=DB_FILES["bio"][1])
                save_data(pd.concat([new_data, new_row], ignore_index=True), "bio")
                st.success("✅ تم الحفظ بنجاح")
                st.rerun()

# --- 2. رصد الدرجات (تم إصلاح خطأ الإزاحة هنا) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    bio = load_data("bio")
    grades_df = load_data("grades")
    
    with st.form("grade_form"):
        st_name = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q = c1.number_input("القرآن", 0, 100)
        f = c1.number_input("الفقه", 0, 100)
        h = c2.number_input("الحديث", 0, 100)
        s = c2.number_input("السيرة", 0, 100)
        
        if st.form_submit_button("ترحيل الدرجة"):
            if st_name:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                # إصلاح خطأ الإزاحة IndentationError
                if avg >= 90: تقدير = "ممتاز"
                elif avg >= 80: تقدير = "جيد جداً"
                elif avg >= 70: تقدير = "جيد"
                else: تقدير = "مقبول"
                
                new_g = pd.DataFrame([[st_name, q, f, h, s, round(avg, 2), تقدير]], columns=DB_FILES["grades"][1])
                updated = pd.concat([grades_df[grades_df['الاسم'] != st_name], new_g], ignore_index=True)
                save_data(updated, "grades")
                st.success(f"تم الحفظ بنجاح: {تقدير}")
                st.rerun()

# --- 3. السجل العام ---
elif menu == "📋 السجل العام":
    st.subheader("📁 جميع البيانات")
    st.dataframe(load_data("bio"), use_container_width=True)
    st.dataframe(load_data("grades"), use_container_width=True)
