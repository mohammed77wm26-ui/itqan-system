import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="إتقان", layout="wide")

# =========================
# DB
# =========================
FILES = {
    "bio": ("db_bio.csv", ['ID','الاسم','العمر','الصف','الهاتف','الإيميل']),
    "att": ("db_att.csv", ['التاريخ','ID','الحالة']),
    "hifz": ("db_hifz.csv", ['ID','الجزء','السورة','الصفحة','التقييم']),
    "grades": ("db_grades.csv", ['ID','القرآن','الفقه','الحديث','السيرة','المعدل','التقدير'])
}

def load_db(name):
    file, cols = FILES[name]
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    df = pd.read_csv(file, dtype=str)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]

def save_db(df, name):
    file, _ = FILES[name]
    df.to_csv(file, index=False)

# =========================
# INIT SAFE STATE (الأهم)
# =========================
if "form" not in st.session_state:
    st.session_state.form = {
        "name": "",
        "sid": "",
        "age": "",
        "grade": "",
        "phone": "",
        "email": ""
    }

def reset_form():
    st.session_state.form = {
        "name": "",
        "sid": "",
        "age": "",
        "grade": "",
        "phone": "",
        "email": ""
    }

# =========================
# LOGIN
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 دخول")
    u = st.text_input("user")
    p = st.text_input("pass", type="password")

    if st.button("login"):
        if u.upper() in ["ASSAF","عساف"] and p == "7734":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("خطأ")
    st.stop()

# =========================
# LOAD DATA
# =========================
BIO = load_db("bio")
ATT = load_db("att")
GRADES = load_db("grades")
HIFZ = load_db("hifz")

student_map = dict(zip(BIO['ID'], BIO['الاسم']))

# =========================
# MENU
# =========================
menu = st.sidebar.radio("القائمة",[
    "👨‍🎓 الطلاب",
    "📅 الحضور",
    "📖 الحفظ",
    "🎯 الدرجات",
    "📋 التقرير"
])

# =========================
# 1. الطلاب (FIXED)
# =========================
if menu == "👨‍🎓 الطلاب":

    choice = st.selectbox("طالب", ["➕ جديد"] + BIO['الاسم'].tolist())

    if choice != "➕ جديد":
        row = BIO[BIO['الاسم']==choice].iloc[0]
        st.session_state.form["name"] = row['الاسم']
        st.session_state.form["sid"] = row['ID']
        st.session_state.form["age"] = row['العمر']
        st.session_state.form["grade"] = row['الصف']
        st.session_state.form["phone"] = row['الهاتف']
        st.session_state.form["email"] = row['الإيميل']
    else:
        reset_form()

    f = st.session_state.form

    with st.form("student"):
        f["name"] = st.text_input("الاسم", value=f["name"])
        f["sid"] = st.text_input("ID", value=f["sid"])
        f["age"] = st.text_input("العمر", value=f["age"])
        f["grade"] = st.text_input("الصف", value=f["grade"])
        f["phone"] = st.text_input("الهاتف", value=f["phone"])
        f["email"] = st.text_input("الإيميل", value=f["email"])

        if st.form_submit_button("حفظ"):
            BIO2 = BIO[BIO['ID'] != f["sid"]]

            new = pd.DataFrame([[
                f["sid"],f["name"],f["age"],f["grade"],f["phone"],f["email"]
            ]], columns=BIO.columns)

            save_db(pd.concat([BIO2,new],ignore_index=True),"bio")

            st.success("تم الحفظ")

            reset_form()
            st.rerun()

    if st.button("🆕 جديد"):
        reset_form()
        st.rerun()

    st.dataframe(BIO)

# =========================
# 2. الحضور
# =========================
elif menu == "📅 الحضور":
    sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])
    status = st.selectbox("الحالة", ["حاضر","غائب","بعذر"])

    if st.button("حفظ"):
        new = pd.DataFrame([[datetime.now().date(),sid,status]], columns=ATT.columns)
        save_db(pd.concat([ATT,new],ignore_index=True),"att")
        st.success("تم")

# =========================
# 3. الحفظ
# =========================
elif menu == "📖 الحفظ":
    sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])
    part = st.selectbox("الجزء", [str(i) for i in range(1,31)])
    page = st.selectbox("الصفحة", [str(i) for i in range(1,51)])
    rate = st.selectbox("التقييم", ["ممتاز","جيد","مقبول"])

    if st.button("حفظ"):
        new = pd.DataFrame([[sid,part,"",page,rate]], columns=HIFZ.columns)
        save_db(pd.concat([HIFZ,new],ignore_index=True),"hifz")
        st.success("تم")

# =========================
# 4. الدرجات
# =========================
elif menu == "🎯 الدرجات":
    sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])

    q = st.slider("القرآن",0,100)
    f = st.slider("الفقه",0,100)
    h = st.slider("الحديث",0,100)
    s = st.slider("السيرة",0,100)

    if st.button("حساب"):
        avg = (q*0.5)+(((f+h+s)/3)*0.5)
        grade = "ممتاز" if avg>=90 else "جيد جداً" if avg>=80 else "جيد" if avg>=70 else "مقبول"

        new = pd.DataFrame([[sid,q,f,h,s,avg,grade]], columns=GRADES.columns)
        save_db(pd.concat([GRADES[GRADES['ID']!=sid],new],ignore_index=True),"grades")

        st.success(f"{grade} - {avg:.2f}")

# =========================
# 5. التقرير الكامل
# =========================
elif menu == "📋 التقرير":
    st.header("تقرير شامل")

    st.dataframe(BIO, use_container_width=True)
    st.dataframe(ATT, use_container_width=True)
    st.dataframe(HIFZ, use_container_width=True)
    st.dataframe(GRADES, use_container_width=True)
