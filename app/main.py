from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime

from .api.db.database import engine, Base
from .api.v1.routes.users import router as user_router
from .api.v1.routes.projects import router as project_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SoloPublicly"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/api/v1")
app.include_router(project_router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "auth/register.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "auth/login.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/verify-email", response_class=HTMLResponse)
async def verify_email_page(request: Request, token: str):
    return templates.TemplateResponse(
        "auth/verify_email.html", 
        {"request": request, "token": token, "year": datetime.now().year}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/projects/create", response_class=HTMLResponse)
async def create_project(request: Request):
    return templates.TemplateResponse(
        "projects/create_project.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/projects/edit/{project_id}", response_class=HTMLResponse)
async def edit_project(request: Request, project_id: str):
    return templates.TemplateResponse(
        "projects/edit_project.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/projects/view/{project_id}", response_class=HTMLResponse)
async def view_project(request: Request, project_id: str):
    return templates.TemplateResponse(
        "projects/view_project.html", 
        {"request": request, "year": datetime.now().year}
    )

@app.get("/projects/public/{slug}", response_class=HTMLResponse)
async def public_project(request: Request, slug: str):
    return templates.TemplateResponse(
        "projects/public_project.html", 
        {"request": request, "year": datetime.now().year}
    )