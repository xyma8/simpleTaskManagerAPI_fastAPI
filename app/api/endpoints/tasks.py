from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..schemas.task import TaskCreate, TaskResponse
from ...core.security import get_current_user
from ...core.websocket import broadcast
from ...db.dependencies import get_db
from ...db.models import Task, User

router = APIRouter()

# Эндпойнты задач


@router.post(
    "/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id,
        is_completed=False,
        created_at=datetime.utcnow(),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    await broadcast(f"New task created: {new_task.title}")
    return new_task


@router.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_update.title
    task.description = task_update.description
    db.commit()
    await broadcast(f"Task updated: {task.title}")
    return task


@router.delete("/tasks/{task_id}", response_model=TaskResponse)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    await broadcast(f"Task deleted: {task.id}")
    return {"detail": "Task deleted successfully"}
