from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel,Field
app=FastAPI()


#problem 1 safe user signup
class UserIn(BaseModel):
    name:str
    age:int
    password:str
class UserOut(BaseModel):
    name:str
    age:int
@app.post("/username",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def Username(user:UserIn):
    return user


#problem 2 task manager
tasks_db = {
    1: {"id": 1, "title": "Learn FastAPI", "status": "in_progress", "secret_notes": "Focus on response models"},
    2: {"id": 2, "title": "Build REST API", "status": "pending", "secret_notes": "Use PostgreSQL later"},
    3: {"id": 3, "title": "Write Tests", "status": "pending", "secret_notes": "Check 404 edge cases"},
}
class TaskOut(BaseModel):
    id:int
    title:str
    status:str
@app.get("/tasks_db",response_model=list[TaskOut])
def tasks():
    return list(tasks_db.values())
@app.delete("/items/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id:int):
    if item_id not in tasks_db:
        raise HTTPException(status_code=404,detail="item not found")
    del tasks_db[item_id]
    return 


#problem 3 employee directory
employees_db = {
    1: {"id": 1, "name": "Aarav", "role": "Backend Dev", "salary": 85000},
    2: {"id": 2, "name": "Priya", "role": "Designer", "salary": 78000},
}
class EmplyoeeIn(BaseModel):
    id:int
    name:str
    role:str
    salary:int
class EmployeeOut(BaseModel):
    id:int
    name:str
    role:str
@app.post("/employee",response_model=EmployeeOut,status_code=status.HTTP_201_CREATED)
def add_employee(employee:EmplyoeeIn):
    employees_db[employee.id]=employee.model_dump()
    return employee
@app.get("/employees/{employee_id}",response_model=EmployeeOut)
def info(employee_id:int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404,detail="id not found")
    return employees_db[employee_id]


#problem 4 movie watchlist
movies_db = {
    1: {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8, "added_by": "admin_01"},
    2: {"id": 2, "title": "Interstellar", "genre": "Sci-Fi", "rating": 8.7, "added_by": "admin_02"},
}
class MoviesIn(BaseModel):
    id:int
    title:str
    genre:str
    rating:float
    added_by:str
class MoviesOut(BaseModel):
    id:int
    title:str
    genre:str
    rating:float
@app.post("/add_movie",response_model=MoviesOut,status_code=status.HTTP_201_CREATED)
def added(movie:MoviesIn):
    movies_db[movie.id]=movie.model_dump()
    return movie
@app.get("/movies_db",response_model=list[MoviesOut])
def movies():
    return list(movies_db.values())


#problem 5 support ticket queue
tickets_db = {
    1: {"ticket_id": 1, "subject": "Login error", "priority": "high", "status": "open", "internal_notes": "Check auth logs"},
    2: {"ticket_id": 2, "subject": "Billing question", "priority": "low", "status": "open", "internal_notes": "Refund eligible"},
}
class TicketIn(BaseModel):
    ticket_id:int
    subject:str
    priority:str
    status:str="queued"
    internal_notes:str
class TicketOut(BaseModel):
    ticket_id:int
    subject:str
    priority:str
    status:str="queued"
@app.post("/add_tickets",response_model=TicketOut,status_code=status.HTTP_202_ACCEPTED)
def tickets_added(ticket:TicketIn):
    tickets_db[ticket.ticket_id]=ticket.model_dump()
    return ticket
@app.get("/tickets_db/{ticket_id}",response_model=TicketOut)
def return_ticket(ticket_id:int):
    if ticket_id not in tickets_db:
        raise HTTPException(status_code=404,detail="ticket id is not found")
    return tickets_db[ticket_id]


# problem 6 product catalog
products_db = {
    1: {"id": 1, "name": "Mechanical Keyboard", "price": 4500.0, "supplier_cost": 2800.0},
    2: {"id": 2, "name": "Wireless Mouse", "price": 1800.0, "supplier_cost": 950.0},
}
class Products(BaseModel):
    id:int
    name:str
    price:float
class ProductsIn(Products):
    supplier_cost:float
class ProductsOut(Products):
    pass
@app.post("/add_product",response_model=ProductsOut,status_code=status.HTTP_201_CREATED)
def product_added(product:ProductsIn):
    products_db[product.id]=product.model_dump()
    return product
@app.get("/products_db/{product_id}",response_model=ProductsOut)
def prod(product_id:int):
    if product_id not in products_db:
        raise HTTPException(status_code=404,detail="id not found")
    return products_db[product_id]


#problem 7 inventory upsert
inventory_db = {
    1: {"item_id": 1, "name": "USB-C Hub", "stock": 40, "warehouse_code": "WH-NORTH"},
    2: {"item_id": 2, "name": "HDMI Cable", "stock": 120, "warehouse_code": "WH-SOUTH"},
}
class Inventory(BaseModel):
    name:str
    stock:int
class InventoryIn(Inventory):
    warehouse_code:str
class InventoryOut(Inventory):
    item_id:int
@app.put("/inventory/{item_id}",response_model=InventoryOut)
def invent(item_id:int,response:Response,inventory:InventoryIn):
    if item_id not in inventory_db:
        response.status_code=status.HTTP_201_CREATED
    inventory_db[item_id] = {
    "item_id": item_id,
    "name": inventory.name,
    "stock": inventory.stock,
    "warehouse_code": inventory.warehouse_code,
}
    return inventory_db[item_id]


#problem 8 nested response filtering
orders_db = {
    1: {
        "order_id": 1,
        "customer_name": "Karan",
        "items": [
            {"name": "Laptop Stand", "qty": 1, "unit_price": 1500.0, "wholesale_cost": 800.0},
            {"name": "Mouse Pad", "qty": 2, "unit_price": 300.0, "wholesale_cost": 100.0},
        ],
        "total_amount": 2100.0,
    }
}
class OrderItemBase(BaseModel):
    name:str
    qty:int
    unit_price:float
class OrderItemIn(OrderItemBase):
    wholesale_cost:float
class OrderItemOut(OrderItemBase):
    pass 
class OrderIn(BaseModel):
    order_id:int
    customer_name:str
    items:list[OrderItemIn]
class OrderOut(BaseModel):
    order_id:int
    customer_name:str
    items:list[OrderItemOut]
    total_amount:float
@app.post("/orders",response_model=OrderOut,status_code=status.HTTP_201_CREATED)
def price(order:OrderIn):
    total_amount=0
    for i in order.items:
        total_amount+=i.qty*i.unit_price
    orders_db[order.order_id]=order.model_dump()
    orders_db[order.order_id] = {
    "order_id": order.order_id,
    "customer_name": order.customer_name,
    "items": [i.model_dump() for i in order.items],
    "total_amount": total_amount,
}
    return orders_db[order.order_id]

@app.get("/orders/{order_id}",response_model=OrderOut)
def orde(order_id:int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404,detail="id not found")
    return orders_db[order_id]

#problem 9 clean user profile 
profiles_db = {
    "harshal": {
        "username": "harshal",
        "bio": "Backend Developer",
        "website": None,
        "twitter": "@harshal_dev",
        "secret_email": "harshal@private.com",
    },
    "diya": {
        "username": "diya",
        "bio": None,
        "website": "https://diya.design",
        "twitter": None,
        "secret_email": "diya@private.com",
    },
}
class ProfileOut(BaseModel):
    username:str
    bio:str|None=None
    website:str|None=None
    twitter:str|None=None
@app.get("/profiles_db/{username}",response_model=ProfileOut,response_model_exclude_none=True)
def profiles(username:str):
    return profiles_db[username]

#problem 10 mini crud capstone-book library api
library_db = {
    1: {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "pages": 464,
        "notes": None,
        "internal_cost": 450.0,
    },
    2: {
        "id": 2,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "pages": 616,
        "notes": "Must read for backend",
        "internal_cost": 700.0,
    },
}
class BookBase(BaseModel):
    id:int
    title:str
    author:str
    pages:int=Field(ge=0)
    notes:str|None=None
class BookIn(BookBase):
    internal_cost:int=Field(ge=0)
class BookOut(BookBase):
    pass 

@app.get("/library",response_model=list[BookOut],response_model_exclude_none=True,status_code=status.HTTP_200_OK)
def librar():
    return list(library_db.values())

@app.get("/library/{book_id}",response_model=BookOut,response_model_exclude_none=True)
def book(book_id:int):
    if book_id not in library_db:
        raise HTTPException(status_code=404,detail="id  not found")
    return library_db[book_id]

@app.post("/library",response_model=BookOut,response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
def new_book(book:BookIn):
    library_db[book.id]=book.model_dump()
    return library_db[book.id]

@app.delete("/library/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delet(book_id:int):
    if book_id not in library_db:
        raise HTTPException(status_code=404,detail="id  not found")
    del library_db[book_id]
    return

@app.put("/library/{book_id}", response_model=BookOut, response_model_exclude_none=True)
def update_book(book_id: int, book: BookIn):
    if book_id not in library_db:
        raise HTTPException(status_code=404, detail="id not found")
    library_db[book_id] = book.model_dump()
    return library_db[book_id]
