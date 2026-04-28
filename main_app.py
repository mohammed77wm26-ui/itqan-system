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
                st.success("✅ تم تسجيل الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ خطأ في اسم المستخدم أو كلمة المرور")
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
    st.markdown("#### نظام متكامل لإدارة بيانات الطلاب والتحضير والحفظ والدرجات")
with top_col2:
    st.markdown(f"#### 👤 المستخدم: **{st.session_state.username}**")
    if st.button("تسجيل خروج"):
        st.session_state.auth = False
        st.session_state.username = ""
        st.rerun()

# =========================
# قوائم ثابتة
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
# شاشة بيانات الطلاب
# =========================
def screen_students():
    st.header("📝 إدارة بيانات الطلاب")

    names_in_db = BIO['الاسم'].dropna().tolist()
    student_list = ["➕ إضافة طالب جديد"] + names_in_db

    # استخدام session_state لتسريع التنقل وتفريغ الحقول بعد الحفظ
    if 'student_selector' not in st.session_state:
        st.session_state.student_selector = "➕ إضافة طالب جديد"

    selected_name = st.selectbox(
        "🎯 ابحث عن طالب أو أضف جديداً",
        student_list,
        key="student_selector"
    )

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
                    st.error("⚠️ الرجاء إدخال اسم الطالب.")
                elif not id_val:
                    st.error("⚠️ الرجاء اختيار الرقم التسلسلي.")
                else:
                    clean_bio = BIO[BIO['الاسم'] != selected_name] if selected_name != "➕ إضافة طالب جديد" else BIO
                    new_entry = pd.DataFrame(
                        [[id_val, name_input, age_val, grade_val, phone_val, email_val]],
                        columns=clean_bio.columns
                    )
                    updated = pd.concat([clean_bio, new_entry], ignore_index=True)
                    save_db(updated, DB_BIO_FILE)

                    # تفريغ الحقول مباشرة بعد الحفظ
                    st.session_state.student_selector = "➕ إضافة طالب جديد"
                    st.success("✅ تم حفظ بيانات الطالب بنجاح")
                    st.rerun()

        # حذف متتالي: الطالب + كل متعلقاته
        if selected_name != "➕ إضافة طالب جديد":
            if st.button("🗑️ حذف هذا الطالب وجميع سجلاته", type="primary"):
                # حذف من BIO
                updated_bio = BIO[BIO['الاسم'] != selected_name]
                save_db(updated_bio, DB_BIO_FILE)

                # حذف من ATT, HIFZ, GRADES
                updated_att = ATT[ATT['الاسم'] != selected_name]
                updated_hifz = HIFZ[HIFZ['الاسم'] != selected_name]
                updated_grades = GRADES[GRADES['الاسم'] != selected_name]

                save_db(updated_att, DB_ATT_FILE)
                save_db(updated_hifz, DB_HIFZ_FILE)
                save_db(updated_grades, DB_GRADES_FILE)

                st.session_state.student_selector = "➕ إضافة طالب جديد"
                st.warning("🚮 تم حذف الطالب وجميع سجلاته المرتبطة.")
                st.rerun()

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


