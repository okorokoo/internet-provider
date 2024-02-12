SELECT cl.* FROM new_view3 JOIN client cl USING(c_id) WHERE cont = (SELECT MAX(cont) FROM new_view3);
