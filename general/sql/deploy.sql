-- Non-destructive deployment schema for the GENERAL Supabase project.
CREATE SEQUENCE IF NOT EXISTS posts_id_seq START WITH 1;
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY DEFAULT nextval('posts_id_seq'),
    title TEXT NOT NULL,
    body TEXT NOT NULL
);
ALTER SEQUENCE posts_id_seq OWNED BY posts.id;
ALTER TABLE posts ALTER COLUMN id SET DEFAULT nextval('posts_id_seq');
SELECT setval('posts_id_seq', GREATEST(
    COALESCE((SELECT MAX(id) FROM posts), 0) + 1,
    (SELECT last_value FROM posts_id_seq)
), false);
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
