
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://admin:adminpassword@localhost:5432/petshop_dwh"
)

tables = [
    "pet_owners",
    "brands",
    "pet_supplies",
    "transactions",
    "loyalty_points",
    "reviews"
]

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

for table in tables:
    df = pd.read_sql_table(table, engine, schema="public")
    df.to_sql(
        table,
        engine,
        schema="raw",
        if_exists="replace",
        index=False
    )
    print(f"{table}: {len(df)} записів завантажено")

print("Дані успішно завантажені у схему 'raw'!")