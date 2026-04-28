import streamlit as st
import pandas as pd
import os

# ==============================
# إعداد الصفحة
# ==============================
st.set_page_config(page_title="منظومة إتقان", layout="wide")

# ==============================
# تحميل البيانات (مع كاش)
# ==============================
@st.cache_data
def load_data(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file, dtype=str)

def save_data(df, file):
    df.to_csv(file, index=False)
    st.cache_data.clear()

# ==============================
# نظام تسجيل الدخول (محسن)
# ==============================
USERS = {
    "ASSAF": "7734",
    "admin": "admin123"
}

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
# تحميل قواعد البيانات
# ==============================
BIO = load_data('db_bio.csv', ['ID', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = load_data('db_att.csv', ['التاريخ', 'ID', 'الحالة'])
GRADES = load_data('db_grades.csv', ['ID', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل'])

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
                    BIO = pd.concat([BIO, new])
                    save_data(BIO, 'db_bio.csv')
                    st.success("تمت الإضافة")
                    st.rerun()

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

        sid = st.selectbox("اختر الطالب", list(student_map.keys()))
        status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])

        if st.button("تسجيل"):
            new = pd.DataFrame([[pd.Timestamp.now().date(), sid, status]], columns=ATT.columns)
            ATT = pd.concat([ATT, new])
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
        sid = st.selectbox("الطالب", BIO['ID'])

        q = st.slider("القرآن", 0, 100)
        f = st.slider("الفقه", 0, 100)
        h = st.slider("الحديث", 0, 100)
        s = st.slider("السيرة", 0, 100)

        if st.button("حساب"):
            avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)

            st.metric("المعدل", f"{round(avg,2)}%")

            new = pd.DataFrame([[sid, q, f, h, s, avg]], columns=GRADES.columns)
            GRADES = pd.concat([GRADES[GRADES['ID'] != sid], new])
            save_data(GRADES, 'db_grades.csv')

# ==============================
# 4. إحصائيات
# ==============================
elif menu == "📊 الإحصائيات":
    st.title("📈 لوحة التحكم")

    col1, col2, col3 = st.columns(3)

    col1.metric("عدد الطلاب", len(BIO))
    col2.metric("عدد سجلات الحضور", len(ATT))
    col3.metric("عدد الدرجات", len(GRADES))

    if not GRADES.empty:
        st.bar_chart(GRADES.set_index("ID")["المعدل"])
