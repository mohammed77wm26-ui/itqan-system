import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =============================
# إعداد الصفحة
# =============================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

# =============================
# الملفات + الأعمدة
# =============================
FILES = {
    "bio": ("db_bio.csv", ['ID','الاسم','العمر','الصف','الهاتف','الإيميل']),
    "att": ("db_att.csv", ['التاريخ','ID','الحالة']),
    "hifz": ("db_hifz.csv", ['ID','الجزء','السورة','الصفحة','التقييم']),
    "grades": ("db_grades.csv", ['ID','القرآن','الفقه','الحديث','السيرة','المعدل','التقدير'])
}

# =============================
# دوال قاعدة البيانات
# =============================
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

# =============================
# تسجيل الدخول
# =============================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 تسجيل الدخول")
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if u.upper() in ["ASSAF","عساف"] and p == "7734":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("بيانات خاطئة")
    st.stop()

# =============================
# تحميل البيانات
# =============================
BIO = load_db("bio")
ATT = load_db("att")
HIFZ = load_db("hifz")
GRADES = load_db("grades")

# إصلاح ID تلقائي
if BIO['ID'].eq("").any():
    BIO['ID'] = [f"ID-{i+1}" for i in range(len(BIO))]
    save_db(BIO,"bio")

student_map = dict(zip(BIO['ID'], BIO['الاسم']))

# =============================
# القوائم
# =============================
ages = [str(i) for i in range(5, 60)]
grades_list = ["الأول","الثاني","الثالث","الرابع","الخامس","السادس"]
phones = [f"05{str(i).zfill(8)}" for i in range(100)]
emails = ["student@itqan.com","user@itqan.com","admin@itqan.com"]
parts = [f"جزء {i}" for i in range(1,31)]
pages = [str(i) for i in range(1,51)]
status_list = ["حاضر","غائب","متأخر","بعذر"]
evals = ["ممتاز","جيد جداً","جيد","مقبول","ضعيف"]
marks = list(range(0,101))

# =============================
# القائمة الجانبية
# =============================
menu = st.sidebar.radio("القائمة",[
    "👨‍🎓 الطلاب",
    "📅 الحضور",
    "📖 الحفظ",
    "🎯 الدرجات",
    "📊 التقارير"
])

# =============================
# 1. الطلاب
# =============================
if menu == "👨‍🎓 الطلاب":
    st.header("إدارة الطلاب")

    with st.form("add_student"):
        c1,c2 = st.columns(2)

        with c1:
            name = st.text_input("الاسم")
            age = st.selectbox("العمر", [""]+ages)

        with c2:
            sid = st.text_input("ID")
            grade = st.selectbox("الصف", [""]+grades_list)

        phone = st.selectbox("الهاتف", [""]+phones)
        email = st.selectbox("الإيميل", [""]+emails)

        if st.form_submit_button("💾 حفظ"):
            if not name or not sid:
                st.error("أدخل الاسم و ID")
            else:
                BIO2 = BIO[BIO['ID']!=sid]
                new = pd.DataFrame([[sid,name,age,grade,phone,email]], columns=BIO.columns)
                save_db(pd.concat([BIO2,new],ignore_index=True),"bio")
                st.success("تم الحفظ")
                st.rerun()

    st.dataframe(BIO,use_container_width=True)

# =============================
# 2. الحضور
# =============================
elif menu == "📅 الحضور":
    st.header("الحضور")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        with st.form("att"):
            sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])
            status = st.selectbox("الحالة", status_list)

            if st.form_submit_button("حفظ"):
                new = pd.DataFrame([[datetime.now().date(),sid,status]], columns=ATT.columns)
                save_db(pd.concat([ATT,new],ignore_index=True),"att")
                st.success("تم الحفظ")
                st.rerun()

# =============================
# 3. الحفظ
# =============================
elif menu == "📖 الحفظ":
    st.header("متابعة الحفظ")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        with st.form("hifz"):
            sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])
            part = st.selectbox("الجزء", parts)
            page = st.selectbox("الصفحة", pages)
            rating = st.selectbox("التقييم", evals)

            if st.form_submit_button("حفظ"):
                new = pd.DataFrame([[sid,part,"",page,rating]], columns=HIFZ.columns)
                save_db(pd.concat([HIFZ,new],ignore_index=True),"hifz")
                st.success("تم الحفظ")
                st.rerun()

# =============================
# 4. الدرجات
# =============================
elif menu == "🎯 الدرجات":
    st.header("الدرجات")

    if BIO.empty:
        st.warning("لا يوجد طلاب")
    else:
        with st.form("grades"):
            sid = st.selectbox("الطالب", list(student_map.keys()), format_func=lambda x: student_map[x])

            q = st.selectbox("القرآن", marks)
            f = st.selectbox("الفقه", marks)
            h = st.selectbox("الحديث", marks)
            s = st.selectbox("السيرة", marks)

            if st.form_submit_button("حساب"):
                avg = (q*0.5)+(((f+h+s)/3)*0.5)
                grade = "ممتاز" if avg>=90 else "جيد جداً" if avg>=80 else "جيد" if avg>=70 else "مقبول"

                new = pd.DataFrame([[sid,q,f,h,s,avg,grade]], columns=GRADES.columns)
                save_db(pd.concat([GRADES[GRADES['ID']!=sid],new],ignore_index=True),"grades")

                st.metric("المعدل", round(avg,2))
                st.success(grade)

# =============================
# 5. التقارير (Dashboard)
# =============================
elif menu == "📊 التقارير":
    st.header("لوحة التحكم")

    st.metric("عدد الطلاب", len(BIO))
    st.metric("الحضور", len(ATT))
    st.metric("السجلات", len(GRADES))

    if not GRADES.empty:
        df = GRADES.copy()
        df['المعدل'] = pd.to_numeric(df['المعدل'], errors='coerce')
        df = df.dropna()

        if not df.empty:
            st.bar_chart(df.set_index("ID")["المعدل"])



