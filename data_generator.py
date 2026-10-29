import random
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker('uk_UA')
Faker.seed(42)
random.seed(42)

DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/petshop_dwh"


# ---------- ВИМІРИ ----------
def generate_brands():
    names = ["Royal Canin", "Purina", "Hill's", "Acana",
             "Whiskas", "Pedigree", "Trixie", "Ferplast"]
    return pd.DataFrame([
        {"brand_id": i + 1,
         "brand_name": name,
         "country": fake.country()}
        for i, name in enumerate(names)
    ])


def generate_pet_owners(num=1000):
    rows = []
    for i in range(1, num + 1):
        email = fake.email() if random.random() > 0.1 else None  # 10% NULL
        rows.append({
            "owner_id": i,
            "full_name": fake.name(),
            "email": email,
            "city": fake.city(),
            "pet_type": random.choice(["dog", "cat", "bird", "fish", "rodent"]),
            "registration_date": fake.date_between(start_date="-2y", end_date="today"),
        })
    df = pd.DataFrame(rows)
    # 5% дублікатів (щоб було що чистити в dbt)
    duplicates = df.sample(frac=0.05, random_state=42)
    return pd.concat([df, duplicates], ignore_index=True)


def generate_pet_supplies(brand_ids, num=100):
    categories = ["Корм для собак", "Корм для котів", "Іграшка",
                  "Лежак", "Нашийник", "Акваріум", "Клітка"]
    rows = []
    for i in range(1, num + 1):
        category = random.choice(categories)
        rows.append({
            "supply_id": i,
            "brand_id": random.choice(brand_ids),
            "supply_name": f"{category} {fake.word()}",
            "category": category,
            "price": round(random.uniform(30.0, 3000.0), 2),
            "is_active": random.choice([True, True, False]),
        })
    return pd.DataFrame(rows)


# ---------- ФАКТИ ----------
def generate_transactions(owner_ids, supply_ids, num=5000):
    rows = []
    for _ in range(num):
        rows.append({
            "transaction_id": fake.uuid4(),
            "owner_id": random.choice(owner_ids),
            "supply_id": random.choice(supply_ids),
            "quantity": random.randint(1, 5),
            "transaction_date": fake.date_time_between(start_date="-1y", end_date="now"),
            "status": random.choices(["completed", "pending", "cancelled"],
                                     weights=[80, 15, 5])[0],
        })
    return pd.DataFrame(rows)


def generate_loyalty_points(owner_ids, num=3000):
    rows = []
    for i in range(1, num + 1):
        rows.append({
            "loyalty_id": i,
            "owner_id": random.choice(owner_ids),
            "points": random.randint(5, 500),
            "accrual_date": fake.date_time_between(start_date="-1y", end_date="now"),
            "reason": random.choice(["purchase", "birthday", "promo", "referral"]),
        })
    return pd.DataFrame(rows)


# ---------- ДОДАТКОВО (завдання ЛР №1): відгуки ----------
def generate_reviews(owner_ids, supply_ids, num=1500):
    rows = []
    for i in range(1, num + 1):
        comment = fake.sentence(nb_words=10) if random.random() > 0.2 else None  # 20% NULL
        rows.append({
            "review_id": i,
            "supply_id": random.choice(supply_ids),
            "owner_id": random.choice(owner_ids),
            "rating": random.randint(1, 5),
            "comment": comment,
        })
    return pd.DataFrame(rows)


# ---------- ГЕНЕРАЦІЯ ----------
df_brands = generate_brands()
df_owners = generate_pet_owners()
df_supplies = generate_pet_supplies(df_brands["brand_id"].tolist())

owner_ids = df_owners["owner_id"].unique().tolist()
supply_ids = df_supplies["supply_id"].tolist()

df_transactions = generate_transactions(owner_ids, supply_ids)
df_loyalty = generate_loyalty_points(owner_ids)
df_reviews = generate_reviews(owner_ids, supply_ids)

TABLES = {
    "brands": df_brands,
    "pet_owners": df_owners,
    "pet_supplies": df_supplies,
    "transactions": df_transactions,
    "loyalty_points": df_loyalty,
    "reviews": df_reviews,
}

for name, df in TABLES.items():
    print(f"Згенеровано {name}: {len(df)} рядків")


# ---------- ЗАВАНТАЖЕННЯ В DWH ----------
def load_data_to_dwh():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()
    for name, df in TABLES.items():
        print(f"Завантаження {name}...")
        df.to_sql(name, engine, schema="raw", if_exists="replace", index=False)
    print("Дані успішно завантажені у схему 'raw'!")


if __name__ == "__main__":
    load_data_to_dwh()
