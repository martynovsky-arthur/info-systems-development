SELECT
    category_name,
    total_revenue,
    percentage
FROM category_revenue_reports
WHERE month = (%(month)s) AND year = (%(year)s)
ORDER BY total_revenue DESC;
