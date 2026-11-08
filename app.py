"""OLA Ride Insights - Streamlit app. Run: streamlit run app/app.py"""
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent.parent
st.set_page_config(page_title="OLA Ride Insights", page_icon="🚖", layout="wide")

@st.cache_data
def load():
    return pd.read_csv(ROOT / "data" / "ola_cleaned.csv", parse_dates=["Date"])

df = load()
con = sqlite3.connect(":memory:")
df.assign(Date=df["Date"].astype(str)).to_sql("rides", con, index=False)

QUERIES = {
 "Q1 Successful bookings": "SELECT * FROM rides WHERE Booking_Status='Success'",
 "Q2 Avg distance per vehicle type": "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS avg_distance FROM rides WHERE Booking_Status='Success' GROUP BY Vehicle_Type ORDER BY avg_distance DESC",
 "Q3 Rides cancelled by customers": "SELECT COUNT(*) AS cancelled_by_customers FROM rides WHERE Booking_Status='Canceled by Customer'",
 "Q4 Top 5 customers by rides": "SELECT Customer_ID, COUNT(Booking_ID) AS total_rides FROM rides GROUP BY Customer_ID ORDER BY total_rides DESC, Customer_ID LIMIT 5",
 "Q5 Driver cancels: personal & car issues": "SELECT COUNT(*) AS driver_cancel_personal_car FROM rides WHERE Canceled_Rides_by_Driver='Personal & Car related issue'",
 "Q6 Max/Min driver rating (Prime Sedan)": "SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating FROM rides WHERE Vehicle_Type='Prime Sedan' AND Driver_Ratings IS NOT NULL",
 "Q7 UPI payments": "SELECT * FROM rides WHERE Payment_Method='UPI'",
 "Q8 Avg customer rating per vehicle type": "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS avg_customer_rating FROM rides WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type ORDER BY avg_customer_rating DESC",
 "Q9 Total booking value (successful)": "SELECT SUM(Booking_Value) AS total_success_booking_value FROM rides WHERE Booking_Status='Success'",
 "Q10 Incomplete rides + reason": "SELECT Booking_ID, Vehicle_Type, Incomplete_Rides_Reason FROM rides WHERE Incomplete_Rides='Yes'",
}

st.title("🚖 OLA Ride Insights")
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🗂 SQL Explorer", "📈 Power BI Dashboard"])

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
vt = st.sidebar.multiselect("Vehicle type", sorted(df.Vehicle_Type.unique()), default=sorted(df.Vehicle_Type.unique()))
stt = st.sidebar.multiselect("Booking status", sorted(df.Booking_Status.unique()), default=sorted(df.Booking_Status.unique()))
d0, d1 = st.sidebar.date_input("Date range", (df.Date.min().date(), df.Date.max().date()))
f = df[df.Vehicle_Type.isin(vt) & df.Booking_Status.isin(stt) & df.Date.dt.date.between(d0, d1)]

with tab1:
    ok = f[f.Booking_Status == "Success"]
    c = st.columns(5)
    c[0].metric("Total bookings", f"{len(f):,}")
    c[1].metric("Success rate", f"{(len(ok)/max(len(f),1)):.1%}")
    c[2].metric("Revenue (success)", f"₹{ok.Booking_Value.sum():,.0f}")
    c[3].metric("Avg driver rating", f"{ok.Driver_Ratings.mean():.2f}")
    c[4].metric("Avg customer rating", f"{ok.Customer_Rating.mean():.2f}")
    l, r = st.columns(2)
    l.plotly_chart(px.line(f.groupby("Ride_Date").size().reset_index(name="rides"), x="Ride_Date", y="rides", title="Ride volume over time"), width="stretch")
    r.plotly_chart(px.pie(f, names="Booking_Status", title="Booking status breakdown", hole=.4), width="stretch")
    l, r = st.columns(2)
    l.plotly_chart(px.bar(f.groupby("Hour").size().reset_index(name="rides"), x="Hour", y="rides", title="Demand by hour of day"), width="stretch")
    r.plotly_chart(px.bar(ok.groupby("Payment_Method").Booking_Value.sum().reset_index(), x="Payment_Method", y="Booking_Value", title="Revenue by payment method"), width="stretch")

with tab2:
    name = st.selectbox("Choose a query", list(QUERIES))
    st.code(QUERIES[name], language="sql")
    res = pd.read_sql(QUERIES[name], con)
    st.caption(f"{len(res):,} rows")
    q = st.text_input("Search within results")
    if q:
        res = res[res.astype(str).apply(lambda s: s.str.contains(q, case=False)).any(axis=1)]
    st.dataframe(res.head(5000))
    st.download_button("Download CSV", res.to_csv(index=False), file_name="result.csv")

with tab3:
    st.subheader("Power BI Dashboard")
    for name, img in [("Overall", "1_overall.png"), ("Vehicle Type", "2_vehicle_type.png"),
                      ("Revenue", "3_revenue.png"), ("Cancellation", "4_cancellation.png"),
                      ("Ratings", "5_ratings.png")]:
        st.markdown(f"**{name}**")
        st.image(str(ROOT / "screenshots" / img))