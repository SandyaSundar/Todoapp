from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# POST - create todo
@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
	db_todo = Todo(**todo.dict())
	db.add(db_todo)
	db.commit()
	db.refresh(db_todo)
	return db_todo

# get All todos
@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
	return db.query(Todo).all()

# get single todo
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
	todo = db.query(Todo).filter(Todo.id == todo_id).first()
	if not todo:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

	return todo


# PUT - update todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated: TodoCreate, db: Session = Depends(get_db)):
	todo = db.query(Todo).filter(Todo.id == todo_id).first()
	if not todo:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

	for key, value in updated.dict().items():
		setattr(todo, key, value)

	db.commit()
	db.refresh(todo)
	return todo

# DELETE - delete todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
	todo = db.query(Todo).filter(Todo.id == todo_id).first()
	if not todo:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

	db.delete(todo)
	db.commit()
	return None
