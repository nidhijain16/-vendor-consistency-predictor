-- Placeholder for BigQuery Feature Engineering Logic
-- 
-- Goal: Calculate historical vendor statistics to feed into the XGBoost model.

SELECT 
    vendor_id,
    AVG(actual_prep_time - estimated_prep_time) as historical_delay_avg,
    STDDEV(actual_prep_time - estimated_prep_time) as delay_volatility,
    COUNT(*) as total_orders
FROM 
    `delivery_hero_data.vendor_orders`
WHERE 
    created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 
    vendor_id
HAVING 
    total_orders > 50;
