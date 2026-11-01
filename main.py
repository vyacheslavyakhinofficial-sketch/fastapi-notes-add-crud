import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


tasks: list[Tasks] = []


class Tasks(BaseModel):
    id: str
    title: str
    completed: bool


class TasksCreate(BaseModel):
    title: str


class TasksUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


@app.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TasksCreate):
    new_task = Tasks(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_tasks(task_id: str, payload: TasksUpdate):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)




categories: list[Categories] = []


class Categories(BaseModel):
    id: str
    name: str
    completed: bool


class CategoriesCreate(BaseModel):
    name: str


class CategoriesUpdate(BaseModel):
    name: str | None = None
    completed: bool | None = None


@app.get("/categories", status_code=status.HTTP_200_OK)
def get_categories():
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoriesCreate):
    new_category = Categories(id=str(uuid4()), name=payload.name, completed=False)
    categories.append(new_category)
    return new_category


@app.patch("/categories/{categories_id}", status_code=status.HTTP_200_OK)
def update_categories(categories_id: str, payload: CategoriesUpdate):
    for category in categories:
        if category.id == categories_id:
            if payload.name:
                category.name = payload.name
        if category is None:
            raise HTTPException(status_code=404, detail="category not found")


@app.delete("/categories/{categories_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(categories_id: str):
    for category in categories:
        if category.id == categories_id:
            categories.remove(category)
        if category is None:
            raise HTTPException(status_code=404, detail="category not found")



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)