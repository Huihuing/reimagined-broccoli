CREATE SEQUENCE IF NOT EXISTS posts_id_seq START WITH 1;

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY DEFAULT nextval('posts_id_seq'),
    title TEXT NOT NULL,
    body TEXT NOT NULL
);

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;
ALTER TABLE posts
    ALTER COLUMN id SET DEFAULT nextval('posts_id_seq');
