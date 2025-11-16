import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# ============================================
# إضافة مسار Src عشان نقدر نستورد rfm_data.py
# ============================================
SRC_PATH = os.path.join(os.getcwd(), "Src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from rfm_data import load_and_clean_data, create_rfm_data

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
)

st.title("📊 E-Commerce Sales & Customer Segmentation Dashboard")
st.markdown("### RFM Segmentaion تقرير تفاعلي لتحليل المبيعات وسلوك العملاء باستخدام")

# ============================================
# تحميل البيانات مرة واحدة (Cache)
# ============================================
@st.cache_data
@st.cache_data
def load_all():
    data_path = r"C:\Users\LORD LAPTOP\Documents\GitHub\ecommerce-data-analysis\data\raw\digital_market.csv"
    
    df = load_and_clean_data(data_path)
    rfm_df = create_rfm_data(df)

    # 🔥 نضيف عمود Month هنا
    df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)

    return df, rfm_df


data, rfm = load_all()

# ============================================
# Sidebar – Navigation
# ============================================
page = st.sidebar.radio(
    "📌 انتقل إلى:",
    ["Sales Analysis", "RFM Segmentation"]
)

# ============================================
# ================= SALES PAGE ================
# ============================================
if page == "Sales Analysis":
    st.header("📈 Sales Analysis")

    # ====== KPIs ======
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"£{data['TotalPrice'].sum():,.0f}")
    col2.metric("🧾 Total Orders", f"{data['InvoiceNo'].nunique():,}")
    col3.metric("👥 Customers", f"{data['CustomerID'].nunique():,}")

    # ====== Monthly Sales ======
    st.subheader("📅 Monthly Sales Trend")
    monthly_sales = data.groupby("Month")["TotalPrice"].sum().reset_index()

    fig1 = px.line(
        monthly_sales, x="Month", y="TotalPrice",
        markers=True, title="Monthly Sales Trend", template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ====== Top Products ======
    st.subheader("🏆 Top 10 Best-Selling Products")
    top_products = (
        data.groupby("Description")["Quantity"].sum()
        .sort_values(ascending=False).head(10).reset_index()
    )

    fig2 = px.bar(
        top_products, x="Description", y="Quantity",
        title="Top-Selling Products", template="plotly_white"
    )
    fig2.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

    # ====== Top Revenue Products ======
    st.subheader("💸 Top 10 Products by Revenue")
    top_rev = (
        data.groupby("Description")["TotalPrice"].sum()
        .sort_values(ascending=False).head(10).reset_index()
    )

    fig3 = px.bar(
        top_rev, x="Description", y="TotalPrice",
        title="Highest Revenue Products", template="plotly_white"
    )
    fig3.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# ================ RFM PAGE ==================
# ============================================
elif page == "RFM Segmentation":

    st.header("🧩 Customer Segmentation (RFM Analysis)")
    st.write("تحليل RFM يساعدك تعرف: مين أفضل عملائك؟ مين المخلص؟ مين ممكن يرجع؟ ومين ضايع؟")

    # ====== Segments Distribution ======
    st.subheader("📊 Segment Distribution")
    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    fig4 = px.pie(
        seg_counts,
        names="Segment",
        values="Count",
        title="Customer Segments Distribution",
        hole=0.4,
        template="plotly_white"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ====== RFM Table ======
    st.subheader("📋 RFM Table Preview")
    st.dataframe(rfm.head(20))
    # ====== Scatter Plot: Monetary vs Frequency ======
    st.subheader("💰 Spending vs Frequency (RFM)")
    fig5 = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        color="Segment",
        title="Customer Frequency vs Spending",
        template="plotly_white",
        hover_data=["CustomerID"]
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ====== Recency Distribution ======
    st.subheader("🕒 Recency Distribution")
    fig6 = px.histogram(
        rfm,
        x="Recency",
        nbins=30,
        title="How Many Days Since Last Purchase?",
        template="plotly_white"
    )
    st.plotly_chart(fig6, use_container_width=True)