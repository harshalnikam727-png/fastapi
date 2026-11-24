from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
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

#problem 3 validated user registeration
class User(BaseModel):
    username:str=Field(max_length=20,min_length=2)
    password:str=Field(max_length=12,min_length=8)
    age:int=Field(ge=18)
    bio:str|None=Field(default=None)
@app.post("/registration")
def register(user:User):
    return {
        "message":"registration confirmed",
        "username":user.username,
        "age":user.age,
        "bio":user.bio
    }

#problem 4 update a course
courses={
    1:{"name":"maths"},
    2:{"name":"physics"},
    3:{"name":"chemistry"},
}
class New_data(BaseModel):
    name:str=Field(max_length=10)
    id:int=Field(ge=1,le=3)
@app.put("/courses/{id}")
def course(id:int,new:New_data,old_data:bool=False):
    if id not in courses:
        raise HTTPException(404)
    old=courses[id]
    courses[id]=new.model_dump()
    if old_data==True:
        return {"old":old,"updated":courses[id]}
    return {"updated":courses[id]}

#problem 5 food delivery order
class Customer(BaseModel):
    name:str=Field(min_length=2,max_length=20)
    address:str=Field(min_length=2,max_length=50)
    phone:str=Field(min_length=10,max_length=10)
class food_item(BaseModel):
    name:str
    price:float=Field(ge=0)
    quantity:int=Field(ge=1)
class Deliver(BaseModel):
    details:Customer
    items:list[food_item]
@app.post("/delivery_details")
def deliver(deliver:Deliver):
    total_item=0
    total_bill=0
    for i in deliver.items:
        sub_total=i.quantity*i.price
        total_bill+=sub_total
        total_item+=i.quantity
    return {
        "details":deliver.details,
        "total items":total_item,
        "total bill":total_bill
    }





