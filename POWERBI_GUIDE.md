# Power BI Dashboard: Build Guide (about 2 to 3 hours)

## 1. Load data
Home > Get data > Text/CSV > `data/ola_cleaned.csv` > Transform Data. Check the types:
- Date = Date/Time; Booking_Value, Ride_Distance, ratings = Decimal; Hour, Day = Whole number.
- Optional: import the vehicle icon URLs from `Sheet2` of the original Excel and set the column's Data category = Image URL.

## 2. DAX measures (Modeling > New measure)
```DAX
Total Bookings        = COUNTROWS(rides)
Success Bookings      = CALCULATE(COUNTROWS(rides), rides[Booking_Status]="Success")
Success Rate %        = DIVIDE([Success Bookings],[Total Bookings])
Total Booking Value   = SUM(rides[Booking_Value])
Success Booking Value = CALCULATE(SUM(rides[Booking_Value]), rides[Booking_Status]="Success")
Avg Distance          = CALCULATE(AVERAGE(rides[Ride_Distance]), rides[Booking_Status]="Success")
Total Distance        = CALCULATE(SUM(rides[Ride_Distance]), rides[Booking_Status]="Success")
Avg Driver Rating     = AVERAGE(rides[Driver_Ratings])
Avg Customer Rating   = AVERAGE(rides[Customer_Rating])
Cancelled Rides       = CALCULATE(COUNTROWS(rides), rides[Booking_Status] IN {"Canceled by Customer","Canceled by Driver"})
```

## 3. Pages (use the layout in Ola-Slides.pptx; add the 5-button navigation bar to every page)
Tip: export each slide of Ola-Slides.pptx as an image (File > Export > PNG) and use it as the page background (Format page > Canvas background), then place visuals on top. Add Page navigator buttons: Insert > Buttons > Navigator > Page navigator.

| Page | Visual | Fields |
|---|---|---|
| **Overall** | Line chart: Ride Volume Over Time | Axis `Ride_Date`, Values `Total Bookings` |
| | Donut: Booking Status Breakdown | Legend `Booking_Status`, Values `Total Bookings` |
| | KPI cards | Total Bookings, Success Rate %, Success Booking Value |
| **Vehicle Type** | Table (matches the slide) | `Vehicle_Type`, Total Booking Value, Success Booking Value, Avg Distance, Total Distance |
| | Bar: Top 5 Vehicle Types by Distance | Axis `Vehicle_Type`, Values `Total Distance`; Filters > Top N = 5 |
| **Revenue** | Bar/Donut: Revenue by Payment Method | `Payment_Method`, `Success Booking Value` (filter out "Not Applicable") |
| | Table/Bar: Top 5 Customers by Booking Value | `Customer_ID`, `Success Booking Value`; Top N = 5 |
| | Column: Ride Distance per Day | Axis `Ride_Date`, Values `Total Distance` |
| **Cancellation** | Bar: Customer cancel reasons | `Canceled_Rides_by_Customer` (exclude "Not Applicable"), Count |
| | Bar: Driver cancel reasons | `Canceled_Rides_by_Driver` (exclude "Not Applicable"), Count |
| **Ratings** | Histogram (column): Driver ratings distribution | `Driver_Ratings`, Count |
| | Histogram: Customer ratings | `Customer_Rating`, Count |
| | Scatter or clustered column: Customer vs Driver by vehicle | `Vehicle_Type`, `Avg Customer Rating`, `Avg Driver Rating` |

## 4. Slicers (sync across pages: View > Sync slicers)
Date (Ride_Date), Vehicle_Type, Booking_Status.

## 5. Publish for Streamlit
Sign in with a Power BI work account (see the "Free Power BI Work Account" link in your brief). Publish, then File > Embed report > Publish to web (public). Paste the link in the app's third tab.
If Publish to web is blocked, take screenshots of each page and add them to the README and your presentation instead.
Save the file as `OLA_Dashboard.pbix` and put it in the repo.
