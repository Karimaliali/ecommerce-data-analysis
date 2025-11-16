📦 E-commerce Data Analysis & Customer Segmentation (RFM + Dashboard)
This project provides a complete end-to-end analysis of an e-commerce dataset,
including data cleaning, exploratory data analysis (EDA), RFM segmentation,
and an interactive dashboard built with Streamlit, using Plotly visualizations.
🚀 Project Structure
ecommerce-data-analysis/
│
├── data/
│   └── raw/
│       └── digital_market.csv
│
├── Notebooks/
│   └── exploration.ipynb
│
├── Src/
│   └── rfm_data.py
│
├── dashboard/
│   └── app.py
│
└── README.md
📊 Features
✅ 1. Data Cleaning
Remove negative quantities and prices
Drop missing CustomerID
Create total revenue column
Convert InvoiceDate to datetime
✅ 2. Exploratory Data Analysis
Top selling products
Top revenue products
Sales by country
Monthly sales trends
Customer spending distribution
Scatter analysis (price vs quantity)
✅ 3. RFM Segmentation
Customers are divided into segments based on:
R – Recency: Last purchase date
F – Frequency: Number of invoices
M – Monetary: Total spending
Segments include:
Champions
Loyal Customers
New Customers
At Risk
Hibernating
Potential
✅ 4. Interactive Dashboard (Streamlit + Plotly)
Real-time charts
Filter customers
View RFM segmentation visually
Monthly trends and product insights
Run dashboard: streamlit run dashboard/app.py
🛠️ Technologies Used
Python
Pandas
NumPy
Matplotlib
Plotly
Streamlit
Markdown
Jupyter Notebook
▶️ How to Run the Project
1. Install dependencies   pip install -r requirements.txt
2. Start Jupyter Notebook    python -m notebook
3. Run Streamlit Dashboard    streamlit run dashboard/app.py

❤️ Author
Karim Elshazly – Data Analysis & Visualization
🎯 Ready to Impress
This project is designed to look professional on GitHub and impressive in portfolio or job interviews.