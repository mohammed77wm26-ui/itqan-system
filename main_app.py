import streamlit as st
import pandas as pd
import os

# --- إعدادات النظام الأساسية ---
st.set_page_config(page_title="منظومة إتقان الاحترافية", layout="wide")

# دالة التأكد من وجود ملفات البيانات
def init_db():
    if not os.path.exists('students.csv'):
        pd.DataFrame(columns=['ID', 'الاسم', 'الحلقة', 'المستوى']).to_csv('students.csv', index=False)
    if not os.path.exists('grades.csv'):
        pd.DataFrame(columns=['الاسم', 'القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']).to_csv('grades.csv', index=False)

init_db()

# --- نظام الحماية (تسجيل الدخول) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center;'>🔐 تسجيل دخول المنظومة</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user = st.text_input("اسم المستخدم")
            pw = st.text_input("كلمة المرور", type="password")
            if st.button("دخول النظام", use_container_width=True):
                if user == "ASSAF" and pw == "7734":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("خطأ في بيانات الدخول!")
    st.stop()

# --- واجهة البرنامج بعد الدخول ---
st.sidebar.title("💎 لوحة التحكم")
choice = st.sidebar.radio("القائمة:", ["الرئيسية", "تسجيل الطلاب", "رصد الدرجات", "سجل النتائج"])

# تحميل البيانات
df_s = pd.read_csv('students.csv')
df_g = pd.read_csv('grades.csv')

if choice == "الرئيسية":
    st.header("📈 حالة المنظومة العامة")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الطلاب", len(df_s))
    c2.metric("الحلقات النشطة", len(df_s['الحلقة'].unique()))
    c3.metric("الدرجات المرصودة", len(df_g))
    st.divider()
    st.info("مرحباً بك في منظومة إتقان. استخدم القائمة الجانبية لإدارة المهام.")

elif choice == "تسجيل الطلاب":
    st.header("👤 إضافة طالب جديد")
    with st.form("add_student"):
        s_id = st.text_input("رقم الهوية / الطالب")
        s_name = st.text_input("الاسم الثلاثي")
        s_group = st.selectbox("الحلقة", ["حلقة البخاري", "حلقة مسلم", "حلقة الترمذي"])
        s_level = st.selectbox("المستوى", ["مبتدئ", "متوسط", "متقدم"])
        if st.form_submit_button("حفظ الطالب"):
            if s_name:
                new_s = pd.DataFrame([[s_id, s_name, s_group, s_level]], columns=df_s.columns)
                df_s = pd.concat([df_s, new_s], ignore_index=True)
                df_s.to_csv('students.csv', index=False)
                st.success("تم الحفظ بنجاح!")
                st.rerun()

elif choice == "رصد الدرجات":
    st.header("📝 رصد النتائج")
    if df_s.empty:
        st.warning("لا يوجد طلاب! قم بتسجيل الطلاب أولاً.")
    else:
        student_list = df_s['الاسم'].tolist()
        selected_student = st.selectbox("اختر الطالب", student_list)
        
        col1, col2 = st.columns(2)
        with col1:
            q = st.number_input("القرآن (50%)", 0.0, 100.0, 0.0)
            f = st.number_input("الفقه", 0.0, 100.0, 0.0)
        with col2:
            h = st.number_input("الحديث", 0.0, 100.0, 0.0)
            s = st.number_input("السيرة", 0.0, 100.0, 0.0)
            
        if st.button("ترحيل الدرجة وحفظها"):
            # الحساب الدقيق
            avg = (q * 0.5) + ((f + h + s) / 3 * 0.5)
            grade = "ممتاز" if avg >= 90 else "جيد جداً" if avg >= 80 else "جيد" if avg >= 70 else "مقبول"
            
            # تحديث أو إضافة
            new_entry = [selected_student, q, f, h, s, round(avg, 2), grade]
            if selected_student in df_g['الاسم'].values:
                df_g.loc[df_g['الاسم'] == selected_student, ['القرآن', 'الفقه', 'الحديث', 'السيرة', 'المعدل', 'التقدير']] = [q, f, h, s, round(avg, 2), grade]
            else:
                df_g.loc[len(df_g)] = new_entry
            
            df_g.to_csv('grades.csv', index=False)
            st.success(f"تم ترحيل درجات {selected_student} بنجاح!")
            st.balloons()

elif choice == "سجل النتائج":
    st.header("📋 النتائج النهائية")
    if not df_g.empty:
        st.dataframe(df_g, use_container_width=True)
        csv = df_g.to_csv(index=False).encode('utf-8-sig')
        st.download_button("تحميل السجل (Excel/CSV)", csv, "results.csv", "text/csv")
    else:
        st.info("لا توجد نتائج حالياً.")

# خروج
if st.sidebar.button("خروج من النظام"):
    st.session_state['logged_in'] = False
    st.rerun()
