from fastapi import FastAPI, HTTPException
from sqladmin import Admin, ModelView
from sqlalchemy import select
from starlette import status

import settings
from app.core.dependencies import get_context_db
from app.db.models import Organization, AdminUser
from app.db.models.admin import AdminPanel
from app.db.session import engine, async_session

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with get_context_db() as db:
            admin = await db.execute(
                select(AdminPanel).filter(AdminPanel.username == username)
            )

            admin = admin.scalar_one_or_none()

            if admin and admin.check_password(password):
                request.session.update({"user": admin.username})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        async with get_context_db() as db:
            admin = await db.execute(
                select(AdminPanel).filter(AdminPanel.username == user)
            )
            admin = admin.scalar_one_or_none()
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )

            return admin


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)


class BaseModelView(ModelView):
    is_async = True
    page_size = 100
    page_size_options = [100, 500, 1000]
    save_as = True


class PanelUsers(BaseModelView, model=AdminPanel):
    category = "Panel"
    column_list = [AdminPanel.id, AdminPanel.username]


class OrganizationAdmin(BaseModelView, model=Organization):
    category = "Organization"
    column_list = [
        Organization.id,
        Organization.name,
        Organization.password,
        Organization.host_name,
        Organization.port,
    ]
    order_by = [Organization.name.desc()]
    column_sortable_list = [
        Organization.name,
    ]
    column_searchable_list = [
        Organization.name,
    ]


class AdminUsers(BaseModelView, model=AdminUser):
    category = "Admin Users"
    column_list = [AdminUser.id, AdminUser.email, AdminUser.password]
    order_by = [AdminUser.email.desc()]
    column_sortable_list = [
        AdminUser.email,
    ]
    column_searchable_list = [
        AdminUser.email,
    ]


def init_admin(app: FastAPI):
    admin = Admin(
        app=app,
        engine=engine,
        session_maker=async_session,
        base_url="/tenantflow/admin",
        title="TenantFlow Admin",
        authentication_backend=authentication_backend,
    )

    admin.add_view(PanelUsers)
    admin.add_view(OrganizationAdmin)
    admin.add_view(AdminUsers)
