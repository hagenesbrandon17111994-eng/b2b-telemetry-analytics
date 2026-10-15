WITH SalesCTE AS (
    -- Собираем нужные данные через JOIN
    SELECT
        m.manager,
        c.region,
        SUM(f.total_revenue_rub) as total_sales
    FROM fact_sales f
    LEFT JOIN dim_managers m ON f.manager_id = m.manager_id
    LEFT JOIN dim_clients c ON f.client_id = c.client_id
    WHERE f.status = 'Успешно реализовано'
    GROUP BY m.manager, c.region
)
SELECT
    manager,
    region,
    total_sales,
    -- Ранжируем менеджеров внутри каждого региона
    RANK() OVER(PARTITION BY region ORDER BY total_sales DESC) as regional_rank,
    -- Считаем долю продаж менеджера от общих продаж в регионе
    ROUND(total_sales / SUM(total_sales) OVER(PARTITION BY region) * 100, 2) as region_share_percent
FROM SalesCTE
ORDER BY region, regional_rank;
"""

analytics_df = pd.read_sql_query(query, conn)
display(analytics_df.head(10))