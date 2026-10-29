# Modern Data Stack: Pet Shop (Варіант 6)

Навчальний проєкт з дисципліни «Технології сховищ даних».
Предметна область: мережа зоомагазинів.

## Архітектура (ЛР №1)

Python (Faker + Pandas) -> PostgreSQL 15 у Docker (схема `raw`)

## Таблиці

| Таблиця | Тип | Опис |
|---|---|---|
| brands | вимір | Бренди |
| pet_owners | вимір | Власники тварин |
| pet_supplies | вимір | Товари для тварин |
| transactions | факт | Покупки |
| loyalty_points | факт | Нарахування бонусів |
| reviews | факт | Відгуки на товари |

У даних навмисно закладені «брудні» значення: ~10% порожніх email
та ~5% дублікатів власників. Вони потраплять у Raw-шар «як є»
й будуть очищені в dbt (ЛР №2).

## Як запустити

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d
python data_generator.py
```

## Стек

Python, Faker, Pandas, SQLAlchemy, Docker, PostgreSQL
