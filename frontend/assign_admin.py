# assign_admin.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import User, Role
from backend.user_service import UserService

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def promote_to_admin(username):
    # Get user and admin role
    user = session.query(User).filter(User.username == username).first()
    admin_role = session.query(Role).filter(Role.name == "Admin").first()

    if not user:
        print(f"User '{username}' not found!")
        return

    if not admin_role:
        print("Admin role does not exist!")
        return

    # Update role
    user.role_id = admin_role.role_id
    session.commit()
    print(f"User '{username}' promoted to Admin!")

if __name__ == "__main__":
    promote_to_admin("Kance")  # Replace with target username
    session.close()