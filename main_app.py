import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

def get_data(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file, dtype=str) # قراءة الكل كنصوص لمنع أخطاء الأرقام

# --- نظام الحماية ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 دخول النظام</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("اسم المستخدم").strip()
        p = st.text_input("كلمة المرور", type="password").strip()
        if st.button("دخول", use_container_width=True):
            if u.upper() in ["ASSAF", "عساف"] and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# تحميل البيانات
BIO = get_data('db_bio.csv', ['الرقم', 'الاسم', 'العمر', 'الصف', 'الهاتف', 'الإيميل'])
ATT = get_data('db_att.csv', ['التاريخ', 'الاسم', 'الحالة'])
HIFZ = get_data('db_hifz.csv', ['الاسم', 'الجزء', 'السورة', 'الصفحات', 'التقييم'])
GRADES = get_data('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])

menu = st.sidebar.radio("القائمة الرئيسية", ["🏠 بيانات الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "🎯 رصد الدرجات", "📋 السجل العام"])

# --- 1. بيانات الطلاب (قوائم منسدلة لكل شيء) ---
if menu == "🏠 بيانات الطلاب":
    st.header("📝 إدارة بيانات الطلاب")
    
    stages = ["", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", 
              "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي", "جامعي"]
    ages = [""] + [str(i) for i in range(5, 60)]

    st.subheader("🔍 البحث والتعديل")
    student_list = ["➕ إضافة طالب جديد"] + BIO['الاسم'].tolist()
    selected_name = st.selectbox("اختر الاسم لتعديله أو إضافة جديد", student_list)

    # تعبئة القيم الافتراضية
    is_new = selected_name == "➕ إضافة طالب جديد"
    if not is_new:
        row = BIO[BIO['الاسم'] == selected_name].iloc[0]
        v_name, v_age, v_grade, v_id, v_phone, v_email = row['الاسم'], row['العمر'], row['الصف'], row['الرقم'], row['الهاتف'], row['الإيميل']
    else:
        v_name, v_age, v_grade, v_id, v_phone, v_email = "", "", "", "", "", ""

    with st.form("bio_master_form"):
        # الاسم يظل نصاً للإضافة، ويتحول لقائمة في التعديل
        name = st.text_input("الاسم الثلاثي", value=v_name)
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("العمر", ages, index=ages.index(v_age) if v_age in ages else 0)
            grade = st.selectbox("الصف الدراسي", stages, index=stages.index(v_grade) if v_grade in stages else 0)
        
        with col2:
            # الرقم التسلسلي كقائمة إذا كان موجوداً، أو نص للجديد
            s_id = st.text_input("الرقم التسلسلي (ID)", value=v_id)
            phone = st.text_input("رقم الهاتف", value=v_phone)
            
        email = st.text_input("البريد الإلكتروني", value=v_email)
        
        btn_label = "💾 حفظ البيانات" if is_new else "🔄 تحديث البيانات"
        if st.form_submit_button(btn_label):
            if name and s_id:
                # تحديث قاعدة البيانات
                new_data = BIO[BIO['الاسم'] != selected_name] if not is_new else BIO
                added_row = pd.DataFrame([[s_id, name, age, grade, phone, email]], columns=BIO.columns)
                pd.concat([new_data, added_row], ignore_index=True).to_csv('db_bio.csv', index=False)
                st.success("تمت العملية بنجاح")
                st.rerun()
            else: st.error("الاسم والرقم مطلوبان")

# --- 2. التحضير اليومي ---
elif menu == "✅ التحضير اليومي":
    st.header("✅ كشف الحضور")
    if not BIO.empty:
        with st.form("att_f"):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            status = st.selectbox("الحالة", ["حاضر", "غائب", "بعذر"])
            if st.form_submit_button("تسجيل"):
                new_att = pd.DataFrame([[pd.Timestamp.now().date(), student, status]], columns=ATT.columns)
                pd.concat([ATT, new_att], ignore_index=True).to_csv('db_att.csv', index=False)
                st.success("تم الحفظ")

# --- 3. متابعة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل الحفظ")
    if not BIO.empty:
        with st.form("hifz_f"):
            st_name = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            c1, c2, c3 = st.columns(3)
            with c1: part = st.selectbox("الجزء", [f"جزء {i}" for i in range(1, 31)])
            with c2: sura = st.selectbox("السورة", ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"])
            with c3: page = st.selectbox("الصفحة", [f"صفحة {i}" for i in range(1, 605)])
            rate = st.selectbox("التقييم", ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"])
            if st.form_submit_button("حفظ"):
                new_h = pd.DataFrame([[st_name, part, sura, page, rate]], columns=HIFZ.columns)
                pd.concat([HIFZ, new_h], ignore_index=True).to_csv('db_hifz.csv', index=False)
                st.success("تم الحفظ")

# --- 4. رصد الدرجات (رقمي مباشر) ---
elif menu == "🎯 رصد الدرجات":
    st.header("🎯 رصد الدرجات")
    if not BIO.empty:
        with st.form("grade_f"):
            student = st.selectbox("الطالب", [""] + BIO['الاسم'].tolist())
            col1, col2 = st.columns(2)
            q = col1.number_input("القرآن (50%)", 0.0, 100.0, 0.0, step=1.0)
            f = col1.number_input("الفقه", 0.0, 100.0, 0.0, step=1.0)
            h = col2.number_input("الحديث", 0.0, 100.0, 0.0, step=1.0)
            s = col2.number_input("السيرة", 0.0, 100.0, 0.0, step=1.0)
            if st.form_submit_button("ترحيل"):
                avg = (q * 0.5) + (((f + h + s) / 3) * 0.5)
                تقدير = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
                new_g = pd.DataFrame([[student, q, f, h, s, round(avg, 2), تقدير]], columns=GRADES.columns)
                pd.concat([GRADES[GRADES['الاسم'] != student], new_g], ignore_index=True).to_csv('db_grades.csv', index=False)
                st.success(f"تم الحفظ بمعدل {round(avg, 2)}%")
                st.balloons()

# --- 5. السجل العام ---
elif menu == "📋 السجل العام":
    st.header("📋 السجلات")
    t1, t2, t3, t4 = st.tabs(["الطلاب", "التحضير", "الحفظ", "النتائج"])
    t1.dataframe(BIO, use_container_width=True)
    t2.dataframe(ATT, use_container_width=True)
    t3.dataframe(HIFZ, use_container_width=True)
    t4.dataframe(GRADES, use_container_width=True)
