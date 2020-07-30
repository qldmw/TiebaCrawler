CREATE TABLE public.contenttable (
    id integer NOT NULL,
    floor integer NOT NULL,
    content character varying(10000) NOT NULL,
    accountname character varying(100) NOT NULL,
    posttime timestamp without time zone,
    backuptime timestamp without time zone
);

CREATE TABLE public.commenttable (
    id integer NOT NULL,
    floor integer NOT NULL,
    comment character varying(5000) NOT NULL,
    accountname character varying(100) NOT NULL,
    posttime timestamp without time zone,
    backuptime timestamp without time zone
);
