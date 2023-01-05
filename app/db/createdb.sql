create table user(
    id integer primary key,
    name varchar(255),
    telegram_id integer
);

create table template(
    id integer primary key,
    name varchar(255),
    body text,
    user_id integer,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
