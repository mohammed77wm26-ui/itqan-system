import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الأداء الفائق (Ultra-Fast Performance)
# ==========================================
st.set_page_config(page_title="منظومة إتقان - النسخة المستقرة", layout="wide", page_icon="⚡")

# تعريف قواعد البيانات
DB_FILES = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

# وظيفة ذكية لتحميل البيانات وتخزينها في الذاكرة (Session State) لمنع الثقل
def initialize_system():
    for key, config in DB_FILES.items():
        if key not in st.session_state:
            if os.path.exists(config["file"]):
                st.session_state[key] = pd.read_csv(config["file"], encoding="utf-8-sig").fillna("")
            else:
                st.session_state[key] = pd.DataFrame(columns=config["cols"])

def sync_to_disk(key):
    """مزامنة فورية وتلقائية من الذاكرة إلى الملف لضمان الحفظ"""
    st.session_state[key].to_csv(DB_FILES[key]["file"], index=False, encoding="utf-8-sig")

# تشغيل النظام
initialize_system()

# قائمة السور
quran_surahs = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]

# ==========================================
# 2. نظام الدخول
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 نظام إتقان الذكي</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول آمن", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# ==========================================
# 3. لوحة التنقل الفوري
# ==========================================
st.sidebar.title("🚀 التحكم السريع")
menu = st.sidebar.selectbox("القائمة:", ["🏠 الطلاب", "📖 الحفظ", "📋 السجل العام"])

# زر لحفظ يدوي إضافي للاطمئنان فقط
if st.sidebar.button("💾 تأكيد حفظ كافة البيانات"):
    for k in DB_FILES.keys(): sync_to_disk(k)
    st.sidebar.success("تم تأمين كافة البيانات")

# ==========================================
# 4. الشاشات المحسنة
# ==========================================

if menu == "🏠 الطلاب":
    st.header("👤 إدارة الطلاب")
    df_bio = st.session_state.bio
    
    tab1, tab2 = st.tabs(["➕ إضافة سريعة", "✏️ تعديل البيانات"])
    
    with tab1:
        with st.form("add_student", clear_on_submit=True):
            name = st.text_input("اسم الطالب")
            c1, c2 = st.columns(2)
            age = c1.selectbox("العمر", [str(i) for i in range(5, 61)])
            grade = c2.selectbox("المرحلة", ["ابتدائي", "متوسط", "ثانوي", "جامعي"])
            if st.form_submit_button("إضافة وحفظ تلقائي"):
                if name:
                    new_id = f"ID-{len(df_bio) + 101}"
                    new_entry = pd.DataFrame([[name, new_id, age, grade, "", ""]], columns=DB_FILES["bio"]["cols"])
                    st.session_state.bio = pd.concat([df_bio, new_entry], ignore_index=True)
                    sync_to_disk("bio")
                    st.success(f"تم تسجيل {name} وحفظه تلقائياً")
                    st.rerun()

    with tab2:
        if not df_bio.empty:
            target = st.selectbox("اختر الطالب لتعديله:", [""] + df_bio['الاسم'].tolist())
            if target:
                idx = df_bio[df_bio['الاسم'] == target].index[0]
                with st.form("edit_student"):
                    u_phone = st.text_input("رقم الهاتف", value=df_bio.at[idx, 'الهاتف'])
                    u_email = st.text_input("البريد", value=df_bio.at[idx, 'الإيميل'])
                    if st.form_submit_button("حفظ التغييرات"):
                        st.session_state.bio.at[idx, 'الهاتف'] = u_phone
                        st.session_state.bio.at[idx, 'الإيميل'] = u_email
                        sync_to_disk("bio")
                        st.success("تم الحفظ")

elif menu == "📖 الحفظ":
    st.header("📖 التسميع اليومي")
    df_hifz = st.session_state.hifz
    df_bio = st.session_state.bio
    
    if df_bio.empty:
        st.warning("يجب إضافة طلاب أولاً من شاشة الطلاب.")
    else:
        with st.container(border=True):
            student = st.selectbox("اسم الطالب", [""] + df_bio['الاسم'].tolist())
            c1, c2, c3 = st.columns([2, 1, 1])
            surah = c1.selectbox("السورة", quran_surahs)
            part = c2.selectbox("الجزء", [str(i) for i in range(1, 31)])
            errors = c3.number_input("الأخطاء", 0, 50, 0)
            
            if st.button("💾 تسجيل التسميع والحفظ", use_container_width=True):
                if student:
                    eval_v = "ممتاز" if errors == 0 else "جيد جداً" if errors <= 2 else "جيد"
                    new_h = pd.DataFrame([[student, part, surah, 1, errors, eval_v]], columns=DB_FILES["hifz"]["cols"])
                    st.session_state.hifz = pd.concat([df_hifz, new_h], ignore_index=True)
                    sync_to_disk("hifz")
                    st.success(f"تم الحفظ التلقائي للتقييم: {eval_v}")
                else: st.error("اختر الطالب")

elif menu == "📋 السجل العام":
    st.header("📋 معاينة البيانات")
    sub_tab1, sub_tab2 = st.tabs(["سجل الطلاب", "سجل الحفظ"])
    with sub_tab1:
        st.dataframe(st.session_state.bio, use_container_width=True)
    with sub_tab2:
        st.dataframe(st.session_state.hifz, use_container_width=True)

# ميزة التحميل للإكسل (منظم وفوري)
st.sidebar.markdown("---")
if st.sidebar.download_button("📥 تحميل كشف Excel (منظم)", 
                             st.session_state[menu_key := "hifz" if menu=="📖 الحفظ" else "bio"].to_csv(index=False, sep=';', encoding="utf-8-sig").encode('utf-8-sig'),
                             f"itqan_export_{datetime.now().strftime('%H%M')}.csv", "text/csv"):
    st.sidebar.success("تم التحميل")
