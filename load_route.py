from app.auth.routers import router as AuthRouter
from app.user.routers import router as UsersRouter
from app.books.routers import router as BooksRouter
from app.welcome.router import router as WelcomeRouter

ROUTE_LIST = [
    {"route": AuthRouter, "tags": ["Xác Thực"], "prefix": ""},
    {"route": WelcomeRouter, "tags": ["Welcome"], "prefix": "/api"},
    {"route": UsersRouter, "tags": ["Users"], "prefix": "/user"},
    {"route": BooksRouter, "tags": ["Books"], "prefix": "/books"},
]