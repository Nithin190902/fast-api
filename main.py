from fastapi import FastAPI, Depends, HTTPException
from models import Todo
from schemas import TodoCreate, TodoInDB
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Todo

Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependency for db 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# post request
@app.post("/todos/", response_model=TodoInDB)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# get all todos
@app.get("/todos/", response_model=list[TodoInDB])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

# get todo by id
@app.get("/todos/{todo_id}", response_model=TodoInDB)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# update todo by id
@app.put("/todos/{todo_id}", response_model=TodoInDB)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

# delete todo by id
@app.delete("/todos/{todo_id}", response_model=TodoInDB)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo