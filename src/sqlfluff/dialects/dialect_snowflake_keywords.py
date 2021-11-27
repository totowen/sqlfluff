"""A list of all Snowflake SQL key words."""

snowflake_reserved_keywords = """ACCOUNT
ALL
ALTER
AND
ANY
AS
BETWEEN
BY
CASE
CAST
CHECK
COLUMN
CONNECT
CONNECTION
CONSTRAINT
CREATE
CROSS
CURRENT
CURRENT_DATE
CURRENT_TIME
CURRENT_TIMESTAMP
CURRENT_USER
DATABASE
DELETE
DISTINCT
DROP
ELSE
EXISTS
FOLLOWING
FOR
FROM
FULL
GRANT
GROUP
GSCLUSTER
HAVING
ILIKE
IN
INCREMENT
INNER
INSERT
INTERSECT
INTO
IS
ISSUE
JOIN
LATERAL
LEFT
LIKE
LOCALTIME
LOCALTIMESTAMP
MINUS
NATURAL
NOT
NULL
OF
ON
OR
ORDER
ORGANIZATION
PARTITION
PIVOT
QUALIFY
REGEXP
REVOKE
RIGHT
RLIKE
ROW
ROWS
SAMPLE
SCHEMA
SELECT
SET
SOME
START
STRICT
TABLE
TABLESAMPLE
THEN
TO
TRIGGER
TRY_CAST
UNION
UNIQUE
UPDATE
UNPIVOT
USING
VALUES
VIEW
WHEN
WHENEVER
WHERE
WITH
"""

snowflake_unreserved_keywords = """ABORT
ABORT_STATEMENT
ACCESS
ACCOUNTS
ADD
ADMIN
AFTER
ALLOW_OVERLAPPING_EXECUTION
API
APPLY
ASC
AT
AUTHORIZATION
AUTHORIZATIONS
AUTO_INCREMENT
AUTO_INGEST
AUTO_REFRESH
AUTO_RESUME
AUTO_SUSPEND
AUTOINCREMENT
AVRO
AWS_SNS_TOPIC
BEFORE
BEGIN
BERNOULLI
BINARY
BINDING
BLOCK
CACHE
CALL
CALLED
CALLER
CASCADE
CASE_INSENSITIVE
CASE_SENSITIVE
CHAIN
CHANGE_TRACKING
CHARACTER
CLONE
CLUSTER
COLLATE
COLUMNS
COMMENT
COMMIT
CONCURRENTLY
CONTINUE
COPY
CSV
CUBE
CYCLE
DATA
DATA_RETENTION_TIME_IN_DAYS
DATABASES
DATE
DATEADD
DAY
DAYOFYEAR
DEFAULT
DEFAULT_DDL_COLLATION
DEFERRABLE
DEFERRED
DELEGATED
DESC
DESCRIBE
DISABLE
DOMAIN
DOUBLE
ECONOMY
ENABLE
END
ENFORCE_LENGTH
ENFORCED
ENUM
ESCAPE
EXCEPT
EXECUTE
EXECUTION
EXPLAIN
EXTENSION
EXTERNAL
FILE
FILE_FORMAT
FILES
FILTER
FIRST
FORCE
FOREIGN
FORMAT
FORMAT_NAME
FORMATS
FUNCTION
FUNCTIONS
FUTURE
GLOBAL
GRANTED
GRANTS
GROUPING
HISTORY
HOUR
IDENTITY
IF
IGNORE
IMMEDIATE
IMMUTABLE
IMPORTED
INDEX
INITIALLY
INITIALLY_SUSPENDED
INPUT
INTEGRATION
INTEGRATIONS
INTERVAL
JAVASCRIPT
JSON
KEY
LANGUAGE
LARGE
LAST
LIMIT
LOCAL
LOCATION
LOCKS
MANAGE
MANAGED
MASKING
MATCH_BY_COLUMN_NAME
MATCHED
MATERIALIZED
MAX_CLUSTER_COUNT
MAX_CONCURRENCY_LEVEL
MAX_DATA_EXTENSION_TIME_IN_DAYS
MAXVALUE
MERGE
MILLISECOND
MIN_CLUSTER_COUNT
MINUTE
MINVALUE
ML
MODEL
MODIFY
MONITOR
MONTH
NAME
NAN
NETWORK
NEXTVAL
NO
NOCACHE
NOCYCLE
NONE
NOORDER
NOTIFICATION
NULLS
OBJECT
OBJECTS
OFFSET
ON_ERROR
OPERATE
OPTION
OPTIONS
ORC
OUTER
OVER
OVERLAPS
OVERWRITE
OWNER
OWNERSHIP
PARAMETERS
PARQUET
PASSWORD
PATTERN
PIPE
PIPES
POLICIES
POLICY
PRECEDING
PRECISION
PRIMARY
PRIOR
PRIVILEGES
PROCEDURE
PROCEDURES
PUBLIC
PURGE
QUARTER
QUERIES
RANGE
READ
RECURSIVE
REFERENCES
REFERENCE_USAGE
REFRESH_ON_CREATE
REGIONS
REMOVE
RENAME
REPEATABLE
REPLACE
REPLICATION
RESET
RESOURCE
RESOURCE_MONITOR
RESPECT
RESTRICT
RESUME
RETURN_ALL_ERRORS
RETURN_ERRORS
RETURN_FAILED_ONLY
RETURNS
ROLE
ROLES
ROLLBACK
ROLLUP
ROUTINE
ROUTINES
SCALING_POLICY
SCHEDULE
SCHEMAS
SECOND
SECURE
SECURITY
SEED
SEPARATOR
SEQUENCE
SEQUENCES
SERVER
SESSION
SESSION_USER
SETS
SHARE
SHARES
SHOW
SIZE_LIMIT
SKIP_FILE
STAGE
STAGE_COPY_OPTIONS
STAGE_FILE_FORMAT
STAGES
STANDARD
STARTS
STATEMENT
STATEMENT_QUEUED_TIMEOUT_IN_SECONDS
STATEMENT_TIMEOUT_IN_SECONDS
STORAGE
STREAM
STREAMS
SUSPEND
SUSPENDED
SYSDATE
SYSTEM
SWAP
TABLES
TABLESPACE
TABULAR
TAG
TASK
TASKS
TEMP
TEMPLATE
TEMPORARY
TERSE
TEXT
TIME
TIMESTAMP
TRANSACTION
TRANSACTIONS
TRANSIENT
TRUNCATE
TRUNCATECOLUMNS
TYPE
UNBOUNDED
UNSET
UNSIGNED
USAGE
USE
USE_ANY_ROLE
USER
USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE
USER_TASK_TIMEOUT_MS
USERS
VALIDATION_MODE
VALUE
VARIABLES
VARYING
VERSION
VIEWS
VOLATILE
WAIT_FOR_COMPLETION
WAREHOUSE
WAREHOUSE_SIZE
WAREHOUSES
WEEK
WEEKDAY
WINDOW
WITH
WITHIN
WITHOUT
WORK
WRAPPER
WRITE
XML
YEAR
ZONE"""
