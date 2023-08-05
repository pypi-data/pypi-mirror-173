from typing import Any

from .base import (
    BIGINT as BIGINT,
    BINARY as BINARY,
    BIT as BIT,
    BLOB as BLOB,
    BOOLEAN as BOOLEAN,
    CHAR as CHAR,
    DATE as DATE,
    DATETIME as DATETIME,
    DECIMAL as DECIMAL,
    DOUBLE as DOUBLE,
    ENUM as ENUM,
    FLOAT as FLOAT,
    INTEGER as INTEGER,
    JSON as JSON,
    LONGBLOB as LONGBLOB,
    LONGTEXT as LONGTEXT,
    MEDIUMBLOB as MEDIUMBLOB,
    MEDIUMINT as MEDIUMINT,
    MEDIUMTEXT as MEDIUMTEXT,
    NCHAR as NCHAR,
    NUMERIC as NUMERIC,
    NVARCHAR as NVARCHAR,
    REAL as REAL,
    SET as SET,
    SMALLINT as SMALLINT,
    TEXT as TEXT,
    TIME as TIME,
    TIMESTAMP as TIMESTAMP,
    TINYBLOB as TINYBLOB,
    TINYINT as TINYINT,
    TINYTEXT as TINYTEXT,
    VARBINARY as VARBINARY,
    VARCHAR as VARCHAR,
    YEAR as YEAR,
)
from .dml import Insert as Insert, insert as insert
from .expression import match as match

__all__ = (
    "BIGINT",
    "BINARY",
    "BIT",
    "BLOB",
    "BOOLEAN",
    "CHAR",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "DOUBLE",
    "ENUM",
    "DECIMAL",
    "FLOAT",
    "INTEGER",
    "INTEGER",
    "JSON",
    "LONGBLOB",
    "LONGTEXT",
    "MEDIUMBLOB",
    "MEDIUMINT",
    "MEDIUMTEXT",
    "NCHAR",
    "NVARCHAR",
    "NUMERIC",
    "SET",
    "SMALLINT",
    "REAL",
    "TEXT",
    "TIME",
    "TIMESTAMP",
    "TINYBLOB",
    "TINYINT",
    "TINYTEXT",
    "VARBINARY",
    "VARCHAR",
    "YEAR",
    "dialect",
    "insert",
    "Insert",
    "match",
)

dialect: Any
