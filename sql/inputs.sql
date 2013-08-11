-- Table: inputs

CREATE TABLE inputs
(
      inputs_hash character (128),
      inputs character varying(8192),
      CONSTRAINT inputs_pkey PRIMARY KEY (inputs_hash)
)
WITH (
      OIDS=FALSE
);
ALTER TABLE inputs
  OWNER TO vbo;
