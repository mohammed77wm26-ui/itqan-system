import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# ==========================================
# 1. إعدادات الأداء والهوية
# ==========================================
st.set_page_config(page_title="منظومة إتقان التعليمية - الإصدار الاحترافي", layout="wide", page_icon="🏆")

# تعريف قواعد البيانات الكاملة (ضمان عدم سقوط أي حقل)
DB_FILES = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "hifz": {"file": "db_hifz.csv", "cols": ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "grades": {"file": "db_grades.csv", "cols": ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

# قائمة السور الكاملة
quran_surahs = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]

# إدارة البيانات والذاكرة
def initialize_system():
    for key, config in DB_FILES.items():
        if key not in st.session_state:
            if os.path.exists(config["file"]):
                st.session_state[key] = pd.read_csv(config["file"], encoding="utf-8-sig").fillna("")
            else:
                st.session_state[key] = pd.DataFrame(columns=config["cols"])

def sync_to_disk(key):
    st.session_state[key].to_csv(DB_FILES[key]["file"], index=False, encoding="utf-8-sig")

initialize_system()

# ==========================================
# 2. نظام الدخول الصارم
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #4A90E2;'>🔐 نظام إتقان الاحترافي</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            u = st.text_input("اسم المستخدم").strip()
            p = st.text_input("كلمة المرور", type="password").strip()
            if st.button("دخول النظام", use_container_width=True):
                if u.upper() == "ASSAF" and p == "7734":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# ==========================================
# 3. لوحة التحكم الجانبية (إعادة كافة الخيارات)
# ==========================================
st.sidebar.title("🛠️ لوحة التحكم")
menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 إدارة الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# حل مشكلة تصدير الإكسل (تحويل CSV لمتوافق مع إكسل العربي)
def export_excel_ready(key):
    df = st.session_state[key]
    # استخدام الترميز utf-8-sig مع الفاصلة المنقوطة يضمن فتح الملف في إكسل كأعمدة فوراً
    return df.to_csv(index=False, sep=';', encoding="utf-8-sig").encode('utf-8-sig')

st.sidebar.markdown("---")
st.sidebar.subheader("💾 التصدير الذكي")
export_target = st.sidebar.selectbox("اختر الكشف:", list(DB_FILES.keys()), format_func=lambda x: {"bio":"بيانات الطلاب","hifz":"سجل الحفظ","att":"كشف التحضير","grades":"رصد الدرجات"}[x])
st.sidebar.download_button(
    label="📥 تحميل (Excel Ready)",
    data=export_excel_ready(export_target),
    file_name=f"itqan_{export_target}_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True
)

# ==========================================
# 4. شاشات العمل (تغطية كافة الحقول)
# ==========================================

# --- شاشة الطلاب ---
if menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة بيانات الطلاب")
    df_bio = st.session_state.bio
    
    t1, t2 = st.tabs(["➕ إضافة طالب جديد", "✏️ تعديل / حذف"])
    
    with t1:
        with st.form("add_student_full", clear_on_submit=True):
            next_id = f"ID-{len(df_bio) + 101}"
            st.info(f"المعرف القادم: {next_id}")
            name = st.text_input("الاسم الثلاثي")
            c1, c2 = st.columns(2)
            age = c1.selectbox("العمر", [str(i) for i in range(5, 61)])
            grade = c2.selectbox("الصف الدراسي", ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"])
            c3, c4 = st.columns(2)
            phone = c3.text_input("رقم الهاتف")
            email = c4.text_input("البريد الإلكتروني")
            if st.form_submit_button("✅ حفظ البيانات"):
                if name:
                    new_entry = pd.DataFrame([[name, next_id, age, grade, phone, email]], columns=DB_FILES["bio"]["cols"])
                    st.session_state.bio = pd.concat([df_bio, new_entry], ignore_index=True)
                    sync_to_disk("bio")
                    st.success("تم الحفظ بنجاح") ; st.rerun()

    with t2:
        if not df_bio.empty:
            target = st.selectbox("اختر الطالب:", [""] + df_bio['الاسم'].tolist())
            if target:
                idx = df_bio[df_bio['الاسم'] == target].index[0]
                with st.form("edit_bio"):
                    u_phone = st.text_input("الهاتف", value=df_bio.at[idx, 'الهاتف'])
                    u_email = st.text_input("الإيميل", value=df_bio.at[idx, 'الإيميل'])
                    u_grade = st.selectbox("الصف", ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"], index=0)
                    btn_col1, btn_col2 = st.columns(2)
                    if btn_col1.form_submit_button("💾 تحديث"):
                        st.session_state.bio.at[idx, 'الهاتف'] = u_phone
                        st.session_state.bio.at[idx, 'الإيميل'] = u_email
                        st.session_state.bio.at[idx, 'الصف'] = u_grade
                        sync_to_disk("bio")
                        st.success("تم التحديث") ; st.rerun()
                    if btn_col2.form_submit_button("🗑️ حذف"):
                        st.session_state.bio = df_bio.drop(idx)
                        sync_to_disk("bio")
                        st.warning("تم الحذف") ; st.rerun()

# --- شاشة التحضير (المفقودة سابقاً) ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ كشف الحضور والغياب")
    df_bio = st.session_state.bio
    if df_bio.empty:
        st.warning("يرجى إضافة طلاب أولاً")
    else:
        date_today = datetime.now().strftime("%Y-%m-%d")
        st.write(f"تحضير تاريخ: {date_today}")
        
        with st.form("att_form"):
            att_data = []
            for name in df_bio['الاسم']:
                status = st.radio(f"{name}", ["حاضر", "غائب", "مستأذن"], horizontal=True, key=name)
                att_data.append([date_today, name, status])
            
            if st.form_submit_button("💾 حفظ الكشف"):
                new_att = pd.DataFrame(att_data, columns=DB_FILES["att"]["cols"])
                st.session_state.att = pd.concat([st.session_state.att, new_att], ignore_index=True)
                sync_to_disk("att")
                st.success("تم رصد الحضور بنجاح")

# --- شاشة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 متابعة الحفظ والتسميع")
    df_bio = st.session_state.bio
    if not df_bio.empty:
        with st.form("hifz_entry", clear_on_submit=True):
            student = st.selectbox("الطالب", df_bio['الاسم'].tolist())
            c1, c2, c3 = st.columns([2, 1, 1])
            surah = c1.selectbox("السورة", quran_surahs)
            part = c2.selectbox("الجزء", [str(i) for i in range(1, 31)])
            errors = c3.number_input("الأخطاء", 0, 50, 0)
            pages = st.number_input("عدد الصفحات", 1, 100, 1)
            if st.form_submit_button("💾 تسجيل الحفظ"):
                eval_v = "ممتاز" if errors == 0 else "جيد جداً" if errors <= 2 else "جيد"
                new_h = pd.DataFrame([[student, part, surah, pages, errors, eval_v]], columns=DB_FILES["hifz"]["cols"])
                st.session_state.hifz = pd.concat([st.session_state.hifz, new_h], ignore_index=True)
                sync_to_disk("hifz")
                st.success(f"تم التسجيل بنجاح. التقييم: {eval_v}")
    else: st.warning("لا يوجد طلاب")

# --- شاشة الدرجات (المفقودة سابقاً) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد درجات الاختبارات")
    df_bio = st.session_state.bio
    if not df_bio.empty:
        with st.form("grades_form", clear_on_submit=True):
            student = st.selectbox("الطالب", df_bio['الاسم'].tolist())
            c1, c2 = st.columns(2)
            quran = c1.number_input("القرآن (من 100)", 0, 100, 0)
            fiqh = c2.number_input("الفقه (من 100)", 0, 100, 0)
            hadith = c1.number_input("الحديث (من 100)", 0, 100, 0)
            seera = c2.number_input("السيرة (من 100)", 0, 100, 0)
            if st.form_submit_button("💾 رصد الدرجات"):
                avg = (quran + fiqh + hadith + seera) / 4
                rating = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, quran, fiqh, hadith, seera, avg, rating]], columns=DB_FILES["grades"]["cols"])
                st.session_state.grades = pd.concat([st.session_state.grades, new_g], ignore_index=True)
                sync_to_disk("grades")
                st.success(f"تم الرصد. المعدل: {avg}%")

# --- السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 التقارير الشاملة")
    tabs = st.tabs(["بيانات الطلاب", "سجل الحفظ", "الحضور", "الدرجات"])
    with tabs[0]: st.dataframe(st.session_state.bio, use_container_width=True)
    with tabs[1]: st.dataframe(st.session_state.hifz, use_container_width=True)
    with tabs[2]: st.dataframe(st.session_state.att, use_container_width=True)
    with tabs[3]: st.dataframe(st.session_state.grades, use_container_width=True)