# =========================
# شاشة التحضير اليومي
# =========================
def screen_attendance():
    st.header("✅ التحضير اليومي")

    if BIO.empty:
        st.warning("لا توجد بيانات طلاب. الرجاء إضافة طلاب أولاً من شاشة (بيانات الطلاب).")
        return

    col_form, col_table = st.columns([1.2, 2])

    with col_form:
        st.subheader("🗓️ تسجيل حضور جديد")
        with st.form("att_form"):
            today = datetime.today().date()
            date_val = st.date_input("التاريخ", value=today)
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            status = st.selectbox("الحالة", attendance_status)

            submitted = st.form_submit_button("💾 حفظ التحضير")
            if submitted:
                if not student:
                    st.error("⚠️ الرجاء اختيار الطالب.")
                else:
                    new_att = pd.DataFrame(
                        [[date_val.strftime("%Y-%m-%d"), student, status]],
                        columns=ATT_COLUMNS
                    )
                    updated = pd.concat([ATT, new_att], ignore_index=True)
                    save_db(updated, DB_ATT_FILE)
                    st.success("✅ تم تسجيل التحضير بنجاح")
                    st.rerun()

        st.subheader("🗑️ إدارة الحذف")
        # حذف سجلات طالب معين
        del_student = st.selectbox("حذف جميع سجلات التحضير لطالب", [""] + BIO['الاسم'].tolist(), key="att_del_student")
        if del_student and st.button("حذف سجلات التحضير لهذا الطالب"):
            updated = ATT[ATT['الاسم'] != del_student]
            save_db(updated, DB_ATT_FILE)
            st.warning(f"🚮 تم حذف جميع سجلات التحضير للطالب: {del_student}")
            st.rerun()

    with col_table:
        st.subheader("📋 سجل التحضير")
        if ATT.empty:
            st.info("لا توجد سجلات تحضير بعد.")
        else:
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                filter_student = st.selectbox("تصفية حسب الطالب", ["الكل"] + BIO['الاسم'].tolist(), key="att_filter_student")
            with f_col2:
                filter_status = st.selectbox("تصفية حسب الحالة", ["الكل"] + attendance_status, key="att_filter_status")

            df_view = ATT.copy()
            if filter_student != "الكل":
                df_view = df_view[df_view['الاسم'] == filter_student]
            if filter_status != "الكل":
                df_view = df_view[df_view['الحالة'] == filter_status]

            df_view = df_view.sort_values("التاريخ", ascending=False)
            st.dataframe(df_view, use_container_width=True)


# =========================
# شاشة متابعة الحفظ
# =========================
def screen_hifz():
    st.header("📖 متابعة الحفظ")

    if BIO.empty:
        st.warning("لا توجد بيانات طلاب. الرجاء إضافة طلاب أولاً من شاشة (بيانات الطلاب).")
        return

    col_form, col_table = st.columns([1.2, 2])

    with col_form:
        st.subheader("📝 تسجيل حفظ جديد")
        with st.form("hifz_form"):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            part = st.text_input("الجزء (مثال: 1، 2، 30)")
            surah = st.text_input("السورة")
            pages = st.number_input("عدد الصفحات", min_value=1, max_value=20, step=1)
            eval_val = st.selectbox("التقييم", hifz_eval_list)

            submitted = st.form_submit_button("💾 حفظ الحفظ")
            if submitted:
                if not student:
                    st.error("⚠️ الرجاء اختيار الطالب.")
                elif not part or not surah:
                    st.error("⚠️ الرجاء إدخال الجزء والسورة.")
                else:
                    new_hifz = pd.DataFrame(
                        [[student, part, surah, pages, eval_val]],
                        columns=HIFZ_COLUMNS
                    )
                    updated = pd.concat([HIFZ, new_hifz], ignore_index=True)
                    save_db(updated, DB_HIFZ_FILE)
                    st.success("✅ تم تسجيل الحفظ بنجاح")
                    st.rerun()

        st.subheader("🗑️ إدارة الحذف")
        del_student = st.selectbox("حذف جميع سجلات الحفظ لطالب", [""] + BIO['الاسم'].tolist(), key="hifz_del_student")
        if del_student and st.button("حذف سجلات الحفظ لهذا الطالب"):
            updated = HIFZ[HIFZ['الاسم'] != del_student]
            save_db(updated, DB_HIFZ_FILE)
            st.warning(f"🚮 تم حذف جميع سجلات الحفظ للطالب: {del_student}")
            st.rerun()

    with col_table:
        st.subheader("📊 سجل الحفظ")
        if HIFZ.empty:
            st.info("لا توجد سجلات حفظ بعد.")
        else:
            filter_student = st.selectbox("تصفية حسب الطالب", ["الكل"] + BIO['الاسم'].tolist(), key="hifz_filter_student")
            df_view = HIFZ.copy()
            if filter_student != "الكل":
                df_view = df_view[df_view['الاسم'] == filter_student]
            st.dataframe(df_view, use_container_width=True)


