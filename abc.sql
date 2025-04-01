-- 违反规则的写法：使用GROUP BY去重但无聚合函数
SELECT customer_id, order_date 
FROM orders 
GROUP BY customer_id, order_date;

-- 正确写法：使用DISTINCT替代
SELECT DISTINCT customer_id, order_date 
FROM orders;
