import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px # لإضافة رسوم بيانية تجذب المشتري

# =========================
# إعدادات عامة مطورة
# =========================
st.set_page_config(
    page_title="منظومة إتقان الاحترافية V2",
    layout="wide",
    page_icon="💎"
)

# دالة لتحميل التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1e3c72; color: white; }
    .stSelectbox, .stTextInput { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# ثوابت الملفات والأعمدة
# =========================
DB_FILES = {
    "bio": ("db_bio.csv", ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']),
    "att": ("db_att.csv", ['التاريخ', 'الاسم', 'الحالة']),
    "hifz": ("db_hifz.csv", ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم']),
    "grades": ("db_grades.csv", ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])
}

# دالة تحميل بيانات ذكية وموحدة
def load_data(key):
    file, cols = DB_FILES[key]
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False, encoding="utf-8-sig")
    return pd.read_csv(file, encoding="utf-8-sig")

def save_data(df, key):
    file, _ = DB_FILES[key]
    df.to_csv(file, index=False, encoding="utf-8-sig")

# =========================
# نظام الدخول (كما هو مع تحسين بسيط)
# =========================
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # (كود الدخول الخاص بك يوضع هنا)
    # سأختصر العرض هنا للتركيز على التطوير
    st.title("🔐 دخول المنظومة")
    u = st.text_input("المستخدم")
    p = st.text_input("الكلمة", type="password")
    if st.button("دخول"):
        if u.upper() == "ASSAF" and p == "7734":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# =========================
# شريط جانبي متطور
# =========================
menu = st.sidebar.radio("🎯 لوحة التحكم", ["📊 الرئيسية (الإحصائيات)", "🏠 بيانات الطلاب", "✅ التحضير", "📖 متابعة الحفظ", "🎯 الدرجات", "📋 التقارير والسجل"])

# =========================
# 📊 1. شاشة الإحصائيات (تطوير جديد)
# =========================
if menu == "📊 الرئيسية (الإحصائيات)":
    st.title("📊 ملخص أداء الحلقات")
    bio = load_data("bio")
    att = load_data("att")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الطلاب", len(bio))
    col2.metric("حضور اليوم", len(att[att['التاريخ'] == str(datetime.today().date())]))
    col3.metric("المعدل العام", f"{round(load_data('grades')['المعدل'].mean(), 1) if not load_data('grades').empty else 0}%")
    col4.metric("الأجزاء المنجزة", len(load_data("hifz")))

    # رسم بياني بسيط لجذب العين
    if not bio.empty:
        fig = px.pie(bio, names='الصف', title='توزيع الطلاب حسب المراحل الدراسية')
        st.plotly_chart(fig, use_container_width=True)

# =========================
# 🏠 2. تطوير شاشة البيانات (البحث السريع والتعديل)
# =========================
elif menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة الطلاب")
    bio_df = load_data("bio")
    
    # ميزة البحث السريع بالاسم أو الرقم
    search = st.text_input("🔍 ابحث عن طالب (بالاسم أو الرقم)")
    if search:
        bio_df = bio_df[bio_df['الاسم'].str.contains(search) | bio_df['الرقم'].astype(str).str.contains(search)]

    # (استخدم كود الفورم الخاص بك هنا مع ميزة التصفير التي أبدعت فيها)
    st.dataframe(bio_df, use_container_width=True)
    # إضافة زر تصدير لـ Excel
    st.download_button("📥 تحميل كشف الطلاب (Excel)", bio_df.to_csv(), "students.csv")

# =========================
# 🎯 3. تطوير رصد الدرجات (المعادلة الذكية)
# =========================
elif menu == "🎯 الدرجات":
    st.header("🎯 رصد الدرجات")
    bio = load_data("bio")
    grades = load_data("grades")
    
    with st.form("grade_form"):
        student = st.selectbox("الطالب", bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q = c1.number_input("درجة القرآن (50%)", 0, 100)
        f = c1.number_input("الفقه", 0, 100)
        h = c2.number_input("الحديث", 0, 100)
        s = c2.number_input("السيرة", 0, 100)
        
        if st.form_submit_button("إصدار النتيجة النهائية"):
            # معادلتك الذهبية
            avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
             تقدير = "امتياز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
            
            new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=DB_FILES["grades"][1])
            updated = pd.concat([grades[grades['الاسم'] != student], new_g])
            save_data(updated, "grades")
            st.success(f"تم اعتماد درجة {student} بمعدل {round(avg,2)}% ({تقدير})")

# =========================
# 📋 4. شاشة التقارير (أهم ميزة للبيع)
# =========================
elif menu == "📋 التقارير والسجل":
    st.header("📋 نظام التقارير الموحد")
    bio = load_data("bio")
    
    report_type = st.radio("نوع التقرير", ["سجل شامل", "تقرير طالب محدد"])
    
    if report_type == "سجل شامل":
        st.dataframe(load_data("grades"), use_container_width=True)
    else:
        target = st.selectbox("اختر الطالب لإصدار تقريره", bio['الاسم'].tolist())
        if target:
            # تجميع بيانات الطالب من كل الملفات
            st.subheader(f"📄 تقرير أداء: {target}")
            g = load_data("grades")
            student_grade = g[g['الاسم'] == target]
            if not student_grade.empty:
                st.write(student_grade)
            else:
                st.warning("لا توجد درجات مرصودة لهذا الطالب.")
