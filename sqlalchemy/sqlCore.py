from email.headerregistry import Address
from sqlalchemy import insert, Column, BigInteger, ForeignKey, PrimaryKeyConstraint, create_engine, text, Connection, MetaData, Table, String, Integer, select  # type: ignore
from sqlalchemy.orm import Mapped, Session, as_declarative, declarative_base, declared_attr, foreign, registry, mapped_column
from sqlalchemy.dialects import sqlite, postgresql

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("name", String(30)),
    Column("fullname", String)
)

address_table = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("email_address", String(30),),
    Column("user_id", ForeignKey('users.id'))
)

metadata.create_all(engine)

stmt = insert(user_table).values(name="test", fullname="testest")
stmt_no_values = insert(user_table)
sqlite_stmt = stmt_no_values.compile(engine, sqlite.dialect())
postgresql_stmt = stmt_no_values.compile(engine, postgresql.dialect())

with engine.begin() as conn: #Connection
    result = conn.execute(
        insert(user_table),
        [
            {"name": "Test1", "fullname": "Test1 Full"},
            {"name": "Test2", "fullname": "Test2 Full"},
            {"name": "Test3", "fullname": "Test3 Full"}
        ]
    )

with engine.begin() as conn:
    result = conn.execute(
        select(user_table).where(
            user_table.c.name.startswith("Test"),
            user_table.c.fullname.contains("3")
        )
    )

print(result.all())

