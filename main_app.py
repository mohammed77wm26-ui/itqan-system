import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

def get_db(file_name, cols):
    if not os.path.exists(file_name):
        pd.DataFrame(columns=cols).to_csv(file_name, index=False)
    return pd.read_csv(file_name)

# --- نظام الحماية ---
if 'locked' not in st.session_state: st.session_state.locked = True

if st.session_state.locked:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if u == "ASSAF" and p == "7734":
                st.session_state.locked = False
                st.rerun()
            else: st.error("البيانات خاطئة")
    st.stop()

# --- تحميل البيانات ---
BIO = get_db('students_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = get_db('daily_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = get_db('hifz_track.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = get_db('final_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["بيانات الطلاب", "التحضير اليومي", "متابعة الحفظ", "رصد الدرجات", "السجل العام"])

# --- 1. شاشة الأسماء ---
if menu == "بيانات الطلاب":
    st.header("📝 تسجيل البيانات")
    with st.form("bio_form"):
        name = st.text_input("الاسم الثلاثي")
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", [str(i) for i in range(5, 30)])
            grade_level = st.selectbox("الصف", ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس"])
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", [f"ID-{i}" for i in range(100, 500)])
            phone = st.text_input("رقم الهاتف")
        email = st.text_input("البريد الإلكتروني")
        if st.form_submit_button("حفظ البيانات"):
            if name:
                new_row = pd.DataFrame([[s_id, name, age, grade_level, phone, email]], columns=BIO.columns)
                pd.concat([BIO, new_row], ignore_index=True).to_csv('students_bio.csv', index=False)
                st.success("تم الحفظ بنجاح!")
                st.rerun()

# --- 2. التحضير اليومي ---
elif menu == "التحضير اليومي":
    st.header("✅ كشف الحضور")
    if not BIO.empty:
        student = st.selectbox("اختر الطالب", BIO['الاسم'])
        status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])
        if st.button("تسجيل"):
            new_att = pd.DataFrame([[pd.Timestamp.now().date(), student, status]], columns=ATT.columns)
            pd.concat([ATT, new_att], ignore_index=True).to_csv('daily_att.csv', index=False)
            st.success("تم التسجيل")

# --- 3. متابعة الحفظ ---
elif menu == "متابعة الحفظ":
    st.header("📖 سجل الحفظ")
    suras = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]
    if not BIO.empty:
        st_name = st.selectbox("الطالب", BIO['الاسم'])
        c1, c2, c3 = st.columns(3)
        part = c1.selectbox("الجزء", [f"جزء {i}" for i in range(1, 31)])
        sura = c2.selectbox("السورة", suras)
        pages = c3.selectbox("الصفحات", [f"صفحة {i}" for i in range(1, 51)])
        rate = st.select_slider("التقييم", ["ضعيف", "جيد", "ممتاز"])
        if st.button("حفظ"):
            new_h = pd.DataFrame([[st_name, part, sura, pages, rate]], columns=HIFZ.columns)
            pd.concat([HIFZ, new_h], ignore_index=True).to_csv('hifz_track.csv', index=False)
            st.success("تم الحفظ")

# --- 4. رصد الدرجات ---
elif menu == "رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        student = st.selectbox("الطالب", BIO['الاسم'])
        col1, col2 = st.columns(2)
        q = col1.number_input("القرآن (50%)", 0.0, 100.0, 90.0)
        f = col1.number_input("الفقه", 0.0, 100.0, 90.0)
        h = col2.number_input("الحديث", 0.0, 100.0, 90.0)
        s = col2.number_input("السيرة", 0.0, 100.0, 90.0)
        if st.button("ترحيل"):
            avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
            # تم إصلاح السطر الذي تسبب في الخطأ بالصورة:
            if avg >= 90: تقدير = "ممتاز"
            elif avg >= 80: تقدير = "جيد جداً"
            elif avg >= 70: تقدير = "جيد"
            else: تقدير = "مقبول"
            
            GRADES = GRADES[GRADES['الاسم'] != student]
            new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
            pd.concat([GRADES, new_g], ignore_index=True).to_csv('final_grades.csv', index=False)
            st.success(f"تم الترحيل بمعدل {round(avg, 2)}%")
            st.balloons()

# --- 5. السجل العام ---
elif menu == "السجل العام":
    st.header("📋 السجلات")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    t1.dataframe(BIO, use_container_width=True)
    t2.dataframe(ATT, use_container_width=True)
    t3.dataframe(HIFZ, use_container_width=True)
    t4.dataframe(GRADES, use_container_width=True)

if st.sidebar.button("خروج"):
    st.session_state.locked = True
    st.rerun()

