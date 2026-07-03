from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func

from database import engine, get_db, Base
from models import Product
from schemas import (
    ProductCreate,
    ProductResponse,
    ProductListResponse,
    StatisticsResponse,
)
from cache import cache

# Создаём таблицы при старте приложения
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products API",
    description="API для работы с товарами + кэширование + статистика",
    version="1.0.0",
)


# =============================================================================
# GET /products/ — список товаров (с кэшированием)
# =============================================================================
@app.get("/products/", response_model=ProductListResponse)
def get_products(
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    cache_key = f"products_list_skip{skip}_limit{limit}"
    cached = cache.get(cache_key)

    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    products = db.query(Product).offset(skip).limit(limit).all()
    total = db.query(Product).count()

    data = {"products": products, "total": total}
    cache.set(cache_key, data, ttl=60)  # кэш на 60 секунд

    response.headers["X-Cache"] = "MISS"
    return data


# =============================================================================
# GET /products/{id} — получить товар по ID
# =============================================================================
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail=f"Товар с ID {product_id} не найден")
    return product


# =============================================================================
# GET /statistics/ — базовая аналитика
# =============================================================================
@app.get("/statistics/", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total = db.query(Product).count()

    if total == 0:
        return StatisticsResponse(
            total_products=0,
            average_price=0.0,
            min_price=0.0,
            max_price=0.0,
            categories={},
        )

    avg_price = db.query(sa_func.avg(Product.price)).scalar() or 0.0
    min_price = db.query(sa_func.min(Product.price)).scalar() or 0.0
    max_price = db.query(sa_func.max(Product.price)).scalar() or 0.0

    category_counts = (
        db.query(Product.category, sa_func.count(Product.id))
        .group_by(Product.category)
        .all()
    )
    categories = {
        (cat if cat else "Без категории"): count
        for cat, count in category_counts
    }

    return StatisticsResponse(
        total_products=total,
        average_price=round(float(avg_price), 2),
        min_price=float(min_price),
        max_price=float(max_price),
        categories=categories,
    )


# =============================================================================
# POST /products/ — создание товара (для тестирования кэша)
# =============================================================================
@app.post("/products/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    cache.clear()  # инвалидация кэша при изменении данных
    return db_product