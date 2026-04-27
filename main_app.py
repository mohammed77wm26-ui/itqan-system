import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# دالة ذكية لإدارة قواعد البيانات
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

# --- 1. شاشة الأسماء (قوائم منسدلة) ---
if menu == "بيانات الطلاب":
    st.header("📝 تسجيل البيانات")
    with st.form("bio_form"):
        name = st.text_input("الاسم الثلاثي")
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", [str(i) for i in range(5, 25)])
            grade_level = st.selectbox("الصف", ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس"])
        with col2:
            s_id = st.selectbox("الرقم التسلسلي", [f"ID-{i}" for i in range(100, 500)])
            phone = st.text_input("رقم الهاتف")
        email = st.text_input("البريد الإلكتروني")
        
        if st.form_submit_button("حفظ البيانات"):
            if name:
                new_data = pd.DataFrame([[s_id, name, age, grade_level, phone, email]], columns=BIO.columns)
                BIO = pd.concat([BIO, new_data], ignore_index=True)
                BIO.to_csv('students_bio.csv', index=False)
                st.success("تم الحفظ!")
            else: st.error("يرجى كتابة الاسم")

# --- 2. التحضير اليومي ---
elif menu == "التحضير اليومي":
    st.header("✅ كشف الحضور")
    if not BIO.empty:
        selected_student = st.selectbox("اختر الطالب", BIO['الاسم'])
        status = st.selectbox("الحالة اليومية", ["حاضر", "غائب", "بعذر"])
        if st.button("تسجيل الحالة"):
            new_att = pd.DataFrame([[pd.Timestamp.now().date(), selected_student, status]], columns=ATT.columns)
            ATT = pd.concat([ATT, new_att], ignore_index=True)
            ATT.to_csv('daily_att.csv', index=False)
            st.success(f"تم تسجيل {selected_student}")

# --- 3. متابعة الحفظ (قوائم شاملة) ---
elif menu == "متابعة الحفظ":
    st.header("📖 متابعة الحفظ والجزئية")
    suras = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]
    if not BIO.empty:
        st_name = st.selectbox("الطالب", BIO['الاسم'])
        c1, c2, c3 = st.columns(3)
        part = c1.selectbox("الجزء", [f"جزء {i}" for i in range(1, 31)])
        sura = c2.selectbox("السورة", suras)
        pages = c3.selectbox("عدد الصفحات المنجزة", [f"{i} صفحات" for i in range(1, 51)])
        rate = st.select_slider("التقييم", ["ضعيف", "مقبول", "جيد", "جيد جداً", "ممتاز"])
        
        if st.button("حفظ سجل الحفظ"):
            new_h = pd.DataFrame([[st_name, part, sura, pages, rate]], columns=HIFZ.columns)
            HIFZ = pd.concat([HIFZ, new_h], ignore_index=True)
            HIFZ.to_csv('hifz_track.csv', index=False)
            st.success("تم الحفظ في سجل الحفظ")

# --- 4. رصد الدرجات (الحساب الاحترافي) ---
elif menu == "رصد الدرجات":
    st.header("🎯 نظام رصد الدرجات الاحترافي")
    if not BIO.empty:
        student = st.selectbox("اختر الطالب للرصد", BIO['الاسم'])
        col1, col2 = st.columns(2)
        with col1:
            q = st.number_input("القرآن (50%)", 0.0, 100.0, 90.0)
            f = st.number_input("الفقه", 0.0, 100.0, 90.0)
        with col2:
            h = st.number_input("الحديث", 0.0, 100.0, 90.0)
            s = st.number_input("السيرة", 0.0, 100.0, 90.0)
            
        if st.button("ترحيل وحفظ"):
            # المعادلة: القرآن 50% + (متوسط المواد الثلاث الأخرى) 50%
            total_avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
             تقدير = "ممتاز" if total_avg >= 90 else "جيد جداً" if total_avg >= 80 else "جيد" if total_avg >= 70 else "مقبول"
            
            # منع تكرار الطالب وتحديث درجته
            GRADES = GRADES[GRADES['الاسم'] != student] # حذف القديم إن وجد
            new_g = pd.DataFrame([[student, q, f, h, s, round(total_avg, 2), تقدير]], columns=GRADES.columns)
            GRADES = pd.concat([GRADES, new_g], ignore_index=True)
            GRADES.to_csv('final_grades.csv', index=False)
            st.success(f"تم الترحيل! المعدل: {round(total_avg, 2)}%")
            st.balloons()

# --- 5. السجل العام (بدون تغيير) ---
elif menu == "السجل العام":
    st.header("📋 سجل البيانات والنتائج")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    with t1: st.dataframe(BIO, use_container_width=True)
    with t2: st.dataframe(ATT, use_container_width=True)
    with t3: st.dataframe(HIFZ, use_container_width=True)
    with t4: st.dataframe(GRADES, use_container_width=True)

if st.sidebar.button("خروج"):
    st.session_state.locked = True
    st.rerun()
