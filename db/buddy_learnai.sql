CREATE TABLE IF NOT EXISTS user(
    id INT AUTO GENERATED PRIMARY KEY,
    username VARCHAR(15) NOT NULL,
    email VARCHAR(40),
    first_name VARCHAR(30),
    middle_name VARCHAR(30),
    last_name VARCHAR(30),
    profile_pic IMAGE(255);

)