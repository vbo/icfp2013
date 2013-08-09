-- Table: program

-- DROP TABLE program;

CREATE TABLE program
(
      id serial NOT NULL,
      size smallint NOT NULL,
      operators character varying(64) NOT NULL,
      code character varying,
      inputs character varying(8192),
      outputs character varying(8192),
      CONSTRAINT program_pkey PRIMARY KEY (id)
)
WITH (
      OIDS=FALSE
);
ALTER TABLE program
  OWNER TO vbo;

