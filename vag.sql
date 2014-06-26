CREATE TABLE varnish(
   id INTEGER PRIMARY KEY   AUTOINCREMENT,
   name           TEXT    NOT NULL,
   ip           TEXT    NOT NULL,
   port           TEXT    NOT NULL,
   secret           TEXT    NOT NULL
);
