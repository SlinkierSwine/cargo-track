from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqladmin.authentication import AuthenticationBackend
from pathlib import Path


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        # Для простоты тестирования, принимаем только admin/admin
        if username == "admin" and password == "admin":
            # Сохраняем информацию о пользователе в сессии
            request.session.update({"user_id": "admin", "role": "admin"})
            return True
        
        return False

    async def login_page(self, request: Request) -> HTMLResponse:
        # Читаем HTML шаблон
        template_path = Path(__file__).parent.parent / "templates" / "admin_login.html"
        with open(template_path, "r") as f:
            html_content = f.read()
        
        return HTMLResponse(content=html_content)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[bool]:
        # Проверяем, есть ли пользователь в сессии
        user_id = request.session.get("user_id")
        user_role = request.session.get("role")
        
        if not user_id or user_role != "admin":
            return False
        
        return True


def get_admin_auth() -> AdminAuth:
    return AdminAuth(secret_key="orders-admin-secret-key-change-in-production") 