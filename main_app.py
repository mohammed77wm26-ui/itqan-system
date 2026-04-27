import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام وتسريع الأداء ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# وظيفة تحميل البيانات السريعة جداً
def get_data(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file)

# --- نظام الحماية ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if u == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# تحميل القواعد
BIO = get_data('db_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = get_data('db_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = get_data('db_hifz.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = get_data('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. بيانات الطلاب ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 تسجيل البيانات")
    with st.form("bio_form", clear_on_submit=True):
        name = st.text_input("الاسم الثلاثي")
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", [""] + [str(i) for i in range(5, 30)])
            grade = st.selectbox("الصف", ["", "الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس"])
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", [""] + [f"ID-{i}" for i in range(100, 500)])
            phone = st.text_input("الهاتف")
        email = st.text_input("الإيميل")
        if st.form_submit_button("حفظ وإضافة جديد"):
            if name and s_id:
                new = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=BIO.columns)
                pd.concat([BIO, new], ignore_index=True).to_csv('db_bio.csv', index=False)
                st.success("تم الحفظ وتفريغ الخانات")
                st.rerun()

# --- 2. التحضير اليومي ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ كشف الحضور")
    if not BIO.empty:
        with st.form("att_form", clear_on_submit=True):
            student = st.selectbox("اختر الطالب", [""] + BIO['الاسم'].tolist())
            status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])
            if st.form_submit_button("تسجيل الحضور"):
                new_att = pd.DataFrame([[pd.Timestamp.now().date(), student, status]], columns=ATT.columns)
                pd.concat([ATT, new_att], ignore_index=True).to_csv('db_att.csv', index=False)
                st.success(f"تم تسجيل {student}")

# --- 3. متابعة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل الحفظ")
    if not BIO.empty:
        with st.form("hifz_form", clear_on_submit=True):
            st_name = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            c1, c2, c3 = st.columns(3)
            with c1: part = st.selectbox("الجزء", [f"جزء {i}" for i in range(1, 31)])
            with c2: sura = st.selectbox("السورة", ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"])
            with c3: page = st.selectbox("الصفحة", [f"صفحة {i}" for i in range(1, 51)])
            # التقييم أصبح قائمة منسدلة الآن
            rate = st.selectbox("تقييم الحفظ", ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"])
            if st.form_submit_button("حفظ سجل الحفظ"):
                new_h = pd.DataFrame([[st_name, part, sura, page, rate]], columns=HIFZ.columns)
                pd.concat([HIFZ, new_h], ignore_index=True).to_csv('db_hifz.csv', index=False)
                st.success("تم الحفظ وتفريغ الخانات")

# --- 4. رصد الدرجات (حقول فارغة وتلقائية) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        with st.form("grade_form", clear_on_submit=True):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            # الحقول تبدأ من 0.0 كما طلبت
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, 0.0)
            f = col1.number_input("الفقه", 0.0, 100.0, 0.0)
            h = col2.number_input("الحديث", 0.0, 100.0, 0.0)
            s = col2.number_input("السيرة", 0.0, 100.0, 0.0)
            if st.form_submit_button("ترحيل الدرجة"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
                pd.concat([GRADES[GRADES['الاسم'] != student], new_g], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم الترحيل بمعدل {round(avg, 2)}% وتصفير الحقول")
                st.balloons()

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 السجلات الكلية")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    t1.dataframe(BIO, use_container_width=True)
    t2.dataframe(ATT, use_container_width=True)
    t3.dataframe(HIFZ, use_container_width=True)
    t4.dataframe(GRADES, use_container_width=True)

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

