import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

def get_data(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file)

# --- الحماية ---
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
ATT = get_data('db_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = get_data('db_hifz.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = get_data('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

STAGES = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", 
          "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]

# --- 1. بيانات الطلاب ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    tab_add, tab_edit = st.tabs(["➕ إضافة طالب جديد", "🔍 بحث وتعديل طالب موجود"])
    
    with tab_add:
        with st.form("add_form", clear_on_submit=True):
            n_name = st.text_input("الاسم الثلاثي")
            c1, c2 = st.columns(2)
            n_age = c1.selectbox("العمر", [""] + [str(i) for i in range(5, 51)], key="n_age")
            n_grade = c1.selectbox("الصف", STAGES, key="n_grade")
            n_id = c2.text_input("الرقم التسلسلي")
            n_phone = c2.text_input("الهاتف")
            n_email = st.text_input("الإيميل")
            if st.form_submit_button("حفظ الطالب الجديد"):
                if n_name and n_id:
                    new_row = pd.DataFrame([[n_id, n_name, n_age, n_grade, n_phone, n_email]], columns=BIO.columns)
                    pd.concat([BIO, new_row], ignore_index=True).to_csv('db_bio.csv', index=False)
                    st.success("تم الحفظ")
                    st.rerun()

    with tab_edit:
        if not BIO.empty:
            edit_name = st.selectbox("اختر الطالب للتعديل", [""] + BIO['الاسم'].tolist())
            if edit_name:
                s_data = BIO[BIO['الاسم'] == edit_name].iloc[0]
                with st.form("edit_form"):
                    u_name = st.text_input("الاسم", value=str(s_data['الاسم']))
                    c1, c2 = st.columns(2)
                    u_age = c1.text_input("العمر (حالي: " + str(s_data['العمر']) + ")", value=str(s_data['العمر']))
                    u_grade = c1.selectbox("الصف الدراسي", STAGES, index=(STAGES.index(s_data['الصف']) if s_data['الصف'] in STAGES else 0))
                    u_id = c2.text_input("الرقم التسلسلي", value=str(s_data['الرقم']))
                    u_phone = c2.text_input("رقم الهاتف", value=str(s_data['الهاتف']))
                    u_email = st.text_input("الإيميل", value=str(s_data['الإيميل']))
                    
                    cc1, cc2 = st.columns(2)
                    if cc1.form_submit_button("تحديث البيانات"):
                        updated_df = BIO[BIO['الاسم'] != edit_name]
                        new_row = pd.DataFrame([[u_id, u_name, u_age, u_grade, u_phone, u_email]], columns=BIO.columns)
                        pd.concat([updated_df, new_row], ignore_index=True).to_csv('db_bio.csv', index=False)
                        st.success("تم التعديل")
                        st.rerun()
                    if cc2.form_submit_button("🗑️ حذف الطالب نهائياً"):
                        BIO[BIO['الاسم'] != edit_name].to_csv('db_bio.csv', index=False)
                        st.warning("تم الحذف")
                        st.rerun()

# --- 2. التحضير اليومي ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ التحضير اليومي")
    if not BIO.empty:
        with st.form("att_form", clear_on_submit=True):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])
            if st.form_submit_button("تسجيل"):
                new_att = pd.DataFrame([[pd.Timestamp.now().date(), student, status]], columns=ATT.columns)
                pd.concat([ATT, new_att], ignore_index=True).to_csv('db_att.csv', index=False)
                st.success("تم التسجيل")

# --- 3. متابعة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل الحفظ")
    if not BIO.empty:
        with st.form("hifz_form", clear_on_submit=True):
            st_name = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            c1, c2, c3 = st.columns(3)
            part = c1.selectbox("الجزء", [f"جزء {i}" for i in range(1, 31)])
            sura = c2.selectbox("السورة", ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"])
            page = c3.selectbox("الصفحة", [f"صفحة {i}" for i in range(1, 605)])
            rate = st.selectbox("التقييم", ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"])
            if st.form_submit_button("حفظ السجل"):
                new_h = pd.DataFrame([[st_name, part, sura, page, rate]], columns=HIFZ.columns)
                pd.concat([HIFZ, new_h], ignore_index=True).to_csv('db_hifz.csv', index=False)
                st.success("تم الحفظ")

# --- 4. رصد الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        with st.form("grade_form", clear_on_submit=True):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, step=1.0)
            f = col1.number_input("الفقه", 0.0, 100.0, step=1.0)
            h = col2.number_input("الحديث", 0.0, 100.0, step=1.0)
            s = col2.number_input("السيرة", 0.0, 100.0, step=1.0)
            if st.form_submit_button("ترحيل الدرجة"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
                pd.concat([GRADES[GRADES['الاسم'] != student], new_g], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم الترحيل: {round(avg, 2)}%")

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 السجلات")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "النتائج"])
    t1.dataframe(BIO, use_container_width=True)
    t2.dataframe(ATT, use_container_width=True)
    t3.dataframe(HIFZ, use_container_width=True)
    t4.dataframe(GRADES, use_container_width=True)

if st.sidebar.button("خروج"):
    st.session_state.auth = False
    st.rerun()
