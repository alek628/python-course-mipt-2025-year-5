CREATE TABLE users (
    user_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name text,
    email text UNIQUE,
    password text
);

CREATE TABLE experiments (
    experiment_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name text,
    description text,
    state text,
    assignee integer REFERENCES users
);

CREATE TABLE tags_list (
    tag_list_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name text UNIQUE
);

CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    experiment_id integer REFERENCES experiments,
    tag_list_id integer REFERENCES tags_list,
    UNIQUE (experiment_id, tag_list_id)
);