SELECT
    category_name,
    total_revenue,
    percentage
FROM category_revenue_reports
WHERE month = %s AND year = %s
ORDER BY total_revenue DESC;
