create table tg_bot_users (
id SERIAL PRIMARY KEY,
tg_user_id INT NOT NULL UNIQUE);

create table futures (
id SERIAL PRIMARY KEY,
future character varying(50) NOT NULL UNIQUE);

create table tg_bot_users_futures (
id BIGSERIAL PRIMARY KEY,
users_id INTEGER NOT NULL REFERENCES tg_bot_users,
futures_id INTEGER NOT NULL REFERENCES futures,
UNIQUE (users_id, futures_id));

CREATE INDEX tg_bot_id_index
ON tg_bot_users (tg_user_id);

CREATE INDEX future_index
ON futures (future);

CREATE INDEX tg_bot_users_futures_index
ON tg_bot_users_futures (users_id, futures_id);