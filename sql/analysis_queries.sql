-- ============================================================
-- TripPulse Insights
-- Curated Business Analysis Queries
-- Database: trip_pulse_insights
-- Author: Saloni Singh
--
-- 30 representative analyses selected from the complete
-- 50-query analysis set.
-- ============================================================

USE trip_pulse_insights;


-- ============================================================
-- EXECUTIVE OVERVIEW
-- ============================================================

-- QUERY 1 - Excecutive KPI Dashboard
SELECT
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT b.booking_id) AS total_bookings,
    COUNT(DISTINCT t.trip_id) AS total_trips,
    COUNT(DISTINCT d.destination_id) AS total_destinations,
    ROUND(SUM(
        CASE
            WHEN b.booking_status <> 'Cancelled'
            THEN b.final_amount
            ELSE 0
        END
    ), 2) AS total_revenue,
    ROUND(AVG(
        CASE
            WHEN b.booking_status <> 'Cancelled'
            THEN b.final_amount
        END
    ), 2) AS average_booking_value,
    ROUND(AVG(b.travelers_count), 2) AS average_travelers_per_booking
FROM customers c
LEFT JOIN bookings b
    ON c.customer_id = b.customer_id
LEFT JOIN trips t
    ON b.trip_id = t.trip_id
LEFT JOIN destinations d
    ON t.destination_id = d.destination_id;

-- QUERY 2 - Booking Status and Cancellation Analysis
SELECT
    booking_status,
    COUNT(*) AS total_bookings,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings),
        2
    ) AS booking_percentage,
    ROUND(
        SUM(final_amount),
        2
    ) AS total_booking_value
FROM bookings
GROUP BY booking_status
ORDER BY total_bookings DESC;

-- QUERY 3 - Top Destinations by Revenue
SELECT
    d.destination_name,
    COUNT(b.booking_id) AS total_bookings,
    ROUND(SUM(b.final_amount), 2) AS total_revenue,
    ROUND(AVG(b.final_amount), 2) AS average_booking_value
FROM bookings AS b
JOIN trips AS t
    ON b.trip_id = t.trip_id
JOIN destinations AS d
    ON t.destination_id = d.destination_id
WHERE b.booking_status <> 'Cancelled'
GROUP BY d.destination_id, d.destination_name
ORDER BY total_revenue DESC
LIMIT 10;

-- QUERY 4 - Booking Volume VS Revenue
SELECT
    d.destination_name,
    COUNT(b.booking_id) AS total_bookings,
    ROUND(SUM(b.final_amount), 2) AS total_revenue,
    ROUND(AVG(b.final_amount), 2) AS average_booking_value
FROM bookings AS b
JOIN trips AS t
    ON b.trip_id = t.trip_id
JOIN destinations AS d
    ON t.destination_id = d.destination_id
WHERE b.booking_status <> 'Cancelled'
GROUP BY d.destination_id, d.destination_name
ORDER BY total_bookings DESC;

-- QUERY 5 - Revenue VS Booking Volume
WITH destination_performance AS (
    SELECT
        d.destination_name,
        COUNT(b.booking_id) AS total_bookings,
        ROUND(SUM(b.final_amount), 2) AS total_revenue
    FROM bookings AS b
    JOIN trips AS t
        ON b.trip_id = t.trip_id
    JOIN destinations AS d
        ON t.destination_id = d.destination_id
    WHERE b.booking_status <> 'Cancelled'
    GROUP BY d.destination_id, d.destination_name
),

benchmarks AS (
    SELECT
        AVG(total_bookings) AS avg_bookings,
        AVG(total_revenue) AS avg_revenue
    FROM destination_performance
)

SELECT
    dp.destination_name,
    dp.total_bookings,
    dp.total_revenue,
    CASE
        WHEN dp.total_bookings >= b.avg_bookings
             AND dp.total_revenue >= b.avg_revenue
            THEN 'High Volume - High Revenue'

        WHEN dp.total_bookings >= b.avg_bookings
             AND dp.total_revenue < b.avg_revenue
            THEN 'High Volume - Low Revenue'

        WHEN dp.total_bookings < b.avg_bookings
             AND dp.total_revenue >= b.avg_revenue
            THEN 'Low Volume - High Revenue'

        ELSE 'Low Volume - Low Revenue'
    END AS performance_segment

FROM destination_performance AS dp
CROSS JOIN benchmarks AS b
ORDER BY dp.total_revenue DESC;

-- ============================================================
-- BOOKING & TREND ANALYSIS
-- ============================================================

