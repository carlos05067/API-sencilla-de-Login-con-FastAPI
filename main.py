from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI()
engine = create_engine("sqlite:///./database.db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str

class LoginRequest(SQLModel):
    username: str
    password: str

@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        if not s.exec(select(User).where(User.username == "admin")).first():
            s.add(User(username="admin", password="admin"))
            s.add(User(username="user", password="user"))
            s.add(User(username="guest", password="guest"))
            s.commit()

@app.post("/login")
def login(data: LoginRequest):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == data.username)).first()
        if not user or user.password != data.password:
            raise HTTPException(401, "Usuario o contraseña incorrectos")
        return {"message": "Login exitoso", "username": user.username}