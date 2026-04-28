import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="منظومة إتقان", layout="wide", page_icon="🌟")

# =========================
# الملفات + الأعمدة
# =========================
FILES = {
    "bio": ("db_bio.csv", ['ID','الاسم','العمر','الصف','الهاتف','الإيميل']),
    "att": ("db_att.csv", ['التاريخ','ID','الحالة']),
    "hifz": ("db_hifz.csv", ['ID','الجزء','السورة','الصفحة','التقييم']),
    "grades": ("db_grades.csv", ['ID','القرآن','الفقه','الحديث','السيرة','المعدل','التقدير'])
}

# =========================
# DB
# =========================
def load_db(name):
    file, cols = FILES[name]
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False, encoding="utf-8-sig")
    df = pd.read_csv(file, dtype=str, encoding="utf-8-sig")
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]

def save_db(df, name):
    file, _ = FILES[name]
    df.to_csv(file, index=False, encoding="utf-8-sig")

# =========================
# LOGIN
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 دخول النظام")
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
# LOAD DATA
# =========================
BIO = load_db("bio")
ATT = load_db("att")
GRADES = load_db("grades")
HIFZ = load_db("hifz")

student_map = dict(zip(BIO['ID'], BIO['الاسم']))

# =========================
# RESET FORM (المفتاح لحلك)
# =========================
def reset_student_form():
    keys = [
        "name","sid","age","grade","phone","email","selector"
    ]
    for k in keys:
        st.session_state[k] = ""

# أول مرة
for k in ["name","sid","age","grade","phone","email","selector"]:
    if k not in st.session_state:
        st.session_state[k] = ""

# =========================
# MENU
# =========================
menu = st.sidebar.radio("القائمة",[
    "👨‍🎓 الطلاب",
    "📅 الحضور",
    "📖 الحفظ",
    "🎯 الدرجات",
    "📋 التقرير الشامل"
])

# =========================
# 1. الطلاب
# =========================
if menu == "👨‍🎓 الطلاب":
    st.header("إدارة الطلاب")

    choice = st.selectbox(
        "اختر طالب أو جديد",
        ["➕ جديد"] + BIO['الاسم'].tolist(),
        key="selector"
    )

    if choice != "➕ جديد":
        row = BIO[BIO['الاسم']==choice].iloc[0]
        st.session_state.sid = row['ID']
        st.session_state.name = row['الاسم']
        st.session_state.age = row['العمر']
        st.session_state.grade = row['الصف']
        st.session_state.phone = row['الهاتف']
        st.session_state.email = row['الإيميل']
    else:
        reset_student_form()

    with st.form("student_form"):
        st.session_state.name = st.text_input("الاسم", st.session_state.name)
        st.session_state.sid = st.text_input("ID", st.session_state.sid)

        c1,c2 = st.columns(2)

        with c1:
            st.session_state.age = st.text_input("العمر", st.session_state.age)
            st.session_state.grade = st.text_input("الصف", st.session_state.grade)

        with c2:
            st.session_state.phone = st.text_input("الهاتف", st.session_state.phone)
            st.session_state.email = st.text_input("الإيميل", st.session_state.email)

        save = st.form_submit_button("💾 حفظ")

        if save:
            BIO2 = BIO[BIO['ID'] != st.session_state.sid]
            new = pd.DataFrame([[
                st.session_state.sid,
                st.session_state.name,
                st.session_state.age,
                st.session_state.grade,
                st.session_state.phone,
                st.session_state.email
            ]], columns=BIO.columns)

            save_db(pd.concat([BIO2,new],ignore_index=True),"bio")

            st.success("تم الحفظ")

            # 🔥 أهم سطر: تفريغ فوري
            reset_student_form()
            st.rerun()

    # زر جديد مستقل
    if st.button("🆕 طالب جديد"):
        reset_student_form()
        st.rerun()

    st.dataframe(BIO,use_container_width=True)

# =========================
# 2. الحضور
# =========================
elif menu == "📅 الحضور":
    st.header("الحضور")

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
    st.header("الحفظ")

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
    st.header("الدرجات")

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
# 5. التقرير الشامل (FULL DATA)
# =========================
elif menu == "📋 التقرير الشامل":
    st.header("📊 تقرير شامل للنظام")

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("الطلاب", len(BIO))
    col2.metric("الحضور", len(ATT))
    col3.metric("الحفظ", len(HIFZ))
    col4.metric("الدرجات", len(GRADES))

    st.subheader("👨‍🎓 الطلاب")
    st.dataframe(BIO, use_container_width=True)

    st.subheader("📅 الحضور")
    st.dataframe(ATT, use_container_width=True)

    st.subheader("📖 الحفظ")
    st.dataframe(HIFZ, use_container_width=True)

    st.subheader("🎯 الدرجات")
    st.dataframe(GRADES, use_container_width=True)



