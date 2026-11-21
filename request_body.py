from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
#problem 1 creating a book with pydantic models
class Book(BaseModel):
    title:str
    author:str
    price:float
    in_stock:bool=True
@app.post("/books")
def books(book:Book):
    return {"status":"created","book":book}

#problem 2 order total calculator
class Order(BaseModel):
    item_name:str
    customer_name:str
    price:float
    quantity:int
    discount_per:float
@app.post("/orders")
def bill(order:Order):
    subtotal=order.quantity*order.price
    total=subtotal*(1-((order.discount_per)/100))
    return {
        "customer name":order.customer_name,
        "item name":order.item_name,
        "subtotal":subtotal,
        "discount applied":order.discount_per,
        "total":total
    }

