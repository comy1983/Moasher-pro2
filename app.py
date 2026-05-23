import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. إعدادات الهوية البصرية الحصرية (مستوحاة من منصة مدرستي)
st.set_page_config(page_title="منصة مؤشر التعليمية", layout="wide", initial_sidebar_state="expanded")

# تطبيق تصميم مخصص CSS للألوان والخطوط والبطاقات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    /* إعدادات النص والاتجاه العام */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #f8f9fa; /* خلفية بيضاء مائلة للرمادي الفاتح جداً */
    }
    
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-left: 1px solid #e9ecef;
    }
    
    /* تصميم البطاقات الذكية للإحصائيات */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-top: 5px solid #28a745; /* الخط الأخضر المميز لمنصة مدرستي */
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 16px;
        color: #6c757d;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #212529;
    }
    
    /* تحسين شكل الأزرار */
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* تعديل العناوين */
    h1, h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. ترويسة المنصة الاحترافية
st.markdown("""
<div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 25px; border-right: 8px solid #28a745;">
    <h1 style="margin: 0; font-size: 28px;">📊 منصة مؤشر الخوارزمية للتحليل التنبئي</h1>
    <p style="margin: 5px 0 0 0; color: #6c757d; font-size: 16px;">لوحة التحكم الذكية لإدارة تعليم المنطقة - تحليل نتائج (نافس / قدرات / تحصيلي)</p>
</div>
""", unsafe_allow_html=True)

# 3. رفع ملف البيانات
uploaded_file = st.file_uploader("📂 اسحبي وأفلتِ ملف البيانات هنا (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # قراءة البيانات
        df = pd.read_excel(uploaded_file)
        
        # التأكد من الأعمدة الأساسية وحساب الفجوة
        df['الفجوة التعليمية'] = df['درجة المدرسة'] - df['درجة الاختبار المعياري']
        
        # تصنيف النطاقات
        def classify_zone(row):
            if row['الفجوة التعليمية'] <= 5 and row['درجة الاختبار المعياري'] >= 75:
                return '🟢 نطاق التميز'
            elif row['الفجوة التعليمية'] <= 15:
                return '🟡 النطاق الآمن'
            else:
                return '🔴 نطاق الدعم المستهدف'
        
        df['النطاق والتصنيف'] = df.apply(classify_zone, axis=1)
        
        # --- الشريط الجانبي للفلترة والبحث الذكي ---
        st.sidebar.header("🔍 أدوات التصفية والبحث")
        
        # 1. البحث باسم المدرسة
        search_query = st.sidebar.text_input("ابحثي عن مدرسة معينة:")
        
        # 2. الفلترة حسب النطاق
        all_categories = ['الكل'] + list(df['النطاق والتصنيف'].unique())
        selected_category = st.sidebar.selectbox("تصفية حسب نطاق الدعم:", all_categories)
        
        # تطبيق الفلاتر على البيانات
        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['اسم المدرسة'].str.contains(search_query, na=False)]
        if selected_category != 'الكل':
            filtered_df = filtered_df[filtered_df['النطاق والتصنيف'] == selected_category]
            
        # --- عرض المؤشرات العامة (البطاقات الذكية) ---
        st.markdown("### 📌 المؤشرات الرئيسية للمنطقة")
        col1, col2, col3 = st.columns(3)
        
        total_schools = filtered_df['اسم المدرسة'].nunique()
        avg_gap = round(filtered_df['الفجوة التعليمية'].mean(), 2)
        target_schools = filtered_df[filtered_df['النطاق والتصنيف'] == '🔴 نطاق الدعم المستهدف']['اسم المدرسة'].nunique()
        
        with col1:
            st.markdown(f"""<div class='metric-card'><div class='metric-title'>إجمالي المدارس المشمولة</div><div class='metric-value'>{int(total_schools)} مدرسة</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card' style='border-top-color: #ffc107;'><div class='metric-title'>متوسط الفجوة التعليمية</div><div class='metric-value'>{avg_gap} %</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class='metric-card' style='border-top-color: #dc3545;'><div class='metric-title'>مدارس الدعم المستهدف</div><div class='metric-value'>{int(target_schools)} مدرسة</div></div>""", unsafe_allow_html=True)
            
        # --- الرسوم البيانية ---
        st.markdown("---")
        st.markdown("### 📈 التحليل الإحصائي والتوزيع")
        
        chart_col, space_col = st.columns([2, 1])
        with chart_col:
            fig = px.pie(filtered_df, names='النطاق والتصنيف', color='النطاق والتصنيف',
                         title="توزيع المدارس حسب نطاقات الأداء التعليمي",
                         color_discrete_map={'🟢 نطاق التميز':'#28a745', '🟡 النطاق الآمن':'#ffc107', '🔴 نطاق الدعم المستهدف':'#dc3545'})
            fig.update_layout(font_family="Tajawal", title_alignment="right")
            st.plotly_chart(fig, use_container_width=True)
            
        # --- جدول البيانات والتقارير ---
        st.markdown("---")
        st.markdown("### 📋 جدول نتائج التحليل التنبئي")
        
        display_cols = ['اسم المدرسة', 'درجة المدرسة', 'درجة الاختبار المعياري', 'الفجوة التعليمية', 'النطاق والتصنيف']
        st.dataframe(filtered_df[display_cols].reset_index(drop=True), use_container_width=True)
        
        # --- تفعيل ميزة تحميل التقرير المطور كملف Excel ---
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            filtered_df[display_cols].to_excel(writer, index=False, sheet_name='تقرير المؤشرات')
        
        st.markdown(" ")
        st.download_button(
            label="📥 تحميل التقرير الـخِتامي المطور (Excel)",
            data=buffer.getvalue(),
            file_name="تقرير_مبادرة_مؤشر_الاحترافي.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error("⚠️ عذراً، تأكدي من أن ملف الـ Excel يحتوي بدقة على الأعمدة التالية كعناوين: 'اسم المدرسة'، 'درجة المدرسة'، 'درجة الاختبار المعياري'")
else:
    st.info("💡 المنصة جاهزة تماماً وبانتظار سحب أو رفع ملف الـ Excel لبدء التحليل الفوري.")
