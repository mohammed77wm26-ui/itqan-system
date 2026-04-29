import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# ==========================================
# 1. إعدادات النظام والأداء الفائق
# ==========================================
st.set_page_config(page_title="منظومة إتقان التعليمية", layout="wide", page_icon="🏆")

DB_FILES = {
    "bio": {"file": "db_bio.csv", "cols": ['الاسم', 'الرقم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']},
    "hifz": {"file": "db_hifz.csv", "cols": ['التاريخ', 'الاسم', 'الجزء', 'السورة', 'الصفحات', 'الأخطاء', 'التقييم']},
    "att": {"file": "db_att.csv", "cols": ['التاريخ', 'الاسم', 'الحالة']},
    "grades": {"file": "db_grades.csv", "cols": ['التاريخ', 'الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']}
}

quran_surahs = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]
grades_list = ["ابتدائي", "متوسط", "ثانوي", "جامعي", "خارج الدراسة"]

def initialize_system():
    for key, config in DB_FILES.items():
        if key not in st.session_state:
            if os.path.exists(config["file"]):
                try:
                    df = pd.read_csv(config["file"], encoding="utf-8-sig")
                    # تنظيف الأسماء من المسافات لضمان دقة البحث
                    if 'الاسم' in df.columns: df['الاسم'] = df['الاسم'].astype(str).str.strip()
                    st.session_state[key] = df
                except:
                    st.session_state[key] = pd.DataFrame(columns=config["cols"])
            else:
                st.session_state[key] = pd.DataFrame(columns=config["cols"])

def sync_to_disk(key):
    st.session_state[key].to_csv(DB_FILES[key]["file"], index=False, encoding="utf-8-sig")

initialize_system()

# ==========================================
# 2. حماية الدخول
# ==========================================
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏆 نظام إتقان - الدخول</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.button("دخول", use_container_width=True):
                if u.upper() == "ASSAF" and p == "7734":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("خطأ في البيانات")
    st.stop()

# ==========================================
# 3. القائمة الجانبية
# ==========================================
st.sidebar.title("💎 المنظومة")
menu = st.sidebar.radio("القائمة:", ["📊 الإحصائيات", "🏠 إدارة الطلاب", "✅ التحضير", "📖 سجل التسميع", "🎯 رصد الدرجات", "📋 السجلات"])

def get_csv_download(df):
    return df.to_csv(index=False, sep=';', encoding="utf-8-sig").encode('utf-8-sig')

# ==========================================
# 4. الشاشات (مع حل جذري للتكرار)
# ==========================================

if menu == "📊 الإحصائيات":
    st.header("📊 ملخص الأداء العام")
    df_bio = st.session_state.bio
    df_hifz = st.session_state.hifz
    df_grades = st.session_state.grades
    
    c1, c2, c3 = st.columns(3)
    c1.metric("عدد الطلاب", len(df_bio))
    c2.metric("متوسط الدرجات", f"{df_grades['المعدل'].mean():.1f}%" if not df_grades.empty else "0%")
    c3.metric("إجمالي صفحات الحفظ", f"{df_hifz['الصفحات'].sum()}" if not df_hifz.empty else "0")
    st.divider()
    st.subheader("🎯 الطلاب الأوائل")
    if not df_grades.empty:
        st.dataframe(df_grades.sort_values(by="المعدل", ascending=False).head(5), use_container_width=True)

elif menu == "🏠 إدارة الطلاب":
    st.header("👤 ملفات الطلاب")
    df = st.session_state.bio
    t1, t2 = st.tabs(["➕ إضافة", "✏️ تعديل / حذف"])
    
    with t1:
        with st.form("add_st", clear_on_submit=True):
            name = st.text_input("الاسم الثلاثي*").strip()
            c1, c2 = st.columns(2)
            age = c1.selectbox("العمر", [str(i) for i in range(5, 61)])
            grade = c2.selectbox("الصف", grades_list)
            phone = st.text_input("الجوال")
            email = st.text_input("الإيميل")
            if st.form_submit_button("حفظ"):
                if name:
                    # منع إضافة اسم موجود مسبقاً
                    if name in df['الاسم'].values:
                        st.error("هذا الاسم مسجل مسبقاً في النظام!")
                    else:
                        new_row = pd.DataFrame([[name, f"ID-{len(df)+101}", age, grade, phone, email]], columns=DB_FILES["bio"]["cols"])
                        st.session_state.bio = pd.concat([df, new_row], ignore_index=True)
                        sync_to_disk("bio")
                        st.success("تم الحفظ") ; st.rerun()
                else: st.warning("الاسم مطلوب")

    with t2:
        if not df.empty:
            target = st.selectbox("اختر الطالب:", [""] + df['الاسم'].tolist())
            if target:
                idx = df[df['الاسم'] == target].index[0]
                with st.form("edit_st"):
                    u_age = st.selectbox("العمر", [str(i) for i in range(5, 61)], index=[str(i) for i in range(5, 61)].index(str(df.at[idx, 'العمر'])))
                    u_grade = st.selectbox("الصف", grades_list, index=grades_list.index(df.at[idx, 'الصف']))
                    u_phone = st.text_input("الجوال", value=df.at[idx, 'الهاتف'])
                    u_email = st.text_input("الإيميل", value=df.at[idx, 'الإيميل'])
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("تحديث"):
                        st.session_state.bio.at[idx, 'العمر'] = u_age
                        st.session_state.bio.at[idx, 'الصف'] = u_grade
                        st.session_state.bio.at[idx, 'الهاتف'] = u_phone
                        st.session_state.bio.at[idx, 'الإيميل'] = u_email
                        sync_to_disk("bio")
                        st.success("تم التحديث") ; st.rerun()
                    if c2.form_submit_button("حذف الطالب"):
                        st.session_state.bio = df.drop(idx)
                        sync_to_disk("bio")
                        st.warning("تم الحذف") ; st.rerun()

