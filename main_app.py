import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# دالة ذكية لإدارة الملفات ومنع أخطاء الأعمدة
def load_db(file_name, columns):
    if not os.path.exists(file_name):
        pd.DataFrame(columns=columns).to_csv(file_name, index=False)
    df = pd.read_csv(file_name)
    # التأكد من وجود كل الأعمدة المطلوبة
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]

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

# تحميل البيانات بالأعمدة الصحيحة لكل ملف لمنع الانهيار
BIO = load_db('db_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = load_db('db_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = load_db('db_hifz.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = load_db('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- القوائم المنسدلة الثابتة ---
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids_list = [""] + [f"ID-{i}" for i in range(100, 500)]
phones_list = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 100)] # قائمة تجريبية للهواتف
emails_list = ["", "student@itqan.com", "admin@itqan.com", "user@itqan.com"]

# --- 1. شاشة بيانات الطلاب ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    names_in_db = BIO['الاسم'].tolist()
    student_list = ["➕ إضافة طالب جديد"] + names_in_db
    selected_name = st.selectbox("🎯 ابحث عن طالب أو أضف جديداً", student_list)

    # تعبئة افتراضية
    v_name, v_age, v_grade, v_id, v_phone, v_email = "", "", "", "", "", ""
    btn_label = "حفظ طالب جديد"

    if selected_name != "➕ إضافة طالب جديد":
        row = BIO[BIO['الاسم'] == selected_name].iloc[0]
        v_name = str(row['الاسم'])
        v_age = str(row['العمر'])
        v_grade = str(row['الصف'])
        v_id = str(row['الرقم'])
        v_phone = str(row['الهاتف'])
        v_email = str(row['الإيميل'])
        btn_label = "تحديث البيانات"

    with st.form("bio_form"):
        name_input = st.text_input("الاسم الثلاثي (كتابة للتأكيد)", value=v_name)
        c1, c2 = st.columns(2)
        with c1:
            age_val = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade_val = st.selectbox("الصف الدراسي", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        with c2:
            id_val = st.selectbox("الرقم التسلسلي", ids_list, index=ids_list.index(v_id) if v_id in ids_list else 0)
            phone_val = st.selectbox("رقم الهاتف", phones_list, index=phones_list.index(v_phone) if v_phone in phones_list else 0)
        
        email_val = st.selectbox("البريد الإلكتروني", emails_list, index=emails_list.index(v_email) if v_email in emails_list else 0)
        
        if st.form_submit_button(btn_label):
            if name_input and id_val:
                # تحديث البيانات
                clean_bio = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
                new_entry = pd.DataFrame([[id_val, name_input, age_val, grade_val, phone_val, email_val]], columns=BIO.columns)
                pd.concat([clean_bio, new_entry], ignore_index=True).to_csv('db_bio.csv', index=False)
                st.success("✅ تم الحفظ بنجاح")
                st.rerun()

    if selected_name != "➕ إضافة طالب جديد":
        if st.button("🗑️ حذف هذا الطالب"):
            BIO[BIO['الاسم'] != selected_name].to_csv('db_bio.csv', index=False)
            st.rerun()

# --- 2. رصد الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        with st.form("grade_form"):
            student = st.selectbox("اختر الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, step=1.0)
            f = col1.number_input("الفقه", 0.0, 100.0, step=1.0)
            h = col2.number_input("الحديث", 0.0, 100.0, step=1.0)
            s = col2.number_input("السيرة", 0.0, 100.0, step=1.0)
            if st.form_submit_button("ترحيل الدرجة"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_grade = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
                pd.concat([GRADES[GRADES['الاسم'] != student], new_grade], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم الترحيل! المعدل: {round(avg, 2)}%")

# --- شاشات أخرى سريعة ---
elif menu == "📋 السجل العام":
    st.dataframe(BIO, use_container_width=True)
    st.dataframe(GRADES, use_container_width=True)
