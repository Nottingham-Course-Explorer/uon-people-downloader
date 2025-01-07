create table if not exists staff
(
    username   text PRIMARY KEY NOT NULL,
    salutation text             NOT NULL,
    forename   text             NOT NULL,
    surname    text             NOT NULL,
    department text             NOT NULL,
    title      text             NOT NULL,
    email      text             NOT NULL,

    crawl_time int              NOT NULL
);
