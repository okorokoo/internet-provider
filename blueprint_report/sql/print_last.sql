select order_year, order_month, product_id, quantity, cost from report
where order_year = $in_year and order_month = $in_month