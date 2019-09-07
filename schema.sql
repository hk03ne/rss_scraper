CREATE TABLE entries (
    site_title not null, 
    site_url not null, 
    entry_title not null, 
    entry_url not null, 
    summary, 
    updated not null);

CREATE TABLE feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    site_title not null, 
    site_url not null, 
    feed_url not null unique);

INSERT INTO feeds (site_title, site_url, feed_url) 
    VALUES ("技術評論社", "https://gihyo.jp", "https://gihyo.jp/feed/atom");
INSERT INTO feeds (site_title, site_url, feed_url)
    VALUES ("Mogura VR", "https://www.moguravr.com", "https://www.moguravr.com/feed");
