import streamlit as st
import pandas as pd
import os

# ---------------- إعدادات عامة ----------------
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# ---------------- دوال مساعدة للملفات ----------------
@st.cache_data
def load_db(file_name, columns):
    """تحميل ملف CSV مع ضمان وجود الأعمدة المطلوبة."""
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
    else:
        df = pd.read_csv(file_name, encoding="utf-8-sig")
    # ضمان وجود كل الأعمدة
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]


def save_db(df, file_name):
    """حفظ DataFrame في CSV وتحديث الكاش."""
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    load_db.clear()  # مسح الكاش لإعادة التحميل بالقيم الجديدة


# ---------------- نظام الدخول ----------------
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'username' not in st.session_state:
    st.session_state.username = ""

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول منظومة إتقان الاحترافية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() in ["ASSAF", "عساف"] and p == "7734":
                st.session_state.auth = True
                st.session_state.username = u
                st.success("تم تسجيل الدخول بنجاح ✅")
                st.rerun()
            else:
                st.error("❌ خطأ في اسم المستخدم أو كلمة المرور")
    st.stop()

# ---------------- تحميل البيانات ----------------
BIO = load_db('db_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = load_db('db_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = load_db('db_hifz.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = load_db('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

# ---------------- شريط علوي ----------------
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown("## 🌟 منظومة إتقان الاحترافية")
with top_col2:
    st.markdown(f"#### 👤 المستخدم: **{st.session_state.username}**")

st.sidebar.markdown("## 📌 القائمة الرئيسية")
menu = st.sidebar.radio(
    "",
    ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"]
)

# ---------------- قوائم ثابتة ----------------
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي",
          "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط",
          "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]

ages = [""] + [str(i) for i in range(5, 51)]
ids_list = [""] + [f"ID-{i}" for i in range(100, 500)]
phones_list = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 100)]
emails_list = ["", "student@itqan.com", "admin@itqan.com", "user@itqan.com"]


# ---------------- دالة: شاشة بيانات الطلاب ----------------
def screen_students():
    st.header("📝 إدارة بيانات الطلاب")

    names_in_db = BIO['الاسم'].dropna().tolist()
    student_list = ["➕ إضافة طالب جديد"] + names_in_db
    selected_name = st.selectbox("🎯 ابحث عن طالب أو أضف جديداً", student_list)

    # قيم افتراضية
    v_name = v_age = v_grade = v_id = v_phone = v_email = ""
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

    col_form, col_info = st.columns([2, 1])

    with col_form:
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

            submitted = st.form_submit_button(btn_label)
            if submitted:
                if not name_input:
                    st.error("الرجاء إدخال اسم الطالب.")
                elif not id_val:
                    st.error("الرجاء اختيار الرقم التسلسلي.")
                else:
                    # حذف السجل القديم إن وجد
                    clean_bio = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
                    new_entry = pd.DataFrame(
                        [[id_val, name_input, age_val, grade_val, phone_val, email_val]],
                        columns=clean_bio.columns
                    )
                    updated = pd.concat([clean_bio, new_entry], ignore_index=True)
                    save_db(updated, 'db_bio.csv')
                    st.success("✅ تم حفظ بيانات الطالب بنجاح")
                    st.experimental_rerun()

        if selected_name != "➕ إضافة طالب جديد":
            if st.button("🗑️ حذف هذا الطالب", type="primary"):
                updated = BIO[BIO['الاسم'] != selected_name]
                save_db(updated, 'db_bio.csv')
                st.warning("تم حذف الطالب.")
                st.experimental_rerun()

    # بطاقة معلومات الطالب
    with col_info:
        if selected_name != "➕ إضافة طالب جديد":
            st.markdown("### 🧾 بطاقة الطالب")
            st.markdown(f"**الاسم:** {v_name}")
            st.markdown(f"**العمر:** {v_age}")
            st.markdown(f"**الصف:** {v_grade}")
            st.markdown(f"**الرقم:** {v_id}")
            st.markdown(f"**الهاتف:** {v_phone}")
            st.markdown(f"**الإيميل:** {v_email}")
        else:
            st.info("اختر طالباً من القائمة لعرض بياناته هنا.")


# ---------------- دالة: شاشة رصد الدرجات ----------------
def screen_grades():
    st.header("🎯 رصد الدرجات")

    if BIO.empty:
        st.warning("لا توجد بيانات طلاب. الرجاء إضافة طلاب أولاً من شاشة (بيانات الطلاب).")
        return

    with st.form("grade_form"):
        student = st.selectbox("اختر الطالب", [""] + BIO['الاسم'].tolist())
        col1, col2 = st.columns(2)
        with col1:
            q = st.number_input("القرآن (50%)", 0.0, 100.0, step=1.0)
            f = st.number_input("الفقه", 0.0, 100.0, step=1.0)
        with col2:
            h = st.number_input("الحديث", 0.0, 100.0, step=1.0)
            s = st.number_input("السيرة", 0.0, 100.0, step=1.0)

        submitted = st.form_submit_button("ترحيل الدرجة")
        if submitted:
            if not student:
                st.error("الرجاء اختيار الطالب أولاً.")
            else:
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                if avg >= 90:
                    تقدير = "ممتاز"
                    color = "green"
                elif avg >= 80:
                    تقدير = "جيد جداً"
                    color = "blue"
                elif avg >= 70:
                    تقدير = "جيد"
                    color = "orange"
                else:
                    تقدير = "مقبول"
                    color = "red"

                new_grade = pd.DataFrame(
                    [[student, q, f, h, s, round(avg, 2), تقدير]],
                    columns=GRADES.columns
                )
                clean_grades = GRADES[GRADES['الاسم'] != student]
                updated = pd.concat([clean_grades, new_grade], ignore_index=True)
                save_db(updated, 'db_grades.csv')

                st.markdown(
                    f"✅ تم الترحيل! المعدل: **{round(avg, 2)}%** — "
                    f"<span style='color:{color}; font-weight:bold;'>{تقدير}</span>",
                    unsafe_allow_html=True
                )

    # عرض جدول الدرجات
    if not GRADES.empty:
        st.subheader("📊 آخر الدرجات المسجلة")
        st.dataframe(GRADES.sort_values("المعدل", ascending=False), use_container_width=True)


# ---------------- دالة: شاشة السجل العام ----------------
def screen_log():
    st.header("📋 السجل العام")
    tab1, tab2 = st.tabs(["📁 بيانات الطلاب", "📊 الدرجات"])

    with tab1:
        st.subheader("📁 جميع الطلاب")
        st.dataframe(BIO, use_container_width=True)

    with tab2:
        st.subheader("📊 جميع الدرجات")
        st.dataframe(GRADES, use_container_width=True)


# ---------------- شاشات أخرى (مكان للتطوير لاحقاً) ----------------
def screen_attendance():
    st.header("✅ التحضير اليومي")
    st.info("يمكنك لاحقاً إضافة نموذج للتحضير اليومي مع التاريخ والحالة (حاضر/غائب/متأخر).")


def screen_hifz():
    st.header("📖 متابعة الحفظ")
    st.info("يمكنك لاحقاً إضافة نموذج لتسجيل أجزاء الحفظ والتقييم اليومي أو الأسبوعي.")


# ---------------- توجيه حسب القائمة ----------------
if menu == "🏠 بيانات الطلاب":
    screen_students()
elif
