SELECT * FROM internet_provider.client
WHERE c_birthday = (SELECT MAX(c_birthday) FROM client);

