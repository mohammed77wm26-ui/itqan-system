import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

def get_data(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    data = pd.read_csv(file)
    for col in cols:
        if col not in data.columns: data[col] = ""
    return data

# --- نظام الحماية ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() in ["ASSAF", "عساف"] and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# تحميل البيانات
BIO = get_data('db_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- القوائم الثابتة ---
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones = [""] + [f"05{i:08d}" for i in range(0, 1000)] # مثال لقائمة هواتف، يفضل كتابتها يدوياً أو تركها نصية إذا كانت متغيرة جداً
emails = ["", "student@example.com", "user@itqan.com"]

# --- 1. شاشة بيانات الطلاب (كل شيء قوائم منسدلة) ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    student_list = ["➕ إضافة طالب جديد"] + BIO['الاسم'].tolist()
    selected_name = st.selectbox("🎯 اختر الاسم (للبحث أو التعديل)", student_list)

    # جلب البيانات لوضعها في القوائم عند التعديل
    if selected_name != "➕ إضافة طالب جديد":
        row = BIO[BIO['الاسم'] == selected_name].iloc[0]
        v_name, v_age, v_grade, v_id, v_phone, v_email = row['الاسم'], str(row['العمر']), row['الصف'], str(row['الالرقم']), str(row['الهاتف']), row['الإيميل']
        btn_label = "تحديث البيانات"
    else:
        v_name, v_age, v_grade, v_id, v_phone, v_email = "", "", "", "", "", ""
        btn_label = "حفظ جديد"

    with st.form("universal_form"):
        # حقل الاسم (نصي للإضافة، وقائمة للاختيار من الأعلى)
        name = st.text_input("تأكيد الاسم الثلاثي", value=v_name)
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade = st.selectbox("الصف الدراسي", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", ids, index=ids.index(v_id) if v_id in ids else 0)
            phone = st.selectbox("رقم الهاتف (قائمة)", phones, index=phones.index(v_phone) if v_phone in phones else 0)
            
        email = st.selectbox("البريد الإلكتروني", emails, index=emails.index(v_email) if v_email in emails else 0)
        
        if st.form_submit_button(btn_label):
            if name and s_id:
                new_data = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
                new_row = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=BIO.columns)
                pd.concat([new_data, new_row], ignore_index=True).to_csv('db_bio.csv', index=False)
                st.success("تمت العملية بنجاح!")
                st.rerun()

    if selected_name != "➕ إضافة طالب جديد":
        if st.button("🗑️ حذف الطالب"):
            BIO[BIO['الاسم'] != selected_name].to_csv('db_bio.csv', index=False)
            st.rerun()

# (بقية الشاشات تستمر بنفس المنطق لضمان عدم وجود أخطاء)