# =========================
# شاشة رصد الدرجات
# =========================
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

        submitted = st.form_submit_button("💾 ترحيل الدرجة")
        if submitted:
            if not student:
                st.error("⚠️ الرجاء اختيار الطالب أولاً.")
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
                    columns=GRADES_COLUMNS
                )
                clean_grades = GRADES[GRADES['الاسم'] != student]
                updated = pd.concat([clean_grades, new_grade], ignore_index=True)
                save_db(updated, DB_GRADES_FILE)

                st.markdown(
                    f"✅ تم الترحيل! المعدل: **{round(avg, 2)}%** — "
                    f"<span style='color:{color}; font-weight:bold;'>{تقدير}</span>",
                    unsafe_allow_html=True
                )

    st.subheader("🗑️ إدارة الحذف")
    del_student = st.selectbox("حذف جميع الدرجات لطالب", [""] + BIO['الاسم'].tolist(), key="grades_del_student")
    if del_student and st.button("حذف الدرجات لهذا الطالب"):
        updated = GRADES[GRADES['الاسم'] != del_student]
        save_db(updated, DB_GRADES_FILE)
        st.warning(f"🚮 تم حذف جميع الدرجات للطالب: {del_student}")
        st.rerun()

    if not GRADES.empty:
        st.subheader("📊 آخر الدرجات المسجلة")
        st.dataframe(GRADES.sort_values("المعدل", ascending=False), use_container_width=True)


# =========================
# شاشة السجل العام + تنظيف شامل
# =========================
def screen_log():
    st.header("📋 السجل العام")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 الطلاب", "📊 الدرجات", "✅ التحضير", "📖 الحفظ", "🧹 تنظيف شامل"]
    )

    with tab1:
        st.subheader("📁 جميع الطلاب")
        st.dataframe(BIO, use_container_width=True)

    with tab2:
        st.subheader("📊 جميع الدرجات")
        st.dataframe(GRADES, use_container_width=True)

    with tab3:
        st.subheader("✅ جميع سجلات التحضير")
        st.dataframe(ATT, use_container_width=True)

    with tab4:
        st.subheader("📖 جميع سجلات الحفظ")
        st.dataframe(HIFZ, use_container_width=True)

    with tab5:
        st.subheader("🧹 تنظيف قواعد البيانات")
        st.info("تنبيه: هذه العمليات لا يمكن التراجع عنها.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🧨 حذف جميع بيانات الطلاب وكل المتعلقات"):
                empty = pd.DataFrame(columns=BIO_COLUMNS)
                save_db(empty, DB_BIO_FILE)
                save_db(pd.DataFrame(columns=ATT_COLUMNS), DB_ATT_FILE)
                save_db(pd.DataFrame(columns=HIFZ_COLUMNS), DB_HIFZ_FILE)
                save_db(pd.DataFrame(columns=GRADES_COLUMNS), DB_GRADES_FILE)
                st.warning("🚮 تم حذف جميع البيانات بالكامل.")
                st.rerun()
        with c2:
            if st.button("🧹 حذف جميع سجلات التحضير والحفظ والدرجات فقط"):
                save_db(pd.DataFrame(columns=ATT_COLUMNS), DB_ATT_FILE)
                save_db(pd.DataFrame(columns=HIFZ_COLUMNS), DB_HIFZ_FILE)
                save_db(pd.DataFrame(columns=GRADES_COLUMNS), DB_GRADES_FILE)
                st.warning("🚮 تم تنظيف سجلات التحضير والحفظ والدرجات.")
                st.rerun()


# =========================
# القائمة الجانبية
# =========================
st.sidebar.markdown("## 📌 القائمة الرئيسية")
menu = st.sidebar.radio(
    "",
    ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"]
)

# =========================
# توجيه الشاشات
# =========================
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


