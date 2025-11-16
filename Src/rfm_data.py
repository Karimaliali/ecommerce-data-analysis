import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_and_clean_data(data_path):
    """تحميل البيانات وتطبيق التنظيف الأساسي."""
    try:
        data = pd.read_csv(data_path, encoding='latin1')

        # التنظيف
        data['TotalPrice'] = data['Quantity'] * data['UnitPrice']
        data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]
        data = data.dropna(subset=['CustomerID'])
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def create_rfm_data(df):
    """RFM بدون استعمال qcut إطلاقاً — تقسيم يدوي وآمن."""
    if df is None:
        return None

    # 1 — Reference Date
    ref_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    # 2 — RFM Metrics
    rfm = df.groupby('CustomerID').agg(
        Recency=('InvoiceDate', lambda x: (ref_date - x.max()).days),
        Frequency=('InvoiceNo', 'nunique'),
        Monetary=('TotalPrice', 'sum')
    ).reset_index()

    # ===================================================
    # 3 — Scoring Manual (أفضل حل بدون أي qcut)
    # ===================================================

    # Recency Score (كلما قل الرقم كان أفضل)
    rfm['R_Score'] = pd.cut(
        rfm['Recency'],
        bins=[-1, 30, 90, 180, 365, rfm['Recency'].max()],
        labels=[5, 4, 3, 2, 1]
    )

    # Frequency Score
    rfm['F_Score'] = pd.cut(
        rfm['Frequency'],
        bins=[0, 1, 2, 4, 6, rfm['Frequency'].max()],
        labels=[1, 2, 3, 4, 5]
    )

    # Monetary Score
    rfm['M_Score'] = pd.cut(
        rfm['Monetary'],
        bins=[0, 50, 200, 500, 2000, rfm['Monetary'].max()],
        labels=[1, 2, 3, 4, 5]
    )

    # تحويل لرقم
    rfm[['R_Score', 'F_Score', 'M_Score']] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(int)

    # 4 — Total Score
    rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

    # 5 — Segmentation
    def segment(row):
        if row['R_Score'] >= 4 and row['F_Score'] >= 4:
            return "01. Champions"
        elif row['F_Score'] >= 4:
            return "02. Loyal Customers"
        elif row['R_Score'] >= 4:
            return "03. New Customers"
        elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
            return "04. At Risk"
        elif row['R_Score'] <= 2:
            return "05. Hibernating"
        else:
            return "06. Potential"

    rfm['Segment'] = rfm.apply(segment, axis=1)
    return rfm


   

# ====== تشغيل مباشر (اختياري للمراجعة) ======
if __name__ == '__main__':
    DATA_PATH = os.path.join(os.getcwd(), 'data', 'raw', 'digital_market.csv')

    data = load_and_clean_data(DATA_PATH)
    rfm_result = create_rfm_data(data)

    if rfm_result is not None:
        print("RFM created successfully:")
        print(rfm_result.head())