CREATE TABLE LOGS (
	ID BIGINT NOT NULL,
	MESSAGE VARCHAR(500),
	CONNECT_ID INTEGER,
	CONSTRAINT PK_AGENTLOGG PRIMARY KEY (ID)
);

CREATE INDEX FK_LOGS ON LOGS (CONNECT_ID);
CREATE UNIQUE INDEX FK_LOGS_UQ ON LOGS (ID);