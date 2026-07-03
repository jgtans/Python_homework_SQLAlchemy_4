"""Заполнение БД тестовыми товарами. Запуск: python seed.py"""
from database import engine, SessionLocal, Base
from models import Product

Base.metadata.create_all(bind=engine)

test_products = [
    {"name": "Ноутбук ASUS VivoBook 15", "description": "Intel i5, 8GB RAM, 512GB SSD", "price": 54990.00, "category": "Электроника"},
    {"name": "Смартфон Samsung Galaxy A54", "description": "128GB, 6GB RAM", "price": 29990.00, "category": "Электроника"},
    {"name": "Наушники Sony WH-1000XM5", "description": "Беспроводные, шумоподавление", "price": 27990.00, "category": "Электроника"},
    {"name": "Кресло офисное Ergohuman", "description": "Эргономичное с поясничной поддержкой", "price": 35000.00, "category": "Мебель"},
    {"name": "Стол письменный IKEA", "description": "Массив берёзы, 140x60 см", "price": 12990.00, "category": "Мебель"},
    {"name": "Книга 'Чистый код'", "description": "Роберт Мартин", "price": 890.00, "category": "Книги"},
    {"name": "Книга 'Python. К вершинам мастерства'", "description": "Лучшие практики Python", "price": 1250.00, "category": "Книги"},
    {"name": "Клавиатура Keychron K2", "description": "Механическая, беспроводная", "price": 9500.00, "category": "Электроника"},
    {"name": "Монитор LG 27UK850-W", "description": "27\", 4K UHD, IPS, HDR10", "price": 32000.00, "category": "Электроника"},
    {"name": "Рюкзак для ноутбука", "description": "Водонепроницаемый, до 15.6\"", "price": 3500.00, "category": "Аксессуары"},
    {"name": "Мышь Logitech MX Master 3S", "description": "Беспроводная, USB-C", "price": 7990.00, "category": "Электроника"},
    {"name": "Лампа настольная Xiaomi", "description": "LED, регулировка яркости", "price": 2990.00, "category": "Аксессуары"},
]


def seed_database():
    db = SessionLocal()
    try:
        db.query(Product).delete()
        db.commit()
        for data in test_products:
            db.add(Product(**data))
        db.commit()
        print(f"✅ Добавлено {len(test_products)} товаров")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()


