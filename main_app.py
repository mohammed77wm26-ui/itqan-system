import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# ==========================================
# 1. الإعدادات وتأمين البيانات
# ==========================================
st.set_page_config(page_title="منظومة إتقان - نسخة الإكسيل", layout="wide", page_icon="🌟")

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

# --- دالة تصدير ملف الإكسيل ---
def to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for key in DB_CONFIG.keys():
            df = load_data(key)
            df.to_excel(writer, index=False, sheet_name=key)
    return output.getvalue()

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
# 3. القائمة الجانبية والتصدير
# ==========================================
st.sidebar.title("🛠️ لوحة التحكم")
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

st.sidebar.markdown("---")
st.sidebar.subheader("💾 النسخ الاحتياطي")
excel_data = to_excel()
st.sidebar.download_button(
    label="📥 تصدير البيانات إلى Excel",
    data=excel_data,
    file_name=f"itqan_backup_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# --- الشاشة 1: إدارة الطلاب (تعديل + حذف مترابط + ID تلقائي) ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = load_data("bio")
    
    if not df_bio.empty:
        try:
            nums = [int(str(x).replace('ID-', '')) for x in df_bio['الرقم'] if 'ID-' in str(x)]
            next_id = f"ID-{max(nums) + 1}" if nums else "ID-100"
        except: next_id = "ID-100"
    else: next_id = "ID-100"

    action = st.radio("الإجراء:", ["إضافة طالب جديد", "تعديل / حذف طالب"], horizontal=True)

    if action == "تعديل / حذف طالب":
        target = st.selectbox("اختر الطالب:", [""] + df_bio['الاسم'].tolist())
        if target:
            row = df_bio[df_bio['الاسم'] == target].iloc[0]
            with st.form("edit_form"):
                u_name = st.text_input("الاسم الثلاثي", value=row['الاسم'])
                u_id = st.text_input("الرقم التسلسلي", value=row['الرقم'], disabled=True)
                c1, c2 = st.columns(2)
                u_age = c1.selectbox("العمر", [str(i) for i in range(5, 61)], index=0)
                u_grade = c1.selectbox("الصف", ["", "ابتدائي", "متوسط", "ثانوي", "جامعي"], index=0)
                
                col_b1, col_b2 = st.columns(2)
                if col_b1.form_submit_button("💾 حفظ التعديلات"):
                    df_bio = df_bio[df_bio['الاسم'] != target]
                    new_r = pd.DataFrame([[u_name, u_id, u_age, u_grade, row['الهاتف'], row['الإيميل']]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_r], ignore_index=True), "bio")
                    st.success("تم التحديث")
                    st.rerun()

                if col_b2.form_submit_button("🗑️ حذف شامل"):
                    save_data(df_bio[df_bio['الاسم'] != target], "bio")
                    for k in ["att", "hifz", "grades"]:
                        df_t = load_data(k)
                        save_data(df_t[df_t['الاسم'] != target], k)
                    st.warning("تم الحذف من كافة السجلات")
                    st.rerun()
    else:
        with st.form("add_form", clear_on_submit=True):
            st.info(f"المعرف القادم: {next_id}")
            n_name = st.text_input("الاسم الثلاثي الجديد")
            if st.form_submit_button("✅ إضافة"):
                if n_name:
                    new_s = pd.DataFrame([[n_name, next_id, "", "", "", ""]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_s], ignore_index=True), "bio")
                    st.success("تمت الإضافة")
                    st.rerun()

# --- الشاشة 2: متابعة الحفظ (تقييم آلي + صفحات + قائمة سور) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل الحفظ")
    bio = load_data("bio")
    hifz = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        st_name = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2, c3 = st.columns([2, 1, 1])
        surah = c1.selectbox("السورة", quran_surahs)
        pages = c2.number_input("الصفحات", 1, 100, 1)
        errors = c3.number_input("الأخطاء", 0, 50, 0)
        if st.form_submit_button("💾 حفظ"):
            if st_name:
                ev = "ممتاز" if errors == 0 else "جيد جداً" if errors <= 2 else "جيد" if errors <= 4 else "يحتاج متابعة"
                new_h = pd.DataFrame([[st_name, "", surah, pages, errors, ev]], columns=DB_CONFIG["hifz"]["cols"])
                save_data(pd.concat([hifz, new_h], ignore_index=True), "hifz")
                st.success(f"التقييم: {ev}")

# --- السجل العام (لعرض البيانات) ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير المركزية")
    tabs = st.tabs(["الطلاب", "الحفظ", "التحضير", "الدرجات"])
    with tabs[0]: st.dataframe(load_data("bio"), use_container_width=True)
    with tabs[1]: st.dataframe(load_data("hifz"), use_container_width=True)
    with tabs[2]: st.dataframe(load_data("att"), use_container_width=True)
    with tabs[3]: st.dataframe(load_data("grades"), use_container_width=True)
