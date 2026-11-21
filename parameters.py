from fastapi import FastAPI,HTTPException
from enum import Enum
from fastapi import Query
app=FastAPI()

#problem 1 
@app.get("/health")
def health():
    return {"status":"ok"}
@app.get("/courses")
def course():
    return ["maths","physics","chemistry"]

#problem 2 
@app.get("/courses/top")
def top():
    return {"top_course":"python"}
@app.get("/courses/{course_id}")
def course_get(course_id:int):
    return {"course_id":course_id,"enrolled":True}

#problem 3
@app.get("/greet/{name}")
def greeting(name:str):
    return {"message":f"welcome {name}"}

#problem 4
@app.get("/students/{students_id}/subjects/{subject}/marks/{marks}")
def stu(students_id:int,subject:str,marks:int):
    return {"student_id":students_id,"subject":subject,"marks":marks}

#problem 5 mini data lookup
courses_db={
    1:{"name":"calculus","credits":4},
    2:{"name":"physics","credits":3},
    3:{"name":"python","credits":4},
}
@app.get("/db/courses/{course_id}")
def mini(course_id:int):
    if course_id in courses_db:
        return {"course_id":course_id,"data":courses_db[course_id]}
    else:
        return {"error":"course not found"}

    
#problem 11 combining path+query parameters
@app.get("/db/courses/{course_id}/details")
def combine(course_id:int,include_credits:bool=False):
    if course_id not in courses_db:
        raise HTTPException(404)
    if include_credits==True:
        return courses_db[course_id]
    else:
        return {"name":courses_db[course_id]["name"]}


#problem 6 specific field lookup with real 404
@app.get("/db/courses/{course_id}/{field}")
def get_course_field(course_id:int,field:str):
    if course_id not in courses_db:
        raise HTTPException(404) 
    if field not in courses_db[course_id]:
        raise HTTPException(404) 
    return {field:courses_db[course_id][field]}

#problem 7 predefined choices with Enum
class Department(str,Enum):
    cs="cs"
    math="math"
    physics="physics"
@app.get("/departments/{dept}")
def get_departments(dept:Department):
    if dept==Department.cs:
        return {"building":"A"}
    elif dept==Department.math:
        return {"building":"B"}
    else :
        return {"building":"C"}

#problem 8 basic search endpoint
@app.get("/search")
def query(q:str,limit:int=5):
    return {"query":q,"limit":limit}

#problem 9 pagination with skip and limit
items=["apple","banana","cherry","date","elderberry","fig","grape"]
@app.get("/items")
def paginate(skip:int=0,limit:int=3):
    return {"items":items[skip:skip+limit]}

#problem 10 optional filtering with None
@app.get("/filter-items")
def filter(contains:str|None=None):
    if contains:
        return [item for item in items if contains in item]
    else:
        return items

#problem 12 validated search with Query()
@app.get("/books/search")
def book(keyword:str=Query(min_length=2,max_length=15),max_price:int=Query(default=500,ge=50,le=2000)):
    return {"keyword":keyword,"max_price":max_price}

#problem 13 multiple values with list[str]
@app.get("/books/filter")
def tag(tags:list[str] |None=Query(default=None)):
    if tags:
        return {"count":len(tags),"tags":tags}
    else:
        return {"count":0,"tags":[]}

#problem 14 student report generator
students_db={
    1:{"name":"Aarav","marks":78,"grade":"B"},
    2:{"name":"diya","marks":92,"grade":"A"},
    3:{"name":"kabir","marks":78,"grade":"C"},
}
@app.get("/students_db/{students_id}/report")
def report(students_id:int,bonus_marks:int=Query(default=0,ge=0,le=20),include_grades:bool=False):
    if students_id not in students_db:
        raise HTTPException(404)
    final_marks=students_db[students_id]["marks"]+bonus_marks
    if final_marks>100:
        final_marks=100
    if include_grades==True:
        return {"name":students_db[students_id]["name"],"final_marks":final_marks,"grades":students_db[students_id]["grade"]}
    else:
        return {"name":students_db[students_id]["name"],"final_marks":final_marks}