elif menu == "✅ التحضير":
    st.header("✅ التحضير اليومي")
    df_bio = st.session_state.bio
    today = datetime.now().strftime("%Y-%m-%d")
    if df_bio.empty: st.info("لا يوجد طلاب")
    else:
        with st.form("att_form"):
            st.write(f"تحضير تاريخ: {today}")
            results = []
            for name in df_bio['الاسم']:
                status = st.radio(f"{name}", ["حاضر", "غائب", "مستأذن"], horizontal=True, key=f"att_{name}")
                results.append([today, name, status])
            if st.form_submit_button("حفظ الكشف"):
                # الحل الجذري: حذف تحضير اليوم القديم قبل الإضافة لمنع التكرار
                st.session_state.att = st.session_state.att[st.session_state.att['التاريخ'] != today]
                new_att = pd.DataFrame(results, columns=DB_FILES["att"]["cols"])
                st.session_state.att = pd.concat([st.session_state.att, new_att], ignore_index=True)
                sync_to_disk("att")
                st.success("تم الحفظ")

elif menu == "📖 سجل التسميع":
    st.header("📖 التسميع التراكمي")
    df_bio = st.session_state.bio
    if not df_bio.empty:
        with st.form("hifz_f", clear_on_submit=True):
            name = st.selectbox("الطالب", df_bio['الاسم'].tolist())
            c1, c2, c3 = st.columns(3)
            date_v = c1.date_input("التاريخ", datetime.now())
            surah = c2.selectbox("السورة", quran_surahs)
            part = c3.selectbox("الجزء", range(1, 31))
            c4, c5 = st.columns(2)
            pages = c4.number_input("الصفحات", 0.5, 100.0, 1.0)
            errs = c5.number_input("الأخطاء", 0, 100, 0)
            if st.form_submit_button("تسجيل الحفظ"):
                eval_v = "ممتاز" if errs == 0 else "جيد جداً" if errs <= 2 else "جيد"
                new_row = pd.DataFrame([[date_v.strftime("%Y-%m-%d"), name, part, surah, pages, errs, eval_v]], columns=DB_FILES["hifz"]["cols"])
                st.session_state.hifz = pd.concat([st.session_state.hifz, new_row], ignore_index=True)
                sync_to_disk("hifz")
                st.success("تم التسجيل")

elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات (تحديث تلقائي)")
    df_bio = st.session_state.bio
    if df_bio.empty: st.info("أضف طلاباً")
    else:
        with st.form("gr_form"):
            name = st.selectbox("الطالب", df_bio['الاسم'].tolist())
            date_g = st.date_input("تاريخ الاختبار", datetime.now())
            c1, c2 = st.columns(2)
            q = c1.number_input("القرآن", 0, 100, 0)
            f = c2.number_input("الفقه", 0, 100, 0)
            h = c1.number_input("الحديث", 0, 100, 0)
            s = c2.number_input("السيرة", 0, 100, 0)
            if st.form_submit_button("اعتماد الدرجة"):
                avg = (q+f+h+s)/4
                rate = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد"
                
                # --- الحل الجذري لمنع تكرار الاسم ---
                # 1. حذف السجل القديم لهذا الطالب تماماً من الذاكرة
                st.session_state.grades = st.session_state.grades[st.session_state.grades['الاسم'] != name]
                
                # 2. إضافة السجل الجديد
                new_g = pd.DataFrame([[date_g.strftime("%Y-%m-%d"), name, q, f, h, s, avg, rate]], columns=DB_FILES["grades"]["cols"])
                st.session_state.grades = pd.concat([st.session_state.grades, new_g], ignore_index=True)
                
                # 3. مزامنة
                sync_to_disk("grades")
                st.success(f"تم تحديث درجات {name} بنجاح.")

elif menu == "📋 السجلات":
    st.header("📋 السجلات والتقارير")
    st.info("اضغط على اسم العمود للترتيب، أو استخدم خانة البحث")
    sel = st.selectbox("عرض جدول:", ["bio", "hifz", "att", "grades"], format_func=lambda x: {"bio":"الطلاب","hifz":"التسميع","att":"الحضور","grades":"الدرجات"}[x])
    
    search = st.text_input("🔍 بحث سريع بالاسم...")
    display_df = st.session_state[sel]
    if search:
        display_df = display_df[display_df['الاسم'].str.contains(search)]
    
    st.dataframe(display_df, use_container_width=True)
    st.download_button("📥 تحميل هذا الجدول إكسل", get_csv_download(display_df), f"{sel}.csv", "text/csv")
