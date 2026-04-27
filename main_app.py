import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

DB = {'BIO': 'db_bio.csv', 'GRADES': 'db_grades.csv', 'ATT': 'db_att.csv', 'HIFZ': 'db_hifz.csv'}

# قائمة سور القرآن الكريم كاملة
QURAN_SURAS = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", 
    "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", 
    "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", 
    "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", 
    "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", 
    "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", 
    "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", 
    "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", 
    "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", 
    "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", 
    "النصر", "المسد", "الإخلاص", "الفلق", "الناس"
]

def init_db():
    if not os.path.exists(DB['BIO']):
        pd.DataFrame(columns=['ID', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل']).to_csv(DB['BIO'], index=False)
    if not os.path.exists(DB['GRADES']):
        pd.DataFrame(columns=['ID', 'الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']).to_csv(DB['GRADES'], index=False)
    if not os.path.exists(DB['ATT']):
        pd.DataFrame(columns=['التاريخ', 'ID', 'الاسم', 'الحالة']).to_csv(DB['ATT'], index=False)
    if not os.path.exists(DB['HIFZ']):
        pd.DataFrame(columns=['التاريخ', 'ID', 'الاسم', 'السورة', 'مقدار_الإنجاز', 'مستوى_الإتقان']).to_csv(DB['HIFZ'], index=False)

init_db()

# --- التنقل الجانبي ---
menu = st.sidebar.radio("المجمعات البرمجية:", ["🏠 لوحة التحكم", "👤 تسجيل الطلاب", "🎯 رصد الدرجات", "📍 الحضور والغياب", "📖 متابعة الحفظ", "📊 التقارير"])

# --- 👤 شاشة الطلاب (قوائم منسدلة بالكامل) ---
if menu == "👤 تسجيل الطلاب":
    st.header("👤 تسجيل بيانات الطالب")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("الاسم الكامل")
        c1, c2, c3 = st.columns(3)
        age = c1.selectbox("العمر", [str(i) for i in range(5, 60)])
        grade = c2.selectbox("الصف الدراسي", ["تمهيدي", "ابتدائي", "متوسط", "ثانوي", "جامعي", "خريج"])
        phone = c3.selectbox("رقم الهاتف (مفتاح الدولة)", ["+966", "+971", "+965", "+962"]) # مثال للقوائم
        email_list = st.selectbox("نطاق البريد", ["@gmail.com", "@outlook.com", "@yahoo.com"])
        
        if st.form_submit_button("حفظ الطالب"):
            df = pd.read_csv(DB['BIO'])
            new_id = len(df) + 1
            new_row = pd.DataFrame([[new_id, name, age, grade, phone, email_list]], columns=df.columns)
            new_row.to_csv(DB['BIO'], mode='a', header=False, index=False)
            # تهيئة سجل الدرجات
            pd.DataFrame([[new_id, name, 0, 0, 0, 0, 0, 'جديد']], columns=pd.read_csv(DB['GRADES']).columns).to_csv(DB['GRADES'], mode='a', header=False, index=False)
            st.success(f"تم التسجيل. رقم الطالب الموحد هو: {new_id}")

# --- 🎯 شاشة الدرجات (الوزن النسبي للقرآن) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات (تأثير القرآن 50%)")
    df_bio = pd.read_csv(DB['BIO'])
    if not df_bio.empty:
        with st.form("grade_form"):
            s_name = st.selectbox("اختر الطالب", df_bio['الاسم'].tolist())
            c1, c2, c3, c4 = st.columns(4)
            q = c1.number_input("القرآن الكريم", 0, 100)
            f = c2.number_input("الفقه", 0, 100)
            h = c3.number_input("الحديث", 0, 100)
            s = c4.number_input("السيرة", 0, 100)
            
            if st.form_submit_button("اعتماد الدرجات"):
                # معادلة المعدل الموزون: القرآن 50% والبقية 50% (أي 16.6% لكل مادة أخرى)
                weighted_avg = (q * 0.5) + ((f + h + s) / 3 * 0.5)
                
                if weighted_avg >= 90: rating = "ممتاز 🌟"
                elif weighted_avg >= 80: rating = "جيد جداً ✅"
                elif weighted_avg >= 65: rating = "جيد 🟢"
                else: rating = "مقبول 🟡"
                
                df_g = pd.read_csv(DB['GRADES'])
                df_g.loc[df_g['الاسم'] == s_name, ['القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']] = [q, f, h, s, round(weighted_avg, 2), rating]
                df_g.to_csv(DB['GRADES'], index=False)
                st.success(f"تم التحديث. المعدل الموزون: {weighted_avg}%")

# --- 📖 شاشة متابعة الحفظ (قوائم السور والإنجاز) ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل إنجاز الحفظ")
    df_bio = pd.read_csv(DB['BIO'])
    if not df_bio.empty:
        with st.form("hifz_form", clear_on_submit=True):
            s_name = st.selectbox("اسم الطالب", df_bio['الاسم'].tolist())
            sura = st.selectbox("السورة", QURAN_SURAS)
            
            # قائمة مقدار الإنجاز (2-50 صفحة + جزء وربع)
            amounts = ["ربع جزء", "نصف جزء", "جزء كامل"] + [f"{i} صفحات" for i in range(2, 51)]
            amount = st.selectbox("مقدار الإنجاز", amounts)
            
            quality = st.selectbox("مستوى الإتقان", ["ضعيف", "متوسط", "قوي"])
            
            if st.form_submit_button("حفظ الورد"):
                s_id = df_bio[df_bio['الاسم'] == s_name]['ID'].values[0]
                pd.DataFrame([[datetime.now().date(), s_id, s_name, sura, amount, quality]], columns=pd.read_csv(DB['HIFZ']).columns).to_csv(DB['HIFZ'], mode='a', header=False, index=False)
                st.success("تم الحفظ بنجاح")

# --- استكمال باقي الشاشات (الحضور والتقارير) بنفس المنطق ---
elif menu == "📍 الحضور والغياب":
    st.header("📍 كشف الحضور")
    df_bio = pd.read_csv(DB['BIO'])
    if not df_bio.empty:
        with st.form("att_form"):
            s_name = st.selectbox("اسم الطالب", df_bio['الاسم'].tolist())
            status = st.selectbox("الحالة", ["حاضر ✅", "غائب ❌", "بإذن 📝"])
            if st.form_submit_button("رصد"):
                s_id = df_bio[df_bio['الاسم'] == s_name]['ID'].values[0]
                pd.DataFrame([[datetime.now().date(), s_id, s_name, status]], columns=pd.read_csv(DB['ATT']).columns).to_csv(DB['ATT'], mode='a', header=False, index=False)
                st.success(f"تم رصد {s_name} كـ {status}")
    st.dataframe(pd.read_csv(DB['ATT']).tail(10), use_container_width=True)

elif menu == "📊 التقارير":
    st.header("📊 مركز التحليل الشامل")
    st.subheader("ترتيب الطلاب حسب المعدل الموزون (القرآن هو الحكم)")
    st.dataframe(pd.read_csv(DB['GRADES']).sort_values(by='المعدل', ascending=False), use_container_width=True)
