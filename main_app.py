import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. الإعدادات وتأمين البيانات
# ==========================================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

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
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    return pd.read_csv(config["file"], encoding="utf-8-sig").reindex(columns=config["cols"]).fillna("")

def save_data(df, key):
    df.to_csv(DB_CONFIG[key]["file"], index=False, encoding="utf-8-sig")

# ==========================================
# 2. نظام الدخول
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول منظومة إتقان</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("المستخدم").strip()
        p = st.text_input("المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات خاطئة")
    st.stop()

# ==========================================
# 3. القوائم المنسدلة
# ==========================================
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 61)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 1000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- الشاشة 1: إدارة الطلاب (كاملة الحقول) ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = load_data("bio")
    
    # الـ ID التلقائي
    if not df_bio.empty:
        try:
            nums = [int(str(x).replace('ID-', '')) for x in df_bio['الرقم'] if 'ID-' in str(x)]
            next_id = f"ID-{max(nums) + 1}" if nums else "ID-100"
        except: next_id = "ID-100"
    else: next_id = "ID-100"

    action = st.radio("الإجراء:", ["إضافة طالب جديد", "تعديل / حذف طالب"], horizontal=True)

    if action == "تعديل / حذف طالب":
        target = st.selectbox("اختر الطالب لتعديل بياناته:", [""] + df_bio['الاسم'].tolist())
        if target:
            row = df_bio[df_bio['الاسم'] == target].iloc[0]
            with st.form("edit_student_form"):
                u_name = st.text_input("الاسم الثلاثي", value=row['الاسم'])
                u_id = st.text_input("الرقم التسلسلي", value=row['الرقم'], disabled=True)
                c1, c2 = st.columns(2)
                u_age = c1.selectbox("العمر", ages, index=ages.index(str(row['العمر'])) if str(row['العمر']) in ages else 0)
                u_grade = c1.selectbox("الصف الدراسي", stages, index=stages.index(row['الصف']) if row['الصف'] in stages else 0)
                u_phone = c2.selectbox("رقم الهاتف", phones, index=phones.index(row['الهاتف']) if row['الهاتف'] in phones else 0)
                u_email = c2.selectbox("البريد الإلكتروني", emails, index=emails.index(row['الإيميل']) if row['الإيميل'] in emails else 0)
                
                b1, b2 = st.columns(2)
                if b1.form_submit_button("💾 حفظ التعديلات", use_container_width=True):
                    df_bio = df_bio[df_bio['الاسم'] != target]
                    new_r = pd.DataFrame([[u_name, u_id, u_age, u_grade, u_phone, u_email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_r], ignore_index=True), "bio")
                    st.success("تم التحديث")
                    st.rerun()
                if b2.form_submit_button("🗑️ حذف الطالب", use_container_width=True):
                    save_data(df_bio[df_bio['الاسم'] != target], "bio")
                    st.warning("تم الحذف")
                    st.rerun()
    else:
        with st.form("add_student_form", clear_on_submit=True):
            st.info(f"المعرف التلقائي القادم: {next_id}")
            n_name = st.text_input("الاسم الثلاثي الجديد")
            c1, c2 = st.columns(2)
            n_age = c1.selectbox("العمر", ages)
            n_grade = c1.selectbox("الصف الدراسي", stages)
            n_phone = c2.selectbox("رقم الهاتف", phones)
            n_email = c2.selectbox("البريد الإلكتروني", emails)
            if st.form_submit_button("✅ إضافة الطالب"):
                if n_name:
                    new_s = pd.DataFrame([[n_name, next_id, n_age, n_grade, n_phone, n_email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_s], ignore_index=True), "bio")
                    st.success("تمت الإضافة")
                    st.rerun()

# --- الشاشة 2: متابعة الحفظ (المثالية) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio = load_data("bio")
    hifz = load_data("hifz")
    with st.form("hifz_pro_form", clear_on_submit=True):
        st_name = st.selectbox("اسم الطالب", [""] + bio['الاسم'].tolist())
        c1, c2, c3 = st.columns([2, 2, 1])
        part = c1.selectbox("الجزء", [str(i) for i in range(1, 31)])
        surah = c1.selectbox("السورة", quran_surahs)
        pages = c2.number_input("عدد الصفحات", 1, 100, 1)
        errors = c3.number_input("الأخطاء", 0, 50, 0)
        
        if st.form_submit_button("💾 حفظ سجل الحفظ"):
            if st_name:
                if errors == 0: ev = "ممتاز"
                elif errors <= 2: ev = "جيد جداً"
                elif errors <= 4: ev = "جيد"
                else: ev = "يحتاج متابعة"
                new_h = pd.DataFrame([[st_name, part, surah, pages, errors, ev]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz, new_h], ignore_index=True), "hifz")
                st.success(f"التقييم: {ev}")

# --- الشاشة 3: التحضير ورصد الدرجات والسجل (مدمجة ومستقرة) ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ التحضير")
    bio = load_data("bio")
    att = load_data("att")
    with st.form("att_form", clear_on_submit=True):
        s = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        h = st.selectbox("الحالة", ["حاضر", "غائب", "متأخر", "معتذر"])
        if st.form_submit_button("حفظ"):
            new = pd.DataFrame([[datetime.today().strftime('%Y-%m-%d'), s, h]], columns=DB_CONFIG["att"]["cols"])
            save_data(pd.concat([att, new], ignore_index=True), "att")
            st.success("تم")

elif menu == "🎯 رصد الدرجات":
    st.header("🎯 الدرجات")
    bio = load_data("bio")
    gr = load_data("grades")
    with st.form("gr_form", clear_on_submit=True):
        s = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q, f = c1.number_input("قرآن", 0, 100), c1.number_input("فقه", 0, 100)
        h, si = c2.number_input("حديث", 0, 100), c2.number_input("سيرة", 0, 100)
        if st.form_submit_button("رصد"):
            avg = round((q*0.5) + (((f+h+si)/3)*0.5), 2)
            t = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
            new = pd.DataFrame([[s, q, f, h, si, avg, t]], columns=DB_CONFIG["grades"]["cols"])
            save_data(pd.concat([gr[gr['الاسم'] != s], new], ignore_index=True), "grades")
            st.success(f"المعدل: {avg}")

elif menu == "📋 السجل العام":
    st.header("📋 التقارير")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "الحفظ", "التحضير", "الدرجات"])
    with t1: st.dataframe(load_data("bio"), use_container_width=True)
    with t2: st.dataframe(load_data("hifz"), use_container_width=True)
    with t3: st.dataframe(load_data("att"), use_container_width=True)
    with t4: st.dataframe(load_data("grades"), use_container_width=True)
