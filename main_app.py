import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعدادات عامة
# =========================
st.set_page_config(
    page_title="منظومة إتقان الاحترافية",
    layout="wide",
    page_icon="🌟"
)

# =========================
# ثوابت الملفات والأعمدة
# =========================
DB_BIO_FILE = "db_bio.csv"
DB_ATT_FILE = "db_att.csv"
DB_HIFZ_FILE = "db_hifz.csv"
DB_GRADES_FILE = "db_grades.csv"

BIO_COLUMNS = ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']
ATT_COLUMNS = ['التاريخ', 'الاسم', 'الحالة']
HIFZ_COLUMNS = ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم']
GRADES_COLUMNS = ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']

# =========================
# دوال مساعدة للملفات
# =========================
@st.cache_data
def load_db(file_name: str, columns: list) -> pd.DataFrame:
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
    else:
        df = pd.read_csv(file_name, encoding="utf-8-sig")
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]


def save_db(df: pd.DataFrame, file_name: str):
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    load_db.clear()


# =========================
# نظام الدخول
# =========================
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'username' not in st.session_state:
    st.session_state.username = ""

if not st.session_state.auth:
    st.markdown(
        "<h2 style='text-align: center;'>🔐 دخول منظومة إتقان الاحترافية</h2>",
        unsafe_allow_html=True
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() in ["ASSAF", "عساف"] and p == "7734":
                st.session_state.auth = True
                st.session_state.username = u
                st.success("تم تسجيل الدخول بنجاح")
                st.rerun()
            else:
                st.error("خطأ في البيانات")
    st.stop()

# =========================
# تحميل قواعد البيانات
# =========================
BIO = load_db(DB_BIO_FILE, BIO_COLUMNS)
ATT = load_db(DB_ATT_FILE, ATT_COLUMNS)
HIFZ = load_db(DB_HIFZ_FILE, HIFZ_COLUMNS)
GRADES = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

# =========================
# شريط علوي
# =========================
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown("## 🌟 منظومة إتقان الاحترافية")
with top_col2:
    st.markdown(f"#### 👤 المستخدم: **{st.session_state.username}**")
    if st.button("تسجيل خروج"):
        st.session_state.auth = False
        st.session_state.username = ""
        st.rerun()

# =========================
# القوائم الثابتة
# =========================
stages = [
    "", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي",
    "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط",
    "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"
]
ages = [""] + [str(i) for i in range(5, 51)]
ids_list = [""] + [f"ID-{i}" for i in range(100, 500)]
phones_list = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 100)]
emails_list = ["", "student@itqan.com", "admin@itqan.com", "user@itqan.com"]

attendance_status = ["حاضر", "غائب", "متأخر", "معتذر"]
hifz_eval_list = ["ممتاز", "جيد جداً", "جيد", "مقبول", "يحتاج متابعة"]

# =========================
# شاشة بيانات الطلاب — مع تفريغ تلقائي بعد الحفظ
# =========================
def screen_students():
    st.header("📝 إدارة بيانات الطلاب")

    names_in_db = BIO['الاسم'].dropna().tolist()
    student_list = ["➕ إضافة طالب جديد"] + names_in_db

    if "student_selector" not in st.session_state:
        st.session_state.student_selector = "➕ إضافة طالب جديد"

    selected_name = st.selectbox(
        "🎯 اختر طالباً أو أضف جديداً",
        student_list,
        key="student_selector"
    )

    # تهيئة الحقول
    for key in ["name_input", "age_val", "grade_val", "id_val", "phone_val", "email_val"]:
        st.session_state.setdefault(key, "")

    if selected_name != "➕ إضافة طالب جديد":
        row = BIO[BIO['الاسم'] == selected_name].iloc[0]
        st.session_state.name_input = row['الاسم']
        st.session_state.age_val = row['العمر']
        st.session_state.grade_val = row['الصف']
        st.session_state.id_val = row['الرقم']
        st.session_state.phone_val = row['الهاتف']
        st.session_state.email_val = row['الإيميل']
        btn_label = "تحديث البيانات"
    else:
        btn_label = "حفظ طالب جديد"

    with st.form("bio_form"):
        st.session_state.name_input = st.text_input("الاسم الثلاثي", st.session_state.name_input)

        c1, c2 = st.columns(2)
        with c1:
            st.session_state.age_val = st.selectbox("العمر", ages, index=ages.index(st.session_state.age_val) if st.session_state.age_val in ages else 0)
            st.session_state.grade_val = st.selectbox("الصف الدراسي", stages, index=stages.index(st.session_state.grade_val) if st.session_state.grade_val in stages else 0)
        with c2:
            st.session_state.id_val = st.selectbox("الرقم التسلسلي", ids_list, index=ids_list.index(st.session_state.id_val) if st.session_state.id_val in ids_list else 0)
            st.session_state.phone_val = st.selectbox("رقم الهاتف", phones_list, index=phones_list.index(st.session_state.phone_val) if st.session_state.phone_val in phones_list else 0)

        st.session_state.email_val = st.selectbox("البريد الإلكتروني", emails_list, index=emails_list.index(st.session_state.email_val) if st.session_state.email_val in emails_list else 0)

        if st.form_submit_button(btn_label):

            clean_bio = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
            new_entry = pd.DataFrame([[
                st.session_state.id_val,
                st.session_state.name_input,
                st.session_state.age_val,
                st.session_state.grade_val,
                st.session_state.phone_val,
                st.session_state.email_val
            ]], columns=BIO.columns)

            updated = pd.concat([clean_bio, new_entry], ignore_index=True)
            save_db(updated, DB_BIO_FILE)

            # تفريغ الحقول
            for key in ["name_input", "age_val", "grade_val", "id_val", "phone_val", "email_val"]:
                st.session_state[key] = ""

            st.session_state.student_selector = "➕ إضافة طالب جديد"

            st.success("تم الحفظ وتم تفريغ الحقول تلقائياً")
            st.rerun()


