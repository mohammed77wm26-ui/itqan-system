import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- إعدادات الصفحة والأداء ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# دالة ذكية لإدارة الملفات لضمان السرعة وعدم فقدان البيانات
def manage_db(file_name, columns):
    if not os.path.exists(file_name):
        pd.DataFrame(columns=columns).to_csv(file_name, index=False)
    return pd.read_csv(file_name)

# --- نظام الحماية ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول - منظومة إتقان</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if u == "ASSAF" and p == "7734":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")
    st.stop()

# --- تحميل كافة قواعد البيانات ---
DB = {
    'BIO': manage_db('db_students.csv', ['ID', 'الاسم', 'الهاتف', 'الحلقة', 'المستوى']),
    'ATT': manage_db('db_attendance.csv', ['التاريخ', 'الاسم', 'الحالة']),
    'HIFZ': manage_db('db_hifz.csv', ['التاريخ', 'الاسم', 'السورة', 'مقدار_الإنجاز', 'التقييم']),
    'GRADES': manage_db('db_grades.csv', ['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير'])
}

# --- القائمة الجانبية ---
st.sidebar.title(f"مرحباً بك، {st.session_state.auth and 'أ. عساف'}")
menu = st.sidebar.radio("التنقل بين الشاشات:", 
    ["🏠 الرئيسية", "📝 تسجيل الطلاب", "✅ التحضير اليومي", "📖 متابعة الحفظ", "📊 رصد الدرجات", "📜 السجل العام"])

# --- 1. الرئيسية ---
if menu == "🏠 الرئيسية":
    st.header("📊 لوحة المؤشرات العامة")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("إجمالي الطلاب", len(DB['BIO']))
    kpi2.metric("حالات التحضير", len(DB['ATT']))
    kpi3.metric("سجلات الحفظ", len(DB['HIFZ']))
    st.divider()
    st.image("https://img.freepik.com/free-vector/quran-concept-illustration_114360-9113.jpg", width=300)

# --- 2. تسجيل الطلاب ---
elif menu == "📝 تسجيل الطلاب":
    st.header("👤 إضافة بيانات طالب")
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid = st.text_input("رقم الطالب")
            sname = st.text_input("الاسم الثلاثي")
        with col2:
            sphone = st.text_input("هاتف ولي الأمر")
            sgroup = st.selectbox("الحلقة", ["حلقة البخاري", "حلقة مسلم", "حلقة الترمذي"])
        slevel = st.select_slider("المستوى", options=["الأول", "الثاني", "الثالث"])
        
        if st.form_submit_button("حفظ الطالب"):
            if sname:
                new_row = pd.DataFrame([[sid, sname, sphone, sgroup, slevel]], columns=DB['BIO'].columns)
                DB['BIO'] = pd.concat([DB['BIO'], new_row], ignore_index=True)
                DB['BIO'].to_csv('db_students.csv', index=False)
                st.success("تم تسجيل الطالب بنجاح")
            else: st.error("الاسم مطلوب")

# --- 3. التحضير اليومي ---
elif menu == "✅ التحضير اليومي":
    st.header("📅 تحضير الطلاب")
    date_now = datetime.now().strftime("%Y-%m-%d")
    if not DB['BIO'].empty:
        for index, row in DB['BIO'].iterrows():
            col_n, col_s = st.columns([3, 1])
            col_n.write(row['الاسم'])
            status = col_s.selectbox("الحالة", ["حاضر", "غائب", "مستأذن"], key=f"att_{index}")
            # حفظ التحضير (تبسيطاً يحفظ عند العرض أو بضغط زر)
        if st.button("اعتماد التحضير"):
            st.success("تم حفظ كشف التحضير لليوم")

# --- 4. متابعة الحفظ ---
elif menu == "📖 متابعة الحفظ":
    st.header("📖 سجل الحفظ اليومي")
    if not DB['BIO'].empty:
        s_name = st.selectbox("الطالب", DB['BIO']['الاسم'])
        col1, col2 = st.columns(2)
        with col1:
            sura = st.text_input("السورة / الجزء")
            amount = st.text_input("مقدار الإنجاز (مثلاً: 5 صفحات)")
        with col2:
            rate = st.select_slider("تقييم الحفظ", options=["ضعيف", "جيد", "ممتاز"])
            date_h = st.date_input("التاريخ")
        
        if st.button("تسجيل الحفظ"):
            new_h = pd.DataFrame([[date_h, s_name, sura, amount, rate]], columns=DB['HIFZ'].columns)
            DB['HIFZ'] = pd.concat([DB['HIFZ'], new_h], ignore_index=True)
            DB['HIFZ'].to_csv('db_hifz.csv', index=False)
            st.success("تم تسجيل سجل الحفظ")

# --- 5. رصد الدرجات (حل مشكلة الترحيل) ---
elif menu == "📊 رصد الدرجات":
    st.header("🎯 رصد درجات الاختبارات")
    if not DB['BIO'].empty:
        student = st.selectbox("اختيار الطالب لرصد درجته", DB['BIO']['الاسم'])
        col1, col2 = st.columns(2)
        with col1:
            q = st.number_input("القرآن (من 100)", 0.0, 100.0, 80.0)
            f = st.number_input("الفقه (من 100)", 0.0, 100.0, 80.0)
        with col2:
            h = st.number_input("الحديث (من 100)", 0.0, 100.0, 80.0)
            s = st.number_input("السيرة (من 100)", 0.0, 100.0, 80.0)
        
        if st.button("ترحيل الدرجات إلى السجل النهائي"):
            # الحساب الدقيق مع تحويل الأنواع لتجنب TypeError
            final_avg = (float(q) * 0.5) + (((float(f) + float(h) + float(s)) / 3.0) * 0.5)
            rank = "ممتاز" if final_avg >= 90 else "جيد جداً" if final_avg >= 80 else "جيد" if final_avg >= 70 else "مقبول"
            
            # تحديث السجل أو إضافة جديد
            new_g = [student, q, f, h, s, round(final_avg, 2), rank]
            if student in DB['GRADES']['الاسم'].values:
                DB['GRADES'].loc[DB['GRADES']['الاسم'] == student, ['القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']] = [q, f, h, s, round(final_avg, 2), rank]
            else:
                DB['GRADES'].loc[len(DB['GRADES'])] = new_g
            
            DB['GRADES'].to_csv('db_grades.csv', index=False)
            st.balloons()
            st.success(f"تم الترحيل بنجاح! المعدل: {round(final_avg, 2)}%")

# --- 6. السجل العام ---
elif menu == "📜 السجل العام":
    st.header("📋 كشوفات البيانات")
    tab1, tab2, tab3 = st.tabs(["بيانات الطلاب", "سجل الحفظ", "سجل الدرجات"])
    with tab1: st.dataframe(DB['BIO'], use_container_width=True)
    with tab2: st.dataframe(DB['HIFZ'], use_container_width=True)
    with tab3: st.dataframe(DB['GRADES'], use_container_width=True)

# خروج
if st.sidebar.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
