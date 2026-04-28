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

# القوائم الثابتة
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]
att_status = ["حاضر", "غائب", "متأخر", "معتذر"]
parts = [str(i) for i in range(1, 31)]

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 تسجيل الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة تسجيل الطلاب (تم إضافة التعديل والحذف) ---
if menu == "🏠 تسجيل الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    df = load_data("bio")
    
    t1, t2 = st.tabs(["➕ إضافة جديد", "⚙️ تعديل وحذف"])
    
    with t1:
        with st.form("bio_form", clear_on_submit=True):
            name = st.text_input("الاسم الثلاثي")
            c1, c2 = st.columns(2)
            with c1:
                age = st.selectbox("العمر", ages, key="add_age")
                grade = st.selectbox("الصف الدراسي", stages, key="add_grade")
            with c2:
                s_id = st.selectbox("الرقم التسلسلي", ids, key="add_id")
                phone = st.selectbox("رقم الهاتف", phones, key="add_phone")
            email = st.selectbox("البريد الإلكتروني", emails, key="add_email")
            if st.form_submit_button("✅ حفظ البيانات"):
                if name and s_id:
                    new_row = pd.DataFrame([[name, s_id, age, grade, phone, email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df, new_row], ignore_index=True), "bio")
                    st.success("✔️ تم الحفظ")
                    st.rerun()

    with t2:
        if not df.empty:
            edit_name = st.selectbox("اختر طالب للتعديل أو الحذف", [""] + df['الاسم'].tolist())
            if edit_name:
                student_data = df[df['الاسم'] == edit_name].iloc[0]
                with st.form("edit_form"):
                    new_n = st.text_input("الاسم", value=student_data['الاسم'])
                    c1, c2 = st.columns(2)
                    new_a = c1.selectbox("العمر", ages, index=ages.index(str(student_data['العمر'])) if str(student_data['العمر']) in ages else 0)
                    new_g = c1.selectbox("الصف", stages, index=stages.index(student_data['الصف']) if student_data['الصف'] in stages else 0)
                    new_i = c2.selectbox("الرقم", ids, index=ids.index(student_data['الرقم']) if student_data['الرقم'] in ids else 0)
                    new_p = c2.selectbox("الهاتف", phones, index=phones.index(student_data['الهاتف']) if student_data['الهاتف'] in phones else 0)
                    
                    col_b1, col_b2 = st.columns(2)
                    if col_b1.form_submit_button("💾 حفظ التعديلات"):
                        df.loc[df['الاسم'] == edit_name, ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف']] = [new_n, new_i, new_a, new_g, new_p]
                        save_data(df, "bio")
                        st.success("تم التعديل")
                        st.rerun()
                    if col_b2.form_submit_button("🗑️ حذف الطالب", type="primary"):
                        df = df[df['الاسم'] != edit_name]
                        save_data(df, "bio")
                        st.warning("تم الحذف")
                        st.rerun()
        else:
            st.info("لا يوجد طلاب مسجلين.")

# --- 3. شاشة الحفظ (تم إضافة المعادلة الآلية للتقييم) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio = load_data("bio")
    hifz_df = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        part = c1.selectbox("الجزء", parts)
        surah = c1.text_input("السورة")
        pages = c2.number_input("عدد الصفحات المحفوظة اليوم", 1, 20)
        
        st.info("💡 التقييم يتم آلياً بناءً على عدد الصفحات")
        
        if st.form_submit_button("💾 حفظ السجل"):
            if student and surah:
                # --- معادلة التقييم الآلي ---
                if pages >= 15: eval_val = "ممتاز"
                elif pages >= 10: eval_val = "جيد جداً"
                elif pages >= 5: eval_val = "جيد"
                else: eval_val = "مقبول"
                
                new_h = pd.DataFrame([[student, part, surah, pages, eval_val]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz_df, new_h], ignore_index=True), "hifz")
                st.success(f"✔️ تم الحفظ. التقييم المستحق: {eval_val}")
                st.rerun()

# --- بقية الشاشات (التحضير، الدرجات، السجل) تبقى كما هي لضمان الاستقرار ---
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
                st.success(f"✔️ تم التحضير")
                st.rerun()

elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
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
                t = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), t]], columns=DB_CONFIG["grades"]["cols"])
                save_data(pd.concat([grades_df[grades_df['الاسم'] != student], new_g], ignore_index=True), "grades")
                st.success("✔️ تم الحفظ")
                st.rerun()

elif menu == "📋 السجل العام":
    st.header("📋 السجلات")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    with t1: st.dataframe(load_data("bio"), use_container_width=True)
    with t2: st.dataframe(load_data("att"), use_container_width=True)
    with t3: st.dataframe(load_data("hifz"), use_container_width=True)
    with t4: st.dataframe(load_data("grades"), use_container_width=True)
