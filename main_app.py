أفهم إحباطك، فخلّينا نعيد ضبط كل شيء بوضوح وبدون لفّ ودوران:  
الكود التالي فيه:

- **تصفير كامل للنظام** من شاشة السجل العام (يمسح كل الملفات ويعيدها فاضية فعلياً).
- **إلغاء الكاش** نهائياً لتفادي بقاء البيانات القديمة.
- **الاعتماد على القوائم المنسدلة في كل الشاشات** قدر الإمكان.
- **تفريغ حقول بيانات الطالب تلقائياً بعد الحفظ** مع إعادة المؤشر إلى "إضافة طالب جديد" وعدم بقاء بياناته في الحقول.

> انسخ الكود كاملاً كما هو، وضعه مكان ملف التطبيق الحالي.

```python
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
# دوال مساعدة للملفات (بدون كاش)
# =========================
def ensure_db(file_name: str, columns: list):
    if not os.path.exists(file_name):
        pd.DataFrame(columns=columns).to_csv(file_name, index=False, encoding="utf-8-sig")


def load_db(file_name: str, columns: list) -> pd.DataFrame:
    ensure_db(file_name, columns)
    df = pd.read_csv(file_name, encoding="utf-8-sig")
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]


def save_db(df: pd.DataFrame, file_name: str, columns: list):
    df[columns].to_csv(file_name, index=False, encoding="utf-8-sig")


def reset_all_dbs():
    pd.DataFrame(columns=BIO_COLUMNS).to_csv(DB_BIO_FILE, index=False, encoding="utf-8-sig")
    pd.DataFrame(columns=ATT_COLUMNS).to_csv(DB_ATT_FILE, index=False, encoding="utf-8-sig")
    pd.DataFrame(columns=HIFZ_COLUMNS).to_csv(DB_HIFZ_FILE, index=False, encoding="utf-8-sig")
    pd.DataFrame(columns=GRADES_COLUMNS).to_csv(DB_GRADES_FILE, index=False, encoding="utf-8-sig")


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
                st.rerun()
            else:
                st.error("خطأ في البيانات")
    st.stop()

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
parts_list = [str(i) for i in range(1, 31)]

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
# شاشة بيانات الطلاب (تفريغ تلقائي بعد الحفظ)
# =========================
def screen_students():
    st.header("📝 إدارة بيانات الطلاب")

    bio_df = load_db(DB_BIO_FILE, BIO_COLUMNS)
    names_in_db = bio_df['الاسم'].dropna().tolist()
    student_list = ["➕ إضافة طالب جديد"] + names_in_db

    if "student_selector" not in st.session_state:
        st.session_state.student_selector = "➕ إضافة طالب جديد"

    selected_name = st.selectbox(
        "🎯 اختر طالباً أو أضف جديداً",
        student_list,
        key="student_selector"
    )

    # تهيئة الحقول في session_state
    defaults = {
        "name_input": "",
        "age_val": "",
        "grade_val": "",
        "id_val": "",
        "phone_val": "",
        "email_val": ""
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

    if selected_name != "➕ إضافة طالب جديد":
        row = bio_df[bio_df['الاسم'] == selected_name].iloc[0]
        st.session_state.name_input = str(row['الاسم'])
        st.session_state.age_val = str(row['العمر'])
        st.session_state.grade_val = str(row['الصف'])
        st.session_state.id_val = str(row['الرقم'])
        st.session_state.phone_val = str(row['الهاتف'])
        st.session_state.email_val = str(row['الإيميل'])
        btn_label = "تحديث البيانات"
    else:
        btn_label = "حفظ طالب جديد"

    with st.form("bio_form"):
        st.session_state.name_input = st.text_input("الاسم الثلاثي", st.session_state.name_input)

        c1, c2 = st.columns(2)
        with c1:
            st.session_state.age_val = st.selectbox(
                "العمر", ages,
                index=ages.index(st.session_state.age_val) if st.session_state.age_val in ages else 0
            )
            st.session_state.grade_val = st.selectbox(
                "الصف الدراسي", stages,
                index=stages.index(st.session_state.grade_val) if st.session_state.grade_val in stages else 0
            )
        with c2:
            st.session_state.id_val = st.selectbox(
                "الرقم التسلسلي", ids_list,
                index=ids_list.index(st.session_state.id_val) if st.session_state.id_val in ids_list else 0
            )
            st.session_state.phone_val = st.selectbox(
                "رقم الهاتف", phones_list,
                index=phones_list.index(st.session_state.phone_val) if st.session_state.phone_val in phones_list else 0
            )

        st.session_state.email_val = st.selectbox(
            "البريد الإلكتروني", emails_list,
            index=emails_list.index(st.session_state.email_val) if st.session_state.email_val in emails_list else 0
        )

        if st.form_submit_button(btn_label):
            if not st.session_state.name_input:
                st.error("الرجاء إدخال اسم الطالب.")
            elif not st.session_state.id_val:
                st.error("الرجاء اختيار الرقم التسلسلي.")
            else:
                clean_bio = bio_df[bio_df['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else bio_df
                new_entry = pd.DataFrame([[
                    st.session_state.id_val,
                    st.session_state.name_input,
                    st.session_state.age_val,
                    st.session_state.grade_val,
                    st.session_state.phone_val,
                    st.session_state.email_val
                ]], columns=BIO_COLUMNS)
                updated = pd.concat([clean_bio, new_entry], ignore_index=True)
                save_db(updated, DB_BIO_FILE)

                # تفريغ الحقول بالكامل بعد الحفظ
                for k in defaults.keys():
                    st.session_state[k] = ""
                st.session_state.student_selector = "➕ إضافة طالب جديد"

                st.success("✅ تم الحفظ وتم تفريغ الحقول لإضافة طالب جديد.")
                st.rerun()

    # حذف الطالب ومتعلقاته (اختياري)
    if selected_name != "➕ إضافة طالب جديد":
        if st.button("🗑️ حذف هذا الطالب وجميع سجلاته"):
            att_df = load_db(DB_ATT_FILE, ATT_COLUMNS)
            hifz_df = load_db(DB_HIFZ_FILE, HIFZ_COLUMNS)
            grades_df = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

            bio_df = bio_df[bio_df['الاسم'] != selected_name]
            att_df = att_df[att_df['الاسم'] != selected_name]
            hifz_df = hifz_df[hifz_df['الاسم'] != selected_name]
            grades_df = grades_df[grades_df['الاسم'] != selected_name]

            save_db(bio_df, DB_BIO_FILE, BIO_COLUMNS)
            save_db(att_df, DB_ATT_FILE, ATT_COLUMNS)
            save_db(hifz_df, DB_HIFZ_FILE, HIFZ_COLUMNS)
            save_db(grades_df, DB_GRADES_FILE, GRADES_COLUMNS)

            st.session_state.student_selector = "➕ إضافة طالب جديد"
            st.success("🚮 تم حذف الطالب وكل متعلقاته.")
            st.rerun()


# =========================
# شاشة التحضير — قوائم منسدلة بالكامل
# =========================
def screen_attendance():
    st.header("✅ التحضير اليومي")

    bio_df = load_db(DB_BIO_FILE, BIO_COLUMNS)
    att_df = load_db(DB_ATT_FILE, ATT_COLUMNS)

    with st.form("att_form"):
        date_val = st.date_input("التاريخ", datetime.today())
        student = st.selectbox("الطالب", [""] + bio_df['الاسم'].dropna().tolist())
        status = st.selectbox("الحالة", attendance_status)

        if st.form_submit_button("حفظ"):
            if not student:
                st.error("اختر الطالب.")
            else:
                new_att = pd.DataFrame([[date_val.strftime("%Y-%m-%d"), student, status]], columns=ATT_COLUMNS)
                updated = pd.concat([att_df, new_att], ignore_index=True)
                save_db(updated, DB_ATT_FILE, ATT_COLUMNS)
                st.success("تم حفظ التحضير.")
                st.rerun()

    st.subheader("📋 السجل")
    if att_df.empty:
        st.info("لا توجد سجلات.")
    else:
        st.dataframe(att_df, use_container_width=True)


# =========================
# شاشة الحفظ — قوائم منسدلة بالكامل
# =========================
def screen_hifz():
    st.header("📖 متابعة الحفظ")

    bio_df = load_db(DB_BIO_FILE, BIO_COLUMNS)
    hifz_df = load_db(DB_HIFZ_FILE, HIFZ_COLUMNS)

    with st.form("hifz_form"):
        student = st.selectbox("الطالب", [""] + bio_df['الاسم'].dropna().tolist())
        part = st.selectbox("الجزء", parts_list)
        surah = st.text_input("السورة")  # اسم السورة لا يمكن جعله قائمة ثابتة منطقياً
        pages = st.number_input("عدد الصفحات", 1, 20)
        eval_val = st.selectbox("التقييم", hifz_eval_list)

        if st.form_submit_button("حفظ"):
            if not student or not surah:
                st.error("أكمل البيانات.")
            else:
                new_hifz = pd.DataFrame([[student, part, surah, pages, eval_val]], columns=HIFZ_COLUMNS)
                updated = pd.concat([hifz_df, new_hifz], ignore_index=True)
                save_db(updated, DB_HIFZ_FILE, HIFZ_COLUMNS)
                st.success("تم حفظ الحفظ.")
                st.rerun()

    st.subheader("📋 السجل")
    if hifz_df.empty:
        st.info("لا توجد سجلات.")
    else:
        st.dataframe(hifz_df, use_container_width=True)


# =========================
# شاشة الدرجات — قوائم منسدلة بالكامل
# =========================
def screen_grades():
    st.header("🎯 رصد الدرجات")

    bio_df = load_db(DB_BIO_FILE, BIO_COLUMNS)
    grades_df = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

    with st.form("grade_form"):
        student = st.selectbox("الطالب", [""] + bio_df['الاسم'].dropna().tolist())
        q = st.number_input("القرآن", 0, 100)
        f = st.number_input("الفقه", 0, 100)
        h = st.number_input("الحديث", 0, 100)
        s = st.number_input("السيرة", 0, 100)

        if st.form_submit_button("حفظ"):
            if not student:
                st.error("اختر الطالب.")
            else:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                grade = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_grade = pd.DataFrame([[student, q, f, h, s, round(avg, 2), grade]], columns=GRADES_COLUMNS)
                updated = pd.concat([grades_df[grades_df['الاسم'] != student], new_grade], ignore_index=True)
                save_db(updated, DB_GRADES_FILE, GRADES_COLUMNS)
                st.success("تم حفظ الدرجة.")
                st.rerun()

    st.subheader("📋 السجل")
    if grades_df.empty:
        st.info("لا توجد سجلات.")
    else:
        st.dataframe(grades_df.sort_values("المعدل", ascending=False), use_container_width=True)


# =========================
# شاشة السجل العام + تصفير النظام بالكامل
# =========================
def screen_log():
    st.header("📋 السجل العام")

    bio_df = load_db(DB_BIO_FILE, BIO_COLUMNS)
    att_df = load_db(DB_ATT_FILE, ATT_COLUMNS)
    hifz_df = load_db(DB_HIFZ_FILE, HIFZ_COLUMNS)
    grades_df = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 الطلاب", "✅ التحضير", "📖 الحفظ", "🎯 الدرجات", "🧹 تصفير النظام"]
    )

    with tab1:
        st.subheader("📁 بيانات الطلاب")
        st.dataframe(bio_df, use_container_width=True)

    with tab2:
        st.subheader("✅ سجلات التحضير")
        st.dataframe(att_df, use_container_width=True)

    with tab3:
        st.subheader("📖 سجلات الحفظ")
        st.dataframe(hifz_df, use_container_width=True)

    with tab4:
        st.subheader("🎯 سجلات الدرجات")
        st.dataframe(grades_df, use_container_width=True)

    with tab5:
        st.subheader("🧹 تصفير النظام بالكامل")
        st.warning("تنبيه: هذه العملية ستمسح جميع البيانات نهائياً.")
        if st.button("تصفير كل قواعد البيانات"):
            reset_all_dbs()
            st.success("✅ تم تصفير النظام بالكامل. لا توجد الآن أي بيانات سابقة.")
            st.rerun()


# =========================
# القائمة الجانبية
# =========================
menu = st.sidebar.radio(
    "القائمة الرئيسية",
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


