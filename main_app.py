import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="منظومة إتقان", layout="wide")

# =========================
# قاعدة البيانات (SQLite)
# =========================
conn = sqlite3.connect("itqan.db", check_same_thread=False)
c = conn.cursor()

# إنشاء الجداول
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT,
    age TEXT,
    grade TEXT,
    phone TEXT,
    email TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    date TEXT,
    student_id TEXT,
    status TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS grades (
    student_id TEXT PRIMARY KEY,
    quran REAL,
    fiqh REAL,
    hadith REAL,
    seera REAL,
    avg REAL,
    grade TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS hifz (
    student_id TEXT,
    part TEXT,
    surah TEXT,
    page TEXT,
    rating TEXT
)
""")

conn.commit()

# =========================
# دوال مساعدة
# =========================
def fetch(query, params=()):
    return pd.read_sql_query(query, conn, params=params)

def execute(query, params=()):
    c.execute(query, params)
    conn.commit()

# =========================
# تسجيل الدخول
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 تسجيل الدخول")
    u = st.text_input("المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if u.upper() in ["ASSAF","عساف"] and p == "7734":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("خطأ")
    st.stop()

# =========================
# القائمة
# =========================
menu = st.sidebar.radio("القائمة", [
    "👨‍🎓 الطلاب",
    "📅 الحضور",
    "📖 الحفظ",
    "🎯 الدرجات",
    "📊 التقرير الشامل"
])

# =========================
# 1. الطلاب
# =========================
if menu == "👨‍🎓 الطلاب":
    st.header("إدارة الطلاب")

    students = fetch("SELECT * FROM students")
    st.dataframe(students, use_container_width=True)

    with st.form("add_student"):
        id = st.text_input("ID")
        name = st.text_input("الاسم")
        age = st.text_input("العمر")
        grade = st.text_input("الصف")
        phone = st.text_input("الهاتف")
        email = st.text_input("الإيميل")

        if st.form_submit_button("حفظ"):
            execute("""
            INSERT OR REPLACE INTO students VALUES (?,?,?,?,?,?)
            """, (id,name,age,grade,phone,email))

            st.success("تم الحفظ")
            st.rerun()

# =========================
# 2. الحضور
# =========================
elif menu == "📅 الحضور":
    st.header("الحضور")

    students = fetch("SELECT * FROM students")
    if students.empty:
        st.warning("لا يوجد طلاب")
    else:
        sid = st.selectbox("الطالب", students["id"], format_func=lambda x: students[students["id"]==x]["name"].values[0])
        status = st.selectbox("الحالة", ["حاضر","غائب","بعذر"])

        if st.button("حفظ"):
            execute("INSERT INTO attendance VALUES (?,?,?)",
                    (str(datetime.now().date()), sid, status))
            st.success("تم")

# =========================
# 3. الحفظ
# =========================
elif menu == "📖 الحفظ":
    st.header("الحفظ")

    students = fetch("SELECT * FROM students")
    sid = st.selectbox("الطالب", students["id"], format_func=lambda x: students[students["id"]==x]["name"].values[0])

    part = st.selectbox("الجزء", [f"جزء {i}" for i in range(1,31)])
    surah = st.text_input("السورة")
    page = st.selectbox("الصفحة", [str(i) for i in range(1,51)])
    rating = st.selectbox("التقييم", ["ممتاز","جيد جداً","جيد","مقبول"])

    if st.button("حفظ"):
        execute("INSERT INTO hifz VALUES (?,?,?,?)",
                (sid, part, surah, page, rating))
        st.success("تم")

# =========================
# 4. الدرجات
# =========================
elif menu == "🎯 الدرجات":
    st.header("الدرجات")

    students = fetch("SELECT * FROM students")
    sid = st.selectbox("الطالب", students["id"], format_func=lambda x: students[students["id"]==x]["name"].values[0])

    q = st.slider("القرآن",0,100)
    f = st.slider("الفقه",0,100)
    h = st.slider("الحديث",0,100)
    s = st.slider("السيرة",0,100)

    if st.button("حساب"):
        avg = (q*0.5)+(((f+h+s)/3)*0.5)
        grade = "ممتاز" if avg>=90 else "جيد جداً" if avg>=80 else "جيد" if avg>=70 else "مقبول"

        execute("""
        INSERT OR REPLACE INTO grades VALUES (?,?,?,?,?,?,?)
        """, (sid,q,f,h,s,avg,grade))

        st.success(f"{grade} - {avg:.2f}")

# =========================
# 5. التقرير الشامل
# =========================
elif menu == "📊 التقرير الشامل":
    st.header("📊 تقرير النظام الكامل")

    st.subheader("👨‍🎓 الطلاب")
    st.dataframe(fetch("SELECT * FROM students"), use_container_width=True)

    st.subheader("📅 الحضور")
    st.dataframe(fetch("SELECT * FROM attendance"), use_container_width=True)

    st.subheader("📖 الحفظ")
    st.dataframe(fetch("SELECT * FROM hifz"), use_container_width=True)

    st.subheader("🎯 الدرجات")
    st.dataframe(fetch("SELECT * FROM grades"), use_container_width=True)
