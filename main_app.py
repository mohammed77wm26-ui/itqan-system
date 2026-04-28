import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# إعدادات النظام والهوية البصرية
# ==========================================
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide", page_icon="🌟")

# تعريف هيكل البيانات (الأعمدة) لضمان الترتيب ومنع التداخل
DB_CONFIG = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الأخطاء', 'التقييم']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

def load_data(key):
    config = DB_CONFIG[key]
    if not os.path.exists(config["file"]):
        pd.DataFrame(columns=config["cols"]).to_csv(config["file"], index=False, encoding="utf-8-sig")
    df = pd.read_csv(config["file"], encoding="utf-8-sig")
    return df.reindex(columns=config["cols"]).fillna("")

def save_data(df, key):
    df.to_csv(DB_CONFIG[key]["file"], index=False, encoding="utf-8-sig")

# ==========================================
# نظام الدخول الآمن
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول منظومة إتقان</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ بيانات الدخول غير صحيحة")
    st.stop()

# ==========================================
# القوائم والخيارات
# ==========================================
stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
ages = [""] + [str(i) for i in range(5, 51)]
phones = [""] + [f"05{str(i).zfill(8)}" for i in range(1, 2000)]
emails = ["", "student@itqan.com", "user@itqan.com", "admin@itqan.com"]

# ==========================================
# القائمة الجانبية للتنقل
# ==========================================
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. شاشة إدارة الطلاب (تعديل + حذف + ID تلقائي) ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = load_data("bio")
    
    # حساب الـ ID التلقائي
    if not df_bio.empty:
        try:
            last_id = max([int(str(x).replace('ID-', '')) for x in df_bio['الالرقم'] if str(x).startswith('ID-')])
            next_id = f"ID-{last_id + 1}"
        except: next_id = "ID-100"
    else: next_id = "ID-100"

    # اختيار الإجراء
    action = st.radio("اختر العملية:", ["إضافة طالب جديد", "تعديل / حذف طالب"], horizontal=True)
    
    if action == "تعديل / حذف طالب":
        target = st.selectbox("اختر الطالب المراد تعديله:", [""] + df_bio['الاسم'].tolist())
        if target:
            row = df_bio[df_bio['الاسم'] == target].iloc[0]
            with st.form("edit_form"):
                u_name = st.text_input("الاسم", value=row['الاسم'])
                u_id = st.text_input("الرقم (ID)", value=row['الرقم'], disabled=True)
                c1, c2 = st.columns(2)
                u_age = c1.selectbox("العمر", ages, index=ages.index(str(row['العمر'])) if str(row['العمر']) in ages else 0)
                u_grade = c1.selectbox("الصف", stages, index=stages.index(row['الصف']) if row['الصف'] in stages else 0)
                u_phone = c2.selectbox("الهاتف", phones, index=phones.index(row['الهاتف']) if row['الهاتف'] in phones else 0)
                u_email = c2.selectbox("الإيميل", emails, index=emails.index(row['الإيميل']) if row['الإيميل'] in emails else 0)
                
                col_b1, col_b2 = st.columns(2)
                if col_b1.form_submit_button("💾 حفظ التعديلات", use_container_width=True):
                    df_bio = df_bio[df_bio['الاسم'] != target]
                    new_row = pd.DataFrame([[u_name, u_id, u_age, u_grade, u_phone, u_email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_row], ignore_index=True), "bio")
                    st.success("تم تحديث البيانات")
                    st.rerun()
                
                if col_b2.form_submit_button("🗑️ حذف الطالب", use_container_width=True):
                    save_data(df_bio[df_bio['الاسم'] != target], "bio")
                    st.warning("تم حذف الطالب من النظام")
                    st.rerun()
    else:
        with st.form("add_form", clear_on_submit=True):
            st.info(f"المعرف التلقائي القادم: {next_id}")
            n_name = st.text_input("الاسم الثلاثي")
            c1, c2 = st.columns(2)
            n_age = c1.selectbox("العمر", ages)
            n_grade = c1.selectbox("الصف", stages)
            n_phone = c2.selectbox("الهاتف", phones)
            n_email = c2.selectbox("الإيميل", emails)
            if st.form_submit_button("✅ إضافة الطالب للنظام"):
                if n_name:
                    new_student = pd.DataFrame([[n_name, next_id, n_age, n_grade, n_phone, n_email]], columns=DB_CONFIG["bio"]["cols"])
                    save_data(pd.concat([df_bio, new_student], ignore_index=True), "bio")
                    st.success("تمت الإضافة بنجاح")
                    st.rerun()

