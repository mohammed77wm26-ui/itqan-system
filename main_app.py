import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. إعدادات النظام الأساسية
# ==========================================
st.set_page_config(page_title="منظومة إتقان التعليمية", layout="wide", page_icon="🌟")

# تعريف بنية الجداول لضمان عدم اختفاء أي حقل والحفاظ على استقلال البيانات
DB_CONFIG = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

quran_surahs = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]

def load_data(key):
    config = DB_CONFIG[key]
    if not os.path.exists(config["file"]):
        # إنشاء ملف فارغ مع ترميز يدعم العربية
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    return pd.read_csv(config["file"], encoding="utf-8-sig").fillna("")

def save_data(df, key):
    # حفظ البيانات بالترميز القياسي
    df.to_csv(DB_CONFIG[key]["file"], index=False, encoding="utf-8-sig")

# ==========================================
# 2. نظام الدخول
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول منظومة إتقان</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول النظام", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# ==========================================
# 3. لوحة التحكم الجانبية والتصدير المنظم
# ==========================================
st.sidebar.title("🛠️ لوحة التحكم")
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

st.sidebar.markdown("---")
st.sidebar.subheader("💾 تصدير كشوفات الإكسل")

def get_excel_ready_data(key):
    df = load_data(key)
    # استخدام sep=';' مع utf-8-sig يحل مشكلة تداخل البيانات في ملف واحد عند فتحه بالإكسل
    csv_str = df.to_csv(index=False, sep=';', encoding="utf-8-sig")
    return csv_str.encode('utf-8-sig')

target_db = st.sidebar.selectbox("اختر الكشف:", ["bio", "hifz", "att", "grades"], 
                                format_func=lambda x: {"bio":"بيانات الطلاب","hifz":"سجل الحفظ","att":"كشف التحضير","grades":"رصد الدرجات"}[x])

st.sidebar.download_button(
    label=f"📥 تحميل كشف {target_db} المنظم",
    data=get_excel_ready_data(target_db),
    file_name=f"itqan_{target_db}_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True
)

# ==========================================
# 4. شاشات النظام
# ==========================================

# --- شاشة الطلاب ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = load_data("bio")
    
    # حساب المعرف القادم تلقائياً
    if not df_bio.empty:
        try:
            nums = [int(str(x).split('-')[1]) for x in df_bio['الرقم'] if '-' in str(x)]
            next_id = f"ID-{max(nums) + 1}" if nums else "ID-100"
        except: next_id = "ID-100"
    else: next_id = "ID-100"

    tab_action = st.radio("الإجراء:", ["إضافة طالب جديد", "تعديل أو حذف"], horizontal=True)

    if tab_action == "إضافة طالب جديد":
        with st.form("add_student_form", clear_on_submit=True):
            st.info(f"المعرف القادم: {next_id}")
            name = st.text_input("الاسم الثلاثي")
            c1, c2 = st.columns(2)
            age = c1.selectbox("العمر", [str(i) for i in range(5, 61)])
            grade = c2.selectbox("الصف الدراسي", ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"])
            c3, c4 = st.columns(2)
            phone = c3.text_input("رقم الهاتف")
            email = c4.text_input("البريد الإلكتروني")
            if st.form_submit_button("✅ حفظ بيانات الطالب"):
                if name:
                    new_row = pd.DataFrame([[name, next_id, age, grade, phone, email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_row], ignore_index=True), "bio")
                    st.success(f"تم إضافة {name} بنجاح.") ; st.rerun()

    else:
        target_name = st.selectbox("اختر الطالب للإجراء:", [""] + df_bio['الاسم'].tolist())
        if target_name:
            row = df_bio[df_bio['الاسم'] == target_name].iloc[0]
            with st.form("edit_student_form"):
                u_name = st.text_input("الاسم", value=row['الاسم'])
                u_id = st.text_input("المعرف", value=row['الرقم'], disabled=True)
                c1, c2 = st.columns(2)
                u_age = c1.selectbox("العمر", [str(i) for i in range(5, 61)], index=[str(i) for i in range(5, 61)].index(str(row['العمر'])) if str(row['العمر']) in [str(i) for i in range(5, 61)] else 0)
                u_grade = c2.selectbox("الصف", ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"], index=["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"].index(row['الصف']) if row['الصف'] in ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"] else 0)
                u_phone = st.text_input("الهاتف", value=row['الهاتف'])
                u_email = st.text_input("البريد", value=row['الإيميل'])
                
                c_btn1, c_btn2 = st.columns(2)
                if c_btn1.form_submit_button("💾 تحديث البيانات"):
                    df_bio = df_bio[df_bio['الاسم'] != target_name]
                    updated = pd.DataFrame([[u_name, u_id, u_age, u_grade, u_phone, u_email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, updated], ignore_index=True), "bio")
                    st.success("تم التحديث") ; st.rerun()
                if c_btn2.form_submit_button("🗑️ حذف نهائي"):
                    save_data(df_bio[df_bio['الاسم'] != target_name], "bio")
                    for k in ["att", "hifz", "grades"]:
                        tmp = load_data(k)
                        save_data(tmp[tmp['الاسم'] != target_name], k)
                    st.warning("تم الحذف من كافة السجلات.") ; st.rerun()

# --- شاشة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل متابعة الحفظ")
    df_students = load_data("bio")
    df_hifz = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        student = st.selectbox("الطالب", [""] + df_students['الاسم'].tolist())
        col1, col2 = st.columns(2)
        part = col1.selectbox("الجزء", [str(i) for i in range(1, 31)])
        errors = col2.number_input("عدد الأخطاء", 0, 100, 0)
        surah = st.selectbox("السورة", quran_surahs)
        pages = st.number_input("الصفحات المنجزة", 1, 604, 1)
        if st.form_submit_button("💾 رصد السجل"):
            if student:
                eval_txt = "ممتاز" if errors == 0 else "جيد جداً" if errors <= 2 else "جيد" if errors <= 5 else "يحتاج متابعة"
                new_h = pd.DataFrame([[student, part, surah, pages, errors, eval_txt]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([df_hifz, new_h], ignore_index=True), "hifz")
                st.success(f"تم الرصد. التقييم الآلي: {eval_txt}")

# --- السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير المركزية")
    tab1, tab2, tab3, tab4 = st.tabs(["بيانات الطلاب", "سجل الحفظ", "كشف التحضير", "رصد الدرجات"])
    with tab1: st.dataframe(load_data("bio"), use_container_width=True)
    with tab2: st.dataframe(load_data("hifz"), use_container_width=True)
    with tab3: st.dataframe(load_data("att"), use_container_width=True)
    with tab4: st.dataframe(load_data("grades"), use_container_width=True)