# =========================
# شاشة التحضير — كلها قوائم منسدلة
# =========================
def screen_attendance():
    st.header("✅ التحضير اليومي")

    with st.form("att_form"):
        date_val = st.date_input("التاريخ", datetime.today())
        student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
        status = st.selectbox("الحالة", attendance_status)

        if st.form_submit_button("حفظ"):
            if student:
                new_att = pd.DataFrame([[date_val, student, status]], columns=ATT_COLUMNS)
                updated = pd.concat([ATT, new_att], ignore_index=True)
                save_db(updated, DB_ATT_FILE)
                st.success("تم الحفظ")
                st.rerun()
            else:
                st.error("اختر الطالب")


# =========================
# شاشة الحفظ — كلها قوائم منسدلة
# =========================
def screen_hifz():
    st.header("📖 متابعة الحفظ")

    with st.form("hifz_form"):
        student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
        part = st.selectbox("الجزء", [str(i) for i in range(1, 31)])
        surah = st.text_input("السورة")
        pages = st.number_input("عدد الصفحات", 1, 20)
        eval_val = st.selectbox("التقييم", hifz_eval_list)

        if st.form_submit_button("حفظ"):
            if student and surah:
                new_hifz = pd.DataFrame([[student, part, surah, pages, eval_val]], columns=HIFZ_COLUMNS)
                updated = pd.concat([HIFZ, new_hifz], ignore_index=True)
                save_db(updated, DB_HIFZ_FILE)
                st.success("تم الحفظ")
                st.rerun()
            else:
                st.error("أكمل البيانات")


# =========================
# شاشة الدرجات — كلها قوائم منسدلة
# =========================
def screen_grades():
    st.header("🎯 رصد الدرجات")

    with st.form("grade_form"):
        student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
        q = st.number_input("القرآن", 0, 100)
        f = st.number_input("الفقه", 0, 100)
        h = st.number_input("الحديث", 0, 100)
        s = st.number_input("السيرة", 0, 100)

        if st.form_submit_button("حفظ"):
            if student:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                grade = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"

                new_grade = pd.DataFrame([[student, q, f, h, s, avg, grade]], columns=GRADES_COLUMNS)
                updated = pd.concat([GRADES[GRADES['الاسم'] != student], new_grade], ignore_index=True)
                save_db(updated, DB_GRADES_FILE)
                st.success("تم الحفظ")
                st.rerun()
            else:
                st.error("اختر الطالب")


# =========================
# شاشة السجل العام
# =========================
def screen_log():
    st.header("📋 السجل العام")
    st.dataframe(BIO)
    st.dataframe(ATT)
    st.dataframe(HIFZ)
    st.dataframe(GRADES)


# =========================
# القائمة الجانبية
# =========================
menu = st.sidebar.radio(
    "القائمة",
    ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"]
)

if menu == "🏠 بيانات الطلاب":
    screen_students()
elif menu == "✅ التحضير اليومي":
    screen_attendance()
elif menu == "📖 متابعة الحفظ":
    screen_hifz()
elif menu == "🎯 رصد الدرجات":
    screen_grades()
elif menu == "📋 السجل العام":
    screen_log()



