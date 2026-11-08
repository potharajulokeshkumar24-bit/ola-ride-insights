"""Clean OLA July dataset, export CSV and load into SQLite (table: rides)."""
import sqlite3
import pandas as pd

SRC = "OLA_DataSet.xlsx"   # put the original file next to this script
df = pd.read_excel(SRC, sheet_name="July")

# ---- 1. Standardise ----
df["Vehicle_Type"] = df["Vehicle_Type"].replace({"eBike": "E-Bike"})
df["Date"] = pd.to_datetime(df["Date"])
df["Time"] = df["Time"].astype(str)
df = df.drop_duplicates(subset="Booking_ID")
df = df.drop(columns=["Vehicle Images"])          # icon URLs, not needed for analysis

# ---- 2. Missing values are structural (ride never happened) ----
df["Payment_Method"] = df["Payment_Method"].fillna("Not Applicable")
df["Canceled_Rides_by_Customer"] = df["Canceled_Rides_by_Customer"].fillna("Not Applicable")
df["Canceled_Rides_by_Driver"] = df["Canceled_Rides_by_Driver"].fillna("Not Applicable")
df["Incomplete_Rides"] = df["Incomplete_Rides"].fillna("Not Applicable")
df["Incomplete_Rides_Reason"] = df["Incomplete_Rides_Reason"].fillna("Not Applicable")
# Ratings / TAT stay NULL on purpose: 0 would distort averages.

# ---- 3. Derived features ----
df["Hour"] = df["Date"].dt.hour
df["Day"] = df["Date"].dt.day
df["Day_Name"] = df["Date"].dt.day_name()
df["Ride_Date"] = df["Date"].dt.date.astype(str)
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["Is_Success"] = (df["Booking_Status"] == "Success").astype(int)

# ---- 4. Save ----
df.to_csv("data/ola_cleaned.csv", index=False)
con = sqlite3.connect("data/ola.db")
df.to_sql("rides", con, if_exists="replace", index=False)
con.close()
print(df.shape); print(df.isna().sum()[df.isna().sum() > 0])
