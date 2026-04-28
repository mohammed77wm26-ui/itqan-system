import streamlit as st
import pandas as pd
import os

# ==============================
# إعداد الصفحة
# ==============================
st.set_page_config(page_title="منظومة إتقان", layout="wide")

# ==============================
# دوال مساعدة (حل جذري للأعمدة)
# ==============================
def ensure_columns(df, required_cols):
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    return df[required_cols]

def load_data(file, cols):
    if not os.path.exists(file):
        df = pd.DataFrame(columns=cols)
        df.to_csv(file, index=False)
        return df
    df = pd.read_csv(file, dtype=str)
    df = ensure_columns(df, cols)
    return df

def save_data(df, file):
    df.to_csv(file, index=False)

# ==============================
# تسجيل الدخول
# ==============================
USERS = {"ASSAF": "7734", "admin": "admin123"}

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if USERS.get(u.upper()) == p:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("بيانات خاطئة")
    st.stop()

# ==============================
# تحميل البيانات (متوافق 100%)
# ==============================
BIO = load_data('db_bio.csv', ['ID', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = load_data('db_att.csv', ['التاريخ', 'ID', 'الحالة'])
GRADES = load_data('db_grades.csv', ['ID', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل'])

# ==============================
# إصلاح البيانات القديمة تلقائيًا
# ==============================
if BIO['ID'].eq("").any():
    BIO['ID'] = [str(i+1) for i in range(len(BIO))]
    save_data(BIO, 'db_bio.csv')

# ==============================
# القائمة
# ==============================
menu = st.sidebar.selectbox("القائمة", [
    "🏠 الطلاب",
    "✅ الحضور",
    "🎯 الدرجات",
    "📊 الإحصائيات"
])

# ==============================
# 1. الطلاب
# ==============================
if menu == "🏠 الطلاب":
    st.title("👨‍🎓 إدارة الطلاب")

    with st.form("add_student"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("الاسم")
            age = st.number_input("العمر", 5, 60)

        with col2:
            student_id = st.text_input("ID")
            grade = st.text_input("الصف")

        if st.form_submit_button("➕ إضافة"):
            if name and student_id:
                if student_id in BIO['ID'].values:
                    st.warning("ID موجود مسبقًا")
                else:
                    new = pd.DataFrame([[student_id, name, age, grade, "", ""]], columns=BIO.columns)
                    BIO = pd.concat([BIO, new], ignore_index=True)
                    save_data(BIO, 'db_bio.csv')
                    st.success("تمت الإضافة")
                    st.rerun()
            else:
                st.error("أدخل الاسم و ID")

    st.dataframe(BIO, use_container_width=True)

# ==============================
# 2. الحضور
# ==============================
elif menu == "✅ الحضور":
    st.title("📅 تسجيل الحضور")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        student_map = dict(zip(BIO['ID'], BIO['الاسم']))
        sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])

        status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])

        if st.button("تسجيل"):
            new = pd.DataFrame([[pd.Timestamp.now().date(), sid, status]], columns=ATT.columns)
            ATT = pd.concat([ATT, new], ignore_index=True)
            save_data(ATT, 'db_att.csv')
            st.success("تم تسجيل الحضور")

# ==============================
# 3. الدرجات
# ==============================
elif menu == "🎯 الدرجات":
    st.title("📊 إدخال الدرجات")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        student_map = dict(zip(BIO['ID'], BIO['الاسم']))
        sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])

        q = st.slider("القرآن", 0, 100)
        f = st.slider("الفقه", 0, 100)
        h = st.slider("الحديث", 0, 100)
        s = st.slider("السيرة", 0, 100)

        if st.button("حساب"):
            avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)

            st.metric("المعدل", f"{round(avg,2)}%")

            new = pd.DataFrame([[sid, q, f, h, s, avg]], columns=GRADES.columns)
            GRADES = pd.concat([GRADES[GRADES['ID'] != sid], new], ignore_index=True)
            save_data(GRADES, 'db_grades.csv')

# ==============================
# 4. الإحصائيات
# ==============================
elif menu == "📊 الإحصائيات":
    st.title("📈 لوحة التحكم")

    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الطلاب", len(BIO))
    col2.metric("سجلات الحضور", len(ATT))
    col3.metric("الدرجات", len(GRADES))

    if not GRADES.empty and "المعدل" in GRADES.columns:
        chart_df = GRADES.copy()
        chart_df["المعدل"] = pd.to_numeric(chart_df["المعدل"], errors='coerce')
        chart_df = chart_df.dropna()

        if not chart_df.empty:
            st.bar_chart(chart_df.set_index("ID")["المعدل"])
        else:
            st.info("لا توجد بيانات صالحة للرسم")
