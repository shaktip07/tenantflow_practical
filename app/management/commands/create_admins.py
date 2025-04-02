from sqlalchemy import select

from app.core.dependencies import get_context_db


async def main():
    try:
        from app.db.models.admin import AdminPanel

        async with get_context_db() as session:
            admins = await session.execute(
                select(AdminPanel).filter(AdminPanel.username == "admin")
            )
            if admins.scalar():
                print("Admin already exists")
                return
            admin = AdminPanel(username="admin", password="Admin@5678")
            session.add(admin)
            await session.commit()
            print("Admin created")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