-- QUERY 6 - Repeat Customers
WITH customer_booking_summary AS (
    SELECT
        c.customer_id,
        COUNT(b.booking_id) AS total_bookings,
        ROUND(
            SUM(
                CASE
                    WHEN b.booking_status <> 'Cancelled'
                    THEN b.final_amount
                    ELSE 0
                END
            ),
            2
        ) AS total_revenue
    FROM customers AS c
    JOIN bookings AS b
        ON c.customer_id = b.customer_id
    GROUP BY c.customer_id
)

SELECT
    CASE
        WHEN total_bookings = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS total_customers,
    SUM(total_bookings) AS total_bookings,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS avg_customer_revenue
FROM customer_booking_summary
GROUP BY customer_type
ORDER BY total_revenue DESC;

-- QUERY 7 - Monthly Booking Trend
SELECT
    DATE_FORMAT(booking_timestamp, '%Y-%m') AS booking_month,
    COUNT(*) AS total_bookings,
    ROUND(
        SUM(
            CASE
                WHEN booking_status <> 'Cancelled'
                THEN final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue
FROM bookings
GROUP BY DATE_FORMAT(booking_timestamp, '%Y-%m')
ORDER BY booking_month;

-- QUERY 8 - Lead Conversion Funnel
SELECT
    lead_status,
    COUNT(*) AS total_leads,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leads),
        2
    ) AS percentage_of_leads
FROM leads
GROUP BY lead_status
ORDER BY total_leads DESC;

-- QUERY 9 - Conversion Rate by Lead Source
SELECT
    lead_source,
    COUNT(*) AS total_leads,
    SUM(
        CASE
            WHEN lead_status = 'Converted' THEN 1
            ELSE 0
        END
    ) AS converted_leads,
    SUM(
        CASE
            WHEN lead_status = 'Lost' THEN 1
            ELSE 0
        END
    ) AS lost_leads,
    ROUND(
        SUM(
            CASE
                WHEN lead_status = 'Converted' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS conversion_rate
FROM leads
GROUP BY lead_source
ORDER BY conversion_rate DESC;

-- QUERY 10 - Why are Leads being Lost?
SELECT
    lost_reason,
    COUNT(*) AS lost_leads,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM leads WHERE lead_status = 'Lost'),
        2
    ) AS percentage_of_lost_leads
FROM leads
WHERE lead_status = 'Lost'
GROUP BY lost_reason
ORDER BY lost_leads DESC;

-- QUERY 11 - Lead Temperature VS Conversion
SELECT
    lead_temperature,
    COUNT(*) AS total_leads,
    SUM(
        CASE
            WHEN lead_status = 'Converted' THEN 1
            ELSE 0
        END
    ) AS converted_leads,
    SUM(
        CASE
            WHEN lead_status = 'Lost' THEN 1
            ELSE 0
        END
    ) AS lost_leads,
    ROUND(
        SUM(
            CASE
                WHEN lead_status = 'Converted' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS conversion_rate
FROM leads
GROUP BY lead_temperature
ORDER BY conversion_rate DESC;

-- ============================================================
-- LEAD & SALES FUNNEL
-- ============================================================

-- QUERY 13 - Interaction Outcome Performance
SELECT
    interaction_outcome,
    COUNT(*) AS total_interactions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM lead_interactions),
        2
    ) AS percentage_of_interactions
FROM lead_interactions
GROUP BY interaction_outcome
ORDER BY total_interactions DESC;

-- QUERY 16 - Which Employees Handle the Most Leads?
SELECT
    e.employee_id,
    e.employee_name,
    e.designation,
    COUNT(li.interaction_id) AS total_interactions,
    COUNT(DISTINCT li.lead_id) AS unique_leads_handled
FROM employees e
JOIN lead_interactions li
    ON e.employee_id = li.employee_id
GROUP BY
    e.employee_id,
    e.employee_name,
    e.designation
ORDER BY unique_leads_handled DESC;

-- QUERY 17 - Employee Conversion Performance
SELECT
    e.employee_id,
    e.employee_name,
    e.designation,
    COUNT(DISTINCT li.lead_id) AS unique_leads_handled,
    COUNT(DISTINCT CASE
        WHEN l.lead_status = 'Converted'
        THEN li.lead_id
    END) AS converted_leads,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN l.lead_status = 'Converted'
            THEN li.lead_id
        END) * 100.0
        / COUNT(DISTINCT li.lead_id),
        2
    ) AS conversion_rate
FROM employees e
JOIN lead_interactions li
    ON e.employee_id = li.employee_id
JOIN leads l
    ON li.lead_id = l.lead_id
GROUP BY
    e.employee_id,
    e.employee_name,
    e.designation
ORDER BY conversion_rate DESC;

