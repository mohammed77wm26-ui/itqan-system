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


def save_db(df: pd.DataFrame, file_name: str):
    df.to_csv(file_name, index=False, encoding="utf-8-sig")


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
# شريط علوي جمالي
# =========================
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="padding:10px; border-radius:10px; background:linear-gradient(90deg,#1e3c72,#2a5298); color:white;">
        <h2>🌟 منظومة إتقان الاحترافية</h2>
        <p>نظام متكامل لإدارة بيانات الطلاب والتحضير والحفظ والدرجات</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with top_col2:
    st.markdown(f"#### 👤 المستخدم: **{st.session_state.username}**")
    if st.button("تسجيل خروج"):
        st.session_state.auth = False
        st.session_state.username = ""
        st.rerun()


# =========================
# شاشة بيانات الطلاب — تفريغ تلقائي بعد الحفظ
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

    col_form, col_info = st.columns([2, 1])

    with col_form:
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

                    for k in defaults.keys():
                        st.session_state[k] = ""
                    st.session_state.student_selector = "➕ إضافة طالب جديد"

                    st.success("✅ تم الحفظ وتم تفريغ الحقول لإضافة طالب جديد.")
                    st.rerun()

        if selected_name != "➕ إضافة طالب جديد":
            if st.button("🗑️ حذف هذا الطالب وجميع سجلاته", type="primary"):
                att_df = load_db(DB_ATT_FILE, ATT_COLUMNS)
                hifz_df = load_db(DB_HIFZ_FILE, HIFZ_COLUMNS)
                grades_df = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

                bio_df = bio_df[bio_df['الاسم'] != selected_name]
                att_df = att_df[att_df['الاسم'] != selected_name]
                hifz_df = hifz_df[hifz_df['الاسم'] != selected_name]
                grades_df = grades_df[grades_df['الاسم'] != selected_name]

                save_db(bio_df, DB_BIO_FILE)
                save_db(att_df, DB_ATT_FILE)
                save_db(hifz_df, DB_HIFZ_FILE)
                save_db(grades_df, DB_GRADES_FILE)

                st.session_state.student_selector = "➕ إضافة طالب جديد"
                st.success("🚮 تم حذف الطالب وكل متعلقاته.")
                st.rerun()

    with col_info:
        if selected_name != "➕ إضافة طالب جديد":
            st.markdown("### 🧾 بطاقة الطالب")
            st.markdown(f"**الاسم:** {st.session_state.name_input}")
            st.markdown(f"**العمر:** {st.session_state.age_val}")
            st.markdown(f"**الصف:** {st.session_state.grade_val}")
            st.markdown(f"**الرقم:** {st.session_state.id_val}")
            st.markdown(f"**الهاتف:** {st.session_state.phone_val}")
            st.markdown(f"**الإيميل:** {st.session_state.email_val}")
        else:
            st.info("اختر طالباً من القائمة لعرض بياناته هنا.")


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

        if st.form_submit_button("حفظ التحضير"):
            if not student:
                st.error("اختر الطالب.")
            else:
                new_att = pd.DataFrame([[date_val.strftime("%Y-%m-%d"), student, status]], columns=ATT_COLUMNS)
                updated = pd.concat([att_df, new_att], ignore_index=True)
                save_db(updated, DB_ATT_FILE)
                st.success("تم حفظ التحضير.")
                st.rerun()

    st.subheader("📋 سجل التحضير")



