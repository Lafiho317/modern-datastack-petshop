
import random
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker("uk_UA")
Faker.seed(42)
random.seed(42)

engine = create_engine(
    "postgresql+psycopg2://admin:adminpassword@localhost:5432/petshop_dwh"
)

# Створення таблиць
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pet_owners (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(150),
            phone VARCHAR(30)
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS brands (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pet_supplies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150),
            category VARCHAR(100),
            price NUMERIC(10,2),
            brand_id INTEGER REFERENCES brands(id)
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            owner_id INTEGER REFERENCES pet_owners(id),
            supply_id INTEGER REFERENCES pet_supplies(id),
            quantity INTEGER,
            total_amount NUMERIC(10,2),
            transaction_date TIMESTAMP
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS loyalty_points (
            id SERIAL PRIMARY KEY,
            owner_id INTEGER REFERENCES pet_owners(id),
            transaction_id INTEGER REFERENCES transactions(id),
            points INTEGER
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            owner_id INTEGER REFERENCES pet_owners(id),
            supply_id INTEGER REFERENCES pet_supplies(id),
            rating INTEGER,
            comment TEXT
        )
    """))

    # Очищення попередніх тестових даних
    conn.execute(text("""
        TRUNCATE TABLE reviews, loyalty_points, transactions,
        pet_supplies, brands, pet_owners RESTART IDENTITY CASCADE
    """))

    # Генерація власників тварин
    owners = [
        {"name": fake.name(), "email": fake.unique.email(), "phone": fake.phone_number()}
        for _ in range(50)
    ]
    conn.execute(text("""
        INSERT INTO pet_owners (name, email, phone)
        VALUES (:name, :email, :phone)
    """), owners)

    # Генерація брендів
    brands = [
        {"name": name}
        for name in ["Royal Canin", "Purina", "Whiskas", "Pedigree",
                     "Hill's", "Brit", "Josera", "Pro Plan", "Acana", "Monge"]
    ]
    conn.execute(text("INSERT INTO brands (name) VALUES (:name)"), brands)

    # Генерація товарів
    supplies = [
        {
            "name": fake.word().capitalize() + " " + random.choice(["корм", "іграшка", "нашийник", "лежанка"]),
            "category": random.choice(["Корм", "Іграшки", "Аксесуари", "Догляд"]),
            "price": round(random.uniform(50, 1500), 2),
            "brand_id": random.randint(1, 10)
        }
        for _ in range(100)
    ]
    conn.execute(text("""
        INSERT INTO pet_supplies (name, category, price, brand_id)
        VALUES (:name, :category, :price, :brand_id)
    """), supplies)

    # Генерація транзакцій
    transactions = []
    for _ in range(500):
        quantity = random.randint(1, 5)
        price = random.uniform(50, 1500)
        transactions.append({
            "owner_id": random.randint(1, 50),
            "supply_id": random.randint(1, 100),
            "quantity": quantity,
            "total_amount": round(price * quantity, 2),
            "transaction_date": fake.date_time_between(start_date="-1y", end_date="now")
        })

    conn.execute(text("""
        INSERT INTO transactions
        (owner_id, supply_id, quantity, total_amount, transaction_date)
        VALUES (:owner_id, :supply_id, :quantity, :total_amount, :transaction_date)
    """), transactions)

    # Нарахування бонусних балів
    points = [
        {
            "owner_id": transaction["owner_id"],
            "transaction_id": i + 1,
            "points": random.randint(1, 100)
        }
        for i, transaction in enumerate(transactions)
    ]
    conn.execute(text("""
        INSERT INTO loyalty_points (owner_id, transaction_id, points)
        VALUES (:owner_id, :transaction_id, :points)
    """), points)

    # Генерація відгуків
    reviews = [
        {
            "owner_id": random.randint(1, 50),
            "supply_id": random.randint(1, 100),
            "rating": random.randint(1, 5),
            "comment": fake.sentence()
        }
        for _ in range(100)
    ]
    conn.execute(text("""
        INSERT INTO reviews (owner_id, supply_id, rating, comment)
        VALUES (:owner_id, :supply_id, :rating, :comment)
    """), reviews)

    # Перевірка кількості записів
    for table in ["pet_owners", "brands", "pet_supplies",
                  "transactions", "loyalty_points", "reviews"]:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        print(f"{table}: {result.scalar()} записів")

print("Генерацію даних завершено!")