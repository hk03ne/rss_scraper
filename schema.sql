CREATE TABLE entries (
    site_title  varchar(300) NOT NULL,
    site_url    varchar(300) NOT NULL,
    entry_title varchar(300) NOT NULL,
    entry_url   varchar(300) NOT NULL,
    summary     varchar(500) NOT NULL,
    updated     varchar(30)  NOT NULL);

CREATE TABLE feeds (
    id SERIAL                NOT NULL,
    site_title  varchar(300) NOT NULL,
    site_url    varchar(300) NOT NULL,
    feed_url    varchar(300) NOT NULL,
    PRIMARY KEY (id));
