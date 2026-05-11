from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

def get_todos(db: Session):
    return db.query(models.Todo).all()