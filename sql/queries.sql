-- OLA Ride Insights: 10 SQL queries (table: rides). Works in MySQL & SQLite.

-- Q1. All successful bookings
SELECT * FROM rides WHERE Booking_Status = 'Success';

-- Q2. Average ride distance per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS avg_distance
FROM rides WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type ORDER BY avg_distance DESC;

-- Q3. Total rides cancelled by customers
SELECT COUNT(*) AS cancelled_by_customers
FROM rides WHERE Booking_Status = 'Canceled by Customer';

-- Q4. Top 5 customers by number of rides
SELECT Customer_ID, COUNT(Booking_ID) AS total_rides
FROM rides GROUP BY Customer_ID
ORDER BY total_rides DESC, Customer_ID LIMIT 5;

-- Q5. Rides cancelled by drivers: personal & car related issues
SELECT COUNT(*) AS driver_cancel_personal_car
FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Q6. Max & min driver rating for Prime Sedan
SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating
FROM rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;

-- Q7. Rides paid via UPI
SELECT * FROM rides WHERE Payment_Method = 'UPI';

-- Q8. Average customer rating per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS avg_customer_rating
FROM rides WHERE Customer_Rating IS NOT NULL
GROUP BY Vehicle_Type ORDER BY avg_customer_rating DESC;

-- Q9. Total booking value of successful rides
SELECT SUM(Booking_Value) AS total_success_booking_value
FROM rides WHERE Booking_Status = 'Success';

-- Q10. Incomplete rides with reason
SELECT Booking_ID, Vehicle_Type, Incomplete_Rides_Reason
FROM rides WHERE Incomplete_Rides = 'Yes';
