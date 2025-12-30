from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def hello():
    return "hello, welcome to the site"

#dumy data addtion if table is empty
products = [
    Product(id=1, name="Laptop", price=1200.99, quantity=10, description="High-performance laptop suitable for work and gaming."),
    Product(id=2, name="Smartphone", price=799.49, quantity=25, description="Latest model smartphone with advanced features."),
    Product(id=3, name="Headphones", price=199.99, quantity=50, description="Noise-cancelling over-ear headphones for immersive sound."),
    Product(id=4, name="Monitor", price=299.99, quantity=15, description="24-inch full HD monitor with vibrant display."),
    Product(id=5, name="Keyboard", price=49.99, quantity=40, description="Mechanical keyboard with customizable RGB lighting."),
    Product(id=6, name="Mouse", price=29.99, quantity=60, description="Wireless ergonomic mouse with adjustable DPI.")
]
    
    
def get_db():
    db = session()
    try:
        yield db
        
    finally:
        db.close()
    

def init_db():
    
    db = session()
    count = db.query(database_models.Product).count
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()
    
init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()
    
    return db_products


@app.get("/products/{id}")
def get_product_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product 
    return "Product Not Found"


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated Sucessfully."
    else:
        return "Product Not Found"
    
    
@app.delete("/products/{id}")
def delete_product(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    else:
        return "product not found"
    