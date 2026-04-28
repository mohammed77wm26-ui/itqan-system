import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="منظومة إتقان", layout="wide", page_icon="🌟")

# =========================
# ملفات + أعمدة (موحدة)
# =========================
DB_BIO_FILE = "db_bio.csv"
DB_ATT_FILE = "db_att.csv"
DB_HIFZ_FILE = "db_hifz.csv"
DB_GRADES_FILE = "db_grades.csv"

BIO_COLUMNS = ['ID', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']
ATT_COLUMNS = ['التاريخ', 'ID', 'الحالة']
HIFZ_COLUMNS = ['ID', 'الجزء', 'السورة', 'الصفحات', 'التقييم']
GRADES_COLUMNS = ['ID', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']

# =========================
# دوال ذكية (تحل KeyError نهائيًا)
# =========================
def ensure_columns(df, cols):
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]

def load_db(file, cols):
    if not os.path.exists(file):
        df = pd.DataFrame(columns=cols)
        df.to_csv(file, index=False, encoding="utf-8-sig")
        return df

    df = pd.read_csv(file, dtype=str, encoding="utf-8-sig")
    df = ensure_columns(df, cols)
    return df

def save_db(df, file):
    df.to_csv(file, index=False, encoding="utf-8-sig")

# =========================
# تسجيل الدخول
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if u.upper() in ["ASSAF", "عساف"] and p == "7734":
            st.session_state.auth = True
            st.session_state.username = u
            st.rerun()
        else:
            st.error("بيانات خاطئة")
    st.stop()

# =========================
# تحميل البيانات
# =========================
BIO = load_db(DB_BIO_FILE, BIO_COLUMNS)
ATT = load_db(DB_ATT_FILE, ATT_COLUMNS)
GRADES = load_db(DB_GRADES_FILE, GRADES_COLUMNS)

# إصلاح تلقائي لأي بيانات قديمة
if BIO['ID'].eq("").any():
    BIO['ID'] = [f"ID-{i+1}" for i in range(len(BIO))]
    save_db(BIO, DB_BIO_FILE)

# =========================
# هيدر جميل
# =========================
st.markdown("""
<div style="padding:10px; border-radius:10px; background:linear-gradient(90deg,#1e3c72,#2a5298); color:white;">
<h2>🌟 منظومة إتقان الاحترافية</h2>
</div>
""", unsafe_allow_html=True)

# =========================
# القائمة
# =========================
menu = st.sidebar.radio("القائمة", [
    "🏠 الطلاب",
    "✅ الحضور",
    "🎯 الدرجات",
    "📊 الإحصائيات"
])

# =========================
# 1. الطلاب
# =========================
if menu == "🏠 الطلاب":
    st.header("👨‍🎓 إدارة الطلاب")

    student_names = BIO['الاسم'].tolist()
    student_choice = st.selectbox("اختر طالب", ["➕ جديد"] + student_names)

    if student_choice != "➕ جديد":
        row = BIO[BIO['الاسم'] == student_choice].iloc[0]
        v_id = row['ID']
        v_name = row['الاسم']
    else:
        v_id, v_name = "", ""

    with st.form("student_form"):
        name = st.text_input("الاسم", v_name)
        sid = st.text_input("ID", v_id)

        if st.form_submit_button("💾 حفظ"):
            if not name or not sid:
                st.error("أدخل الاسم و ID")
            else:
                BIO2 = BIO[BIO['ID'] != sid]
                new = pd.DataFrame([[sid, name, "", "", "", ""]], columns=BIO.columns)
                save_db(pd.concat([BIO2, new], ignore_index=True), DB_BIO_FILE)
                st.success("تم الحفظ")
                st.rerun()

    st.dataframe(BIO, use_container_width=True)

# =========================
# 2. الحضور
# =========================
elif menu == "✅ الحضور":
    st.header("📅 الحضور")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        student_map = dict(zip(BIO['ID'], BIO['الاسم']))
        sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])
        status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])

        if st.button("تسجيل"):
            new = pd.DataFrame([[datetime.now().date(), sid, status]], columns=ATT.columns)
            save_db(pd.concat([ATT, new], ignore_index=True), DB_ATT_FILE)
            st.success("تم الحفظ")

# =========================
# 3. الدرجات
# =========================
elif menu == "🎯 الدرجات":
    st.header("📊 الدرجات")

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
            avg = (q*0.5)+(((f+h+s)/3)*0.5)
            grade = "ممتاز" if avg>=90 else "جيد جداً" if avg>=80 else "جيد" if avg>=70 else "مقبول"

            new = pd.DataFrame([[sid,q,f,h,s,avg,grade]], columns=GRADES.columns)
            save_db(pd.concat([GRADES[GRADES['ID']!=sid], new], ignore_index=True), DB_GRADES_FILE)

            st.metric("المعدل", round(avg,2))

# =========================
# 4. الإحصائيات
# =========================
elif menu == "📊 الإحصائيات":
    st.header("📈 لوحة التحكم")

    st.metric("عدد الطلاب", len(BIO))
    st.metric("سجلات الحضور", len(ATT))
    st.metric("الدرجات", len(GRADES))

    if not GRADES.empty:
        df = GRADES.copy()
        df['المعدل'] = pd.to_numeric(df['المعدل'], errors='coerce')
        df = df.dropna()

        if not df.empty:
            st.bar_chart(df.set_index("ID")["المعدل"])



