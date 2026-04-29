import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# ==========================================
# 1. إعدادات الهوية والأداء المتطور
# ==========================================
st.set_page_config(page_title="منظومة إتقان التعليمية", layout="wide", page_icon="🏆")

# تعريف بنية البيانات المطورة (إضافة التاريخ والمعرفات)
DB_FILES = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "hifz": {"file": "db_hifz.csv", "cols": ['التاريخ', 'الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "grades": {"file": "db_grades.csv", "cols": ['التاريخ', 'الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

quran_surahs = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]
grades_list = ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"]

# وظائف الذاكرة والمزامنة
def initialize_system():
    for key, config in DB_FILES.items():
        if key not in st.session_state:
            if os.path.exists(config["file"]):
                try:
                    df = pd.read_csv(config["file"], encoding="utf-8-sig")
                    # التأكد من وجود كافة الأعمدة المطلوبة في حال تم التحديث من نسخة قديمة
                    for col in config["cols"]:
                        if col not in df.columns: df[col] = ""
                    st.session_state[key] = df
                except:
                    st.session_state[key] = pd.DataFrame(columns=config["cols"])
            else:
                st.session_state[key] = pd.DataFrame(columns=config["cols"])

def sync_to_disk(key):
    st.session_state[key].to_csv(DB_FILES[key]["file"], index=False, encoding="utf-8-sig")

initialize_system()

# ==========================================
# 2. نظام الدخول وحماية الجلسة
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏆 نظام إتقان - الدخول الاحترافي</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if u.upper() == "ASSAF" and p == "7734":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("عذراً، البيانات غير صحيحة")
    st.stop()

# ==========================================
# 3. لوحة التحكم الجانبية والتصدير
# ==========================================
st.sidebar.title("💎 لوحة القيادة")
menu = st.sidebar.radio("الانتقال السريع:", ["📊 الإحصائيات", "🏠 إدارة الطلاب", "✅ التحضير", "📖 سجل التسميع", "🎯 رصد الدرجات", "📋 السجلات العامة"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 مركز التقارير")
export_choice = st.sidebar.selectbox("اختر الجدول:", ["bio", "hifz", "att", "grades"], format_func=lambda x: {"bio":"الطلاب","hifz":"التسميع","att":"الحضور","grades":"الدرجات"}[x])
if st.sidebar.download_button("تصدير كملف Excel (CSV)", 
                             st.session_state[export_choice].to_csv(index=False, sep=';', encoding="utf-8-sig").encode('utf-8-sig'), 
                             f"itqan_{export_choice}_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True):
    st.sidebar.success("تم التصدير بنجاح")

# ==========================================
# 4. الشاشات المتطورة
# ==========================================

# --- شاشة الإحصائيات (Dashboard) ---
if menu == "📊 الإحصائيات":
    st.header("📊 نظرة عامة على الأداء")
    df_bio = st.session_state.bio
    df_hifz = st.session_state.hifz
    df_att = st.session_state.att
    df_grades = st.session_state.grades
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الطلاب", len(df_bio))
    
    # حساب نسبة حضور اليوم
    today = datetime.now().strftime("%Y-%m-%d")
    att_today = df_att[df_att['التاريخ'] == today]
    present_count = len(att_today[att_today['الحالة'] == "حاضر"])
    col2.metric("حضور اليوم", f"{present_count}", f"{len(att_today)} مسجل")
    
    # متوسط الدرجات
    avg_total = df_grades['المعدل'].mean() if not df_grades.empty else 0
    col3.metric("متوسط الدرجات العام", f"{avg_total:.1f}%")
    
    # إنجاز الحفظ
    total_pages = df_hifz['الصفحات'].sum() if not df_hifz.empty else 0
    col4.metric("إجمالي الصفحات المسمعة", f"{total_pages}")
    
    st.markdown("---")
    st.subheader("📈 آخر التحديثات")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("📝 أحدث تسجيلات التسميع")
        st.table(df_hifz.tail(5)[['الاسم', 'السورة', 'التقييم']])
    with c_b:
        st.write("🎯 أعلى الطلاب معدلاً")
        if not df_grades.empty:
            st.table(df_grades.sort_values(by='المعدل', ascending=False).head(5)[['الاسم', 'المعدل', 'التقدير']])

# --- إدارة الطلاب (مع الحذف والتحقق) ---
elif menu == "🏠 إدارة الطلاب":
    st.header("👤 إدارة ملفات الطلاب")
    df = st.session_state.bio
    t1, t2 = st.tabs(["➕ إضافة طالب جديد", "✏️ تعديل وحذف الملفات"])
    
    with t1:
        with st.form("add_full", clear_on_submit=True):
            st.write("📋 أدخل بيانات الطالب بدقة:")
            c1, c2 = st.columns(2)
            name = c1.text_input("الاسم الثلاثي*")
            age = c2.selectbox("العمر", [str(i) for i in range(5, 61)])
            grade = c1.selectbox("الصف الدراسي", grades_list)
            phone = c2.text_input("رقم الجوال")
            email = st.text_input("البريد الإلكتروني")
            if st.form_submit_button("💾 حفظ البيانات"):
                if not name:
                    st.error("الاسم حقل مطلوب!")
                else:
                    new_id = f"ID-{len(df) + 101}"
                    new_row = pd.DataFrame([[name, new_id, age, grade, phone, email]], columns=DB_FILES["bio"]["cols"])
                    st.session_state.bio = pd.concat([df, new_row], ignore_index=True)
                    sync_to_disk("bio")
                    st.success(f"تم تسجيل الطالب {name} بنجاح.") ; st.rerun()

    with t2:
        if not df.empty:
            target = st.selectbox("اختر الطالب للإجراء:", [""] + df['الاسم'].tolist())
            if target:
                idx = df[df['الاسم'] == target].index[0]
                with st.form("edit_full"):
                    st.warning(f"تعديل بيانات: {target}")
                    # استرجاع القيم الحالية بدقة
                    u_age = st.selectbox("العمر", [str(i) for i in range(5, 61)], index=[str(i) for i in range(5, 61)].index(str(df.at[idx, 'العمر'])))
                    u_grade = st.selectbox("الصف الدراسي", grades_list, index=grades_list.index(df.at[idx, 'الصف']))
                    u_phone = st.text_input("رقم الجوال", value=df.at[idx, 'الهاتف'])
                    u_email = st.text_input("البريد الإلكتروني", value=df.at[idx, 'الإيميل'])
                    
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("🔄 تحديث البيانات"):
                        st.session_state.bio.at[idx, 'العمر'] = u_age
                        st.session_state.bio.at[idx, 'الصف'] = u_grade
                        st.session_state.bio.at[idx, 'الهاتف'] = u_phone
                        st.session_state.bio.at[idx, 'الإيميل'] = u_email
                        sync_to_disk("bio")
                        st.success("تم التحديث") ; st.rerun()
                    
                    if c2.form_submit_button("🗑️ حذف الطالب نهائياً"):
                        st.session_state.bio = df.drop(idx)
                        # حذف مرتبط في الجداول الأخرى اختيارياً (للحفاظ على سلامة البيانات)
                        sync_to_disk("bio")
                        st.warning("تم الحذف من النظام") ; st.rerun()

# --- التسميع (مع التاريخ التراكمي) ---
elif menu == "📖 سجل التسميع":
    st.header("📖 رصد التسميع اليومي")
    df_bio = st.session_state.bio
    if df_bio.empty:
        st.info("يرجى إضافة طلاب أولاً")
    else:
        with st.form("hifz_pro", clear_on_submit=True):
            name = st.selectbox("اسم الطالب", df_bio['الاسم'].tolist())
            c1, c2, c3 = st.columns(3)
            date_rec = c1.date_input("تاريخ التسميع", datetime.now())
            surah = c2.selectbox("السورة", quran_surahs)
            part = c3.selectbox("الجزء", list(range(1, 31)))
            c4, c5 = st.columns(2)
            pages = c4.number_input("عدد الصفحات المسمعة", 0.5, 100.0, 1.0, step=0.5)
            errs = c5.number_input("عدد الأخطاء", 0, 100, 0)
            
            if st.form_submit_button("💾 تسجيل في السجل التراكمي"):
                eval_v = "ممتاز" if errs == 0 else "جيد جداً" if errs <= 2 else "جيد"
                new_h = pd.DataFrame([[date_rec.strftime("%Y-%m-%d"), name, part, surah, pages, errs, eval_v]], columns=DB_FILES["hifz"]["cols"])
                st.session_state.hifz = pd.concat([st.session_state.hifz, new_h], ignore_index=True)
                sync_to_disk("hifz")
                st.success(f"تم رصد {pages} صفحات للطالب {name}")

# --- رصد الدرجات (منطق التحديث الذكي) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات والاختبارات")
    df_bio = st.session_state.bio
    if df_bio.empty:
        st.info("لا يوجد طلاب لرصد درجاتهم")
    else:
        with st.form("grades_pro"):
            name = st.selectbox("اختر الطالب", df_bio['الاسم'].tolist())
            date_g = st.date_input("تاريخ الاختبار", datetime.now())
            c1, c2 = st.columns(2)
            q = c1.number_input("القرآن (100)", 0, 100, 0)
            f = c2.number_input("الفقه (100)", 0, 100, 0)
            h = c1.number_input("الحديث (100)", 0, 100, 0)
            s = c2.number_input("السيرة (100)", 0, 100, 0)
            
            if st.form_submit_button("🎯 اعتماد الدرجة"):
                avg = (q+f+h+s)/4
                rate = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                
                # تحديث لو الاسم موجود، أو إضافة لو جديد
                df_g = st.session_state.grades
                if name in df_g['الاسم'].values:
                    idx = df_g[df_g['الاسم'] == name].index[0]
                    st.session_state.grades.iloc[idx] = [date_g.strftime("%Y-%m-%d"), name, q, f, h, s, avg, rate]
                else:
                    new_g = pd.DataFrame([[date_g.strftime("%Y-%m-%d"), name, q, f, h, s, avg, rate]], columns=DB_FILES["grades"]["cols"])
                    st.session_state.grades = pd.concat([df_g, new_g], ignore_index=True)
                
                sync_to_disk("grades")
                st.success(f"تم الرصد بنجاح. المعدل: {avg}%")

# --- السجلات العامة (نظام الفلترة) ---
elif menu == "📋 السجلات العامة":
    st.header("📋 محرك البحث والتقارير")
    st.info("استخدم أدوات التصفية بالأسفل للوصول السريع للمعلومات")
    
    st_tab, h_tab, a_tab, g_tab = st.tabs(["👥 كشف الطلاب", "📖 سجل الحفظ", "✅ الحضور والغياب", "🎯 الدرجات"])
    
    with st_tab:
        search_st = st.text_input("🔍 ابحث عن طالب (بالاسم):", key="search_bio")
        df_filtered = st.session_state.bio
        if search_st: df_filtered = df_filtered[df_filtered['الاسم'].str.contains(search_st)]
        st.dataframe(df_filtered, use_container_width=True)

    with h_tab:
        c1, c2 = st.columns(2)
        search_h = c1.text_input("🔍 بحث بالاسم:", key="search_hifz")
        search_surah = c2.selectbox("🔍 تصفية بالسورة:", ["الكل"] + quran_surahs)
        df_h = st.session_state.hifz
        if search_h: df_h = df_h[df_h['الاسم'].str.contains(search_h)]
        if search_surah != "الكل": df_h = df_h[df_h['السورة'] == search_surah]
        st.dataframe(df_h, use_container_width=True)

    with a_tab:
        st.dataframe(st.session_state.att, use_container_width=True)

    with g_tab:
        st.dataframe(st.session_state.grades, use_container_width=True)
