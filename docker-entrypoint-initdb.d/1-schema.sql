CREATE TABLE entries (
    user_id     integer      NOT NULL,
    feed_id     integer      NOT NULL,
    entry_title varchar(300) NOT NULL,
    entry_url   varchar(300) NOT NULL,
    summary     varchar(1000) NOT NULL,
    updated     varchar(30)  NOT NULL);

CREATE TABLE feeds (
    id          SERIAL       NOT NULL,
    user_id     integer      NOT NULL,
    site_title  varchar(300) NOT NULL,
    site_url    varchar(300) NOT NULL,
    feed_url    varchar(300) NOT NULL,
    PRIMARY KEY (id));

CREATE TABLE users (
    id              SERIAL       NOT NULL,
    mail            varchar(100) UNIQUE,
    password_digest varchar(100) NOT NULL,
    PRIMARY KEY (id));

CREATE VIEW view_entries AS
    SELECT
        feeds.user_id,
        feeds.site_title, 
        feeds.site_url, 
        entries.entry_title, 
        entries.entry_url, 
        entries.summary, 
        entries.updated
    FROM entries
    INNER JOIN feeds ON entries.feed_id = feeds.id;