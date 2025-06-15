CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE containers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    collection_id INT REFERENCES collections(id)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE collection_tags (
    collection_id INT REFERENCES collections(id),
    tag_id INT REFERENCES tags(id),
    PRIMARY KEY (collection_id, tag_id)
);

-- Indexes for performance
CREATE INDEX idx_collections_name_trgm ON collections USING GIN (name gin_trgm_ops);
CREATE INDEX idx_containers_name_trgm ON containers USING GIN (name gin_trgm_ops);
CREATE INDEX idx_tags_name ON tags(name);
