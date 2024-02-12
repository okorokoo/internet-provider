SELECT cl.* FROM client cl
LEFT JOIN balance on balance.c_id = cl.c_id
WHERE b_id is NULL;