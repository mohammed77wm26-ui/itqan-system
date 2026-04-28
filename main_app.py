import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# إعدادات النظام
# ==========================================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

DB_CONFIG = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

# قائمة سور القرآن الكريم كاملة
quran_surahs = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"
]

def load_data(key):
    config = DB_CONFIG[key]
    if not os.path.exists(config["file"]):
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    df = pd.read_csv(config["file"], encoding="utf-8-sig")
    return df.reindex(columns=config["cols"]).fillna("")

def save_data(df, key):
    df.to_csv(DB_CONFIG[key]["file"], index=False, encoding="utf-8-sig")

# ==========================================
# نظام الدخول
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول المنظومة</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ بيانات خاطئة")
    st.stop()

# ==========================================
# التنقل
# ==========================================
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. إدارة الطلاب (تعديل، حذف، ID تلقائي) ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = load_data("bio")
    
    # ID تلقائي
    if not df_bio.empty:
        try:
            ids_only = [int(str(x).replace('ID-', '')) for x in df_bio['الرقم'] if str(x).startswith('ID-')]
            next_id = f"ID-{max(ids_only) + 1}" if ids_only else "ID-100"
        except: next_id = "ID-100"
    else: next_id = "ID-100"

    action = st.radio("الإجراء:", ["إضافة جديد", "تعديل / حذف"], horizontal=True)
    
    if action == "تعديل / حذف":
        target = st.selectbox("اختر الطالب:", [""] + df_bio['الاسم'].tolist())
        if target:
            row = df_bio[df_bio['الاسم'] == target].iloc[0]
            with st.form("edit_form"):
                u_name = st.text_input("الاسم", value=row['الاسم'])
                u_id = st.text_input("الرقم", value=row['الرقم'], disabled=True)
                c1, c2 = st.columns(2)
                u_age = c1.selectbox("العمر", [str(i) for i in range(5, 60)], index=int(row['العمر'])-5 if row['العمر'] else 0)
                u_grade = c1.selectbox("الصف", ["", "ابتدائي", "متوسط", "ثانوي", "جامعي"], index=0)
                if st.form_submit_button("حفظ التعديلات"):
                    df_bio = df_bio[df_bio['الاسم'] != target]
                    new_r = pd.DataFrame([[u_name, u_id, u_age, u_grade, row['الهاتف'], row['الإيميل']]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_r], ignore_index=True), "bio")
                    st.success("تم التحديث")
                    st.rerun()
    else:
        with st.form("add_form", clear_on_submit=True):
            st.info(f"المعرف القادم: {next_id}")
            n_name = st.text_input("الاسم الثلاثي")
            if st.form_submit_button("إضافة الطالب"):
                if n_name:
                    new_s = pd.DataFrame([[n_name, next_id, "", "", "", ""]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_s], ignore_index=True), "bio")
                    st.rerun()

# --- 2. متابعة الحفظ (تمت إضافة الصفحات والسور كقائمة) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio = load_data("bio")
    hifz = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        st_name = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2, c3 = st.columns(3)
        with c1:
            part = st.selectbox("الجزء", [str(i) for i in range(1, 31)])
            surah = st.selectbox("السورة", quran_surahs)
        with c2:
            pages = st.number_input("عدد الصفحات", 1, 100, 1)
        with c3:
            errors = st.number_input("عدد الأخطاء", 0, 100, 0)
        
        if st.form_submit_button("💾 حفظ السجل"):
            if st_name:
                # التقييم الآلي
                if errors == 0: eval_res = "ممتاز"
                elif errors <= 2: eval_res = "جيد جداً"
                elif errors <= 4: eval_res = "جيد"
                else: eval_res = "يحتاج متابعة"
                
                new_h = pd.DataFrame([[st_name, part, surah, pages, errors, eval_res]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz, new_h], ignore_index=True), "hifz")
                st.success(f"تم الحفظ! التقييم: {eval_res}")
                st.rerun()

# --- 3. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير العامة")
    tabs = st.tabs(["الطلاب", "الحفظ", "الدرجات"])
    with tabs[0]: st.dataframe(load_data("bio"), use_container_width=True)
    with tabs[1]: st.dataframe(load_data("hifz"), use_container_width=True)
    with tabs[2]: st.dataframe(load_data("grades"), use_container_width=True)
