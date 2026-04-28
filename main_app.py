import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام وتسريع الأداء ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

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
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() in ["ASSAF", "عساف"] and p == "7734":
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

# --- 1. بيانات الطلاب (إضافة، تعديل، حذف، بحث) ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    # قائمة المراحل الدراسية الشاملة
    stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", 
              "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]

    with st.expander("➕ إضافة طالب جديد", expanded=True):
        with st.form("bio_form", clear_on_submit=True):
            name = st.text_input("الاسم الثلاثي")
            col1, col2 = st.columns(2)
            with col1:
                age = st.selectbox("العمر", [""] + [str(i) for i in range(5, 50)])
                grade = st.selectbox("الصف الدراسي", stages)
            with col2:
                s_id = st.text_input("الرقم التسلسلي (ID)")
                phone = st.text_input("رقم الهاتف")
            email = st.text_input("البريد الإلكتروني")
            if st.form_submit_button("حفظ البيانات"):
                if name and s_id:
                    new = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=BIO.columns)
                    pd.concat([BIO, new], ignore_index=True).to_csv('db_bio.csv', index=False)
                    st.success(f"تم تسجيل الطالب {name} بنجاح")
                    st.rerun()

    st.divider()
    st.subheader("🔍 البحث والإدارة")
    search = st.text_input("ابحث عن اسم طالب للتعديل أو الحذف")
    filtered_bio = BIO[BIO['الاسم'].str.contains(search, na=False)] if search else BIO

    for i, row in filtered_bio.iterrows():
        with st.expander(f"👤 {row['الاسم']} ({row['الرقم']})"):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1: st.write(f"الصف: {row['الصف']} | الهاتف: {row['الهاتف']}")
            with c2:
                if st.button("حذف", key=f"del_{i}"):
                    BIO.drop(i).to_csv('db_bio.csv', index=False)
                    st.warning("تم الحذف")
                    st.rerun()
            with c3:
                st.info("للتعديل: احذف وأعد الإضافة بالبيانات الصحيحة لضمان الدقة")

# --- 2. التحضير اليومي ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ كشف الحضور")
    if not BIO.empty:
        with st.form("att_form", clear_on_submit=True):
            student = st.selectbox("اختر الطالب", [""] + BIO['الاسم'].tolist())
            status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])
            if st.form_submit_button("تسجيل"):
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
            with c3: page = st.selectbox("الصفحة", [f"صفحة {i}" for i in range(1, 100)])
            rate = st.selectbox("تقييم الحفظ", ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"])
            if st.form_submit_button("حفظ السجل"):
                new_h = pd.DataFrame([[st_name, part, sura, page, rate]], columns=HIFZ.columns)
                pd.concat([HIFZ, new_h], ignore_index=True).to_csv('db_hifz.csv', index=False)
                st.success("تم الحفظ بنجاح")

# --- 4. رصد الدرجات (إدخال يدوي مباشر) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    st.info("أدخل الدرجة مباشرة باستخدام لوحة المفاتيح")
    if not BIO.empty:
        with st.form("grade_form", clear_on_submit=True):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            # تم استخدام number_input بقيمة خطوة 1 لسهولة الإدخال اليدوي
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, step=1.0)
            f = col1.number_input("الفقه", 0.0, 100.0, step=1.0)
            h = col2.number_input("الحديث", 0.0, 100.0, step=1.0)
            s = col2.number_input("السيرة", 0.0, 100.0, step=1.0)
            if st.form_submit_button("ترحيل الدرجة النهائية"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
                pd.concat([GRADES[GRADES['الاسم'] != student], new_g], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم ترحيل المعدل: {round(avg, 2)}%")
                st.balloons()

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 كشوفات المنظومة")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "النتائج"])
    t1.dataframe(BIO, use_container_width=True)
    t2.dataframe(ATT, use_container_width=True)
    t3.dataframe(HIFZ, use_container_width=True)
    t4.dataframe(GRADES, use_container_width=True)

if st.sidebar.button("خروج"):
    st.session_state.auth = False
    st.rerun()