-- QUERY 18 - Employee Performance by Designation
SELECT
    e.designation,
    COUNT(DISTINCT li.lead_id) AS unique_leads_handled,
    COUNT(DISTINCT CASE
        WHEN l.lead_status = 'Converted'
        THEN li.lead_id
    END) AS converted_leads,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN l.lead_status = 'Converted'
            THEN li.lead_id
        END) * 100.0
        / COUNT(DISTINCT li.lead_id),
        2
    ) AS conversion_rate
FROM employees e
JOIN lead_interactions li
    ON e.employee_id = li.employee_id
JOIN leads l
    ON li.lead_id = l.lead_id
WHERE e.designation IN (
    'Sales Executive',
    'Senior Sales Executive',
    'Sales Manager'
)
GROUP BY e.designation
ORDER BY conversion_rate DESC;

-- QUERY 19 - Which Interaction Types are Most Effective?
SELECT
    interaction_type,
    COUNT(*) AS total_interactions,
    SUM(
        CASE
            WHEN interaction_outcome = 'Converted'
            THEN 1
            ELSE 0
        END
    ) AS converted_interactions,
    ROUND(
        SUM(
            CASE
                WHEN interaction_outcome = 'Converted'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS conversion_rate
FROM lead_interactions
GROUP BY interaction_type
ORDER BY conversion_rate DESC;

-- QUERY 20 - Revenue by Booking Source
SELECT
    booking_source,
    COUNT(*) AS total_bookings,
    ROUND(
        SUM(
            CASE
                WHEN booking_status <> 'Cancelled'
                THEN final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue,
    ROUND(
        AVG(
            CASE
                WHEN booking_status <> 'Cancelled'
                THEN final_amount
            END
        ),
        2
    ) AS average_booking_value
FROM bookings
GROUP BY booking_source
ORDER BY total_revenue DESC;

-- ============================================================
-- CANCELLATION & RISK ANALYSIS
-- ============================================================

-- QUERY 22 - Cancellation Rate by Booking Source
SELECT
    booking_source,
    COUNT(*) AS total_bookings,
    SUM(CASE
        WHEN booking_status = 'Cancelled' THEN 1
        ELSE 0
    END) AS cancelled_bookings,
    ROUND(
        100.0 * SUM(CASE
            WHEN booking_status = 'Cancelled' THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS cancellation_rate
FROM bookings
GROUP BY booking_source
ORDER BY cancellation_rate DESC;

-- QUERY 23 - Cancellation Rate by Destination
SELECT
    d.destination_name,
    COUNT(*) AS total_bookings,
    SUM(
        CASE
            WHEN b.booking_status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_bookings,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN b.booking_status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
JOIN destinations d
    ON t.destination_id = d.destination_id
GROUP BY d.destination_name
ORDER BY cancellation_rate DESC;

-- QUERY 24 - Cancellation Rtae by Trip Type
SELECT
    t.trip_type,
    COUNT(*) AS total_bookings,
    SUM(
        CASE
            WHEN b.booking_status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_bookings,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN b.booking_status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
GROUP BY t.trip_type
ORDER BY cancellation_rate DESC;

-- ============================================================
-- TRIP, REVENUE & CUSTOMER ANALYSIS
-- ============================================================

-- QUERY 26 - Average Booking Value by Trip Type
SELECT
    t.trip_type,
    COUNT(*) AS total_bookings,
    ROUND(
        AVG(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
            END
        ),
        2
    ) AS average_booking_value,
    ROUND(
        SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
GROUP BY t.trip_type
ORDER BY average_booking_value DESC;

-- QUERY 27 - Revenue Contribution by Trip Type
SELECT
    t.trip_type,
    COUNT(*) AS total_bookings,
    ROUND(
        SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        )
        /
        (
            SELECT SUM(final_amount)
            FROM bookings
            WHERE booking_status <> 'Cancelled'
        ),
        2
    ) AS revenue_contribution_pct
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
GROUP BY t.trip_type
ORDER BY total_revenue DESC;

-- QUERY 28 - Revenue by Destination Type
SELECT
    d.destination_type,
    COUNT(*) AS total_bookings,
    ROUND(
        SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue,
    ROUND(
        AVG(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
            END
        ),
        2
    ) AS average_booking_value
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
JOIN destinations d
    ON t.destination_id = d.destination_id
GROUP BY d.destination_type
ORDER BY total_revenue DESC;

-- QUERY 29 - Cancellation Rate by Destination Type
SELECT
    d.destination_type,
    COUNT(*) AS total_bookings,
    SUM(
        CASE
            WHEN b.booking_status = 'Cancelled'
            THEN 1
            ELSE 0
        END
    ) AS cancelled_bookings,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN b.booking_status = 'Cancelled'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
JOIN destinations d
    ON t.destination_id = d.destination_id
GROUP BY d.destination_type
ORDER BY cancellation_rate DESC;

-- QUERY 30 - Average Travelers per Booking by Trip Type
SELECT
    t.trip_type,
    COUNT(*) AS total_bookings,
    ROUND(
        AVG(b.travelers_count),
        2
    ) AS average_travelers_per_booking
FROM bookings b
JOIN trips t
    ON b.trip_id = t.trip_id
GROUP BY t.trip_type
ORDER BY average_travelers_per_booking DESC;

-- QUERY 34 - Customer Revenue Segmentation
SELECT
    CASE
        WHEN total_revenue >= 100000 THEN 'High Value'
        WHEN total_revenue >= 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment,
    COUNT(*) AS total_customers,
    ROUND(
        SUM(total_revenue),
        2
    ) AS total_revenue,
    ROUND(
        AVG(total_revenue),
        2
    ) AS average_customer_revenue
FROM (
    SELECT
        customer_id,
        SUM(
            CASE
                WHEN booking_status <> 'Cancelled'
                THEN final_amount
                ELSE 0
            END
        ) AS total_revenue
    FROM bookings
    GROUP BY customer_id
) AS customer_revenue
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- QUERY 35 - Repeat VS One-Time Customer Revenue
SELECT
    CASE
        WHEN booking_count > 1 THEN 'Repeat Customer'
        ELSE 'One-time Customer'
    END AS customer_type,
    COUNT(*) AS total_customers,
    SUM(total_revenue) AS total_revenue,
    ROUND(
        100.0 * SUM(total_revenue)
        /
        (
            SELECT SUM(customer_revenue)
            FROM (
                SELECT
                    customer_id,
                    SUM(
                        CASE
                            WHEN booking_status <> 'Cancelled'
                            THEN final_amount
                            ELSE 0
                        END
                    ) AS customer_revenue
                FROM bookings
                GROUP BY customer_id
            ) AS all_customer_revenue
        ),
        2
    ) AS revenue_contribution_pct,
    ROUND(
        AVG(total_revenue),
        2
    ) AS average_customer_revenue
FROM (
    SELECT
        customer_id,
        COUNT(*) AS booking_count,
        SUM(
            CASE
                WHEN booking_status <> 'Cancelled'
                THEN final_amount
                ELSE 0
            END
        ) AS total_revenue
    FROM bookings
    GROUP BY customer_id
) AS customer_summary
GROUP BY customer_type
ORDER BY total_revenue DESC;

-- ============================================================
-- GROWTH & LEAD-TO-REVENUE ANALYSIS
-- ============================================================

-- QUERY 43 - Monthly Revenue Growth
WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(booking_timestamp, '%Y-%m') AS booking_month,
        ROUND(
            SUM(
                CASE
                    WHEN booking_status <> 'Cancelled'
                    THEN final_amount
                    ELSE 0
                END
            ),
            2
        ) AS monthly_revenue
    FROM bookings
    GROUP BY DATE_FORMAT(booking_timestamp, '%Y-%m')
)

SELECT
    booking_month,
    monthly_revenue,
    ROUND(
        100.0 * (
            monthly_revenue
            - LAG(monthly_revenue) OVER (ORDER BY booking_month)
        )
        / NULLIF(
            LAG(monthly_revenue) OVER (ORDER BY booking_month),
            0
        ),
        2
    ) AS mom_growth_percentage
FROM monthly_revenue
ORDER BY booking_month;

-- QUERY 45 - Lead to Booking Conversion
SELECT
    l.lead_source,
    COUNT(DISTINCT l.lead_id) AS total_leads,
    COUNT(DISTINCT b.lead_id) AS converted_leads,
    ROUND(
        100.0 * COUNT(DISTINCT b.lead_id)
        / COUNT(DISTINCT l.lead_id),
        2
    ) AS lead_to_booking_rate
FROM leads l
LEFT JOIN bookings b
    ON l.lead_id = b.lead_id
GROUP BY l.lead_source
ORDER BY lead_to_booking_rate DESC;

-- QUERY 46 - Lead Source to Booking Revenue
SELECT
    l.lead_source,
    COUNT(DISTINCT l.lead_id) AS total_leads,
    COUNT(DISTINCT b.booking_id) AS total_bookings,
    ROUND(
        SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue,
    ROUND(
        SUM(
            CASE
                WHEN b.booking_status <> 'Cancelled'
                THEN b.final_amount
                ELSE 0
            END
        ) / COUNT(DISTINCT l.lead_id),
        2
    ) AS revenue_per_lead
FROM leads l
LEFT JOIN bookings b
    ON l.lead_id = b.lead_id
GROUP BY l.lead_source
ORDER BY total_revenue DESC;

