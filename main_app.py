import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# دالة ذكية لضمان وجود الأعمدة الصحيحة ومنع أخطاء KeyError
def get_data(file):
    cols = ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    data = pd.read_csv(file)
    # التأكد من مطابقة الأعمدة تماماً لما هو مبرمج
    if list(data.columns) != cols:
        data.columns = cols
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

# تحميل البيانات وتجهيز القوائم
BIO = get_data('db_bio.csv')
ATT = get_data('db_att.csv') if os.path.exists('db_att.csv') else pd.DataFrame(columns=['التاريخ', 'الاسم', 'الحالة'])
HIFZ = get_data('db_hifz.csv') if os.path.exists('db_hifz.csv') else pd.DataFrame(columns=['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = get_data('db_grades.csv') if os.path.exists('db_grades.csv') else pd.DataFrame(columns=['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- القوائم المنسدلة (Dropdowns) لكل الحقول ---
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
ids_list = [""] + [f"ID-{i}" for i in range(100, 1000)]
phones_list = [""] + [f"05{i:08d}" for i in range(1, 1000)] # مثال للقائمة
emails_list = ["", "student@itqan.com", "admin@itqan.com"]

# --- 1. شاشة بيانات الطلاب (تحكم كامل بالقوائم) ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    student_list = ["➕ إضافة طالب جديد"] + BIO['الاسم'].tolist()
    selected_name = st.selectbox("🎯 اختر طالب للتعديل أو أضف جديداً", student_list)

    # جلب البيانات لملء القوائم تلقائياً
    if selected_name != "➕ إضافة طالب جديد":
        row = BIO[BIO['الاسم'] == selected_name].iloc[0]
        v_name = row['الاسم']
        v_age = str(row['العمر'])
        v_grade = row['الصف']
        v_id = str(row['الرقم']) # تم تصحيح اسم العمود هنا لمنع KeyError
        v_phone = str(row['الهاتف'])
        v_email = row['الإيميل']
        btn_label = "تحديث البيانات"
    else:
        v_name, v_age, v_grade, v_id, v_phone, v_email = "", "", "", "", "", ""
        btn_label = "حفظ جديد"

    with st.form("bio_universal_form", clear_on_submit=(selected_name == "➕ إضافة طالب جديد")):
        name = st.text_input("الاسم الثلاثي (كتابة)", value=v_name)
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade = st.selectbox("الصف الدراسي", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", ids_list, index=ids_list.index(v_id) if v_id in ids_list else 0)
            phone = st.selectbox("رقم الهاتف", phones_list, index=phones_list.index(v_phone) if v_phone in phones_list else 0)
        
        email = st.selectbox("البريد الإلكتروني", emails_list, index=emails_list.index(v_email) if v_email in emails_list else 0)
        
        if st.form_submit_button(btn_label):
            if name and s_id:
                # حذف السجل القديم عند التحديث
                data_to_save = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
                new_entry = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=BIO.columns)
                pd.concat([data_to_save, new_entry], ignore_index=True).to_csv('db_bio.csv', index=False)
                st.success("✅ تمت العملية بنجاح")
                st.rerun()
            else: st.warning("الرجاء إدخال الاسم والرقم")

    if selected_name != "➕ إضافة طالب جديد":
        if st.button("🗑️ حذف هذا الطالب"):
            BIO[BIO['الاسم'] != selected_name].to_csv('db_bio.csv', index=False)
            st.rerun()

# --- بقية الشاشات (بنفس نظام القوائم المنسدلة للتقييم والدرجات) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        with st.form("grade_form", clear_on_submit=True):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            # إدخال رقمي مباشر (بدون + و -)
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, 0.0)
            f = col1.number_input("الفقه", 0.0, 100.0, 0.0)
            h = col2.number_input("الحديث", 0.0, 100.0, 0.0)
            s = col2.number_input("السيرة", 0.0, 100.0, 0.0)
            if st.form_submit_button("ترحيل"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])
                pd.concat([GRADES[GRADES['الاسم'] != student], new_g], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم الحفظ بنجاح! المعدل: {round(avg, 2)}%")
                st.balloons()