# --- 2. شاشة التحضير ---
elif menu == "✅ التحضير اليومي":
    st.header("📝 سجل الحضور والغياب")
    bio = load_data("bio")
    att = load_data("att")
    with st.form("att_form", clear_on_submit=True):
        st_name = st.selectbox("اسم الطالب", [""] + bio['الاسم'].tolist())
        status = st.selectbox("الحالة", ["حاضر", "غائب", "متأخر", "معتذر"])
        if st.form_submit_button("حفظ التحضير"):
            new_att = pd.DataFrame([[datetime.today().strftime('%Y-%m-%d'), st_name, status]], columns=DB_CONFIG["att"]["cols"])
            save_data(pd.concat([att, new_att], ignore_index=True), "att")
            st.success(f"تم تحضير {st_name}")

# --- 3. شاشة الحفظ (التقييم الآلي) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة حفظ القرآن")
    bio = load_data("bio")
    hifz = load_data("hifz")
    with st.form("hifz_form", clear_on_submit=True):
        st_name = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        part = c1.selectbox("الجزء", [str(i) for i in range(1, 31)])
        surah = c1.text_input("السورة")
        errors = c2.number_input("عدد الأخطاء", 0, 50, 0)
        
        if st.form_submit_button("💾 حفظ السجل"):
            # معادلة التقييم الآلي
            if errors == 0: eval_res = "ممتاز"
            elif errors <= 2: eval_res = "جيد جداً"
            elif errors <= 4: eval_res = "جيد"
            else: eval_res = "يحتاج متابعة"
            
            new_h = pd.DataFrame([[st_name, part, surah, errors, eval_res]], columns=DB_CONFIG["hifz"]["cols"])
            save_data(pd.concat([hifz, new_h], ignore_index=True), "hifz")
            st.success(f"التقييم الآلي: {eval_res}")
            st.rerun()

# --- 4. رصد الدرجات ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات النهائية")
    bio = load_data("bio")
    gr = load_data("grades")
    with st.form("gr_form", clear_on_submit=True):
        st_name = st.selectbox("الطالب", [""] + bio['الاسم'].tolist())
        c1, c2 = st.columns(2)
        q, f = c1.number_input("القرآن", 0, 100), c1.number_input("الفقه", 0, 100)
        h, s = c2.number_input("الحديث", 0, 100), c2.number_input("السيرة", 0, 100)
        if st.form_submit_button("ترحيل الدرجة"):
            avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
            # تجنب أخطاء الإزاحة
            if avg >= 90: t = "ممتاز"
            elif avg >= 80: t = "جيد جداً"
            elif avg >= 70: t = "جيد"
            else: t = "مقبول"
            new_g = pd.DataFrame([[st_name, q, f, h, s, round(avg, 2), t]], columns=DB_CONFIG["grades"]["cols"])
            save_data(pd.concat([gr[gr['الاسم'] != st_name], new_g], ignore_index=True), "grades")
            st.success("تم الرصد بنجاح")

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 قواعد البيانات المركزية")
    tabs = st.tabs(["الطلاب", "التحضير", "الحفظ", "الدرجات"])
    with tabs[0]: st.dataframe(load_data("bio"), use_container_width=True)
    with tabs[1]: st.dataframe(load_data("att"), use_container_width=True)
    with tabs[2]: st.dataframe(load_data("hifz"), use_container_width=True)
    with tabs[3]: st.dataframe(load_data("grades"), use_container_width=True)
