# promote_user.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User
from backend.role_service import RoleService

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def promote_to_manager(username):
    # Find the user
    user = session.query(User).filter(User.username == username).first()
    if not user:
        print(f"User '{username}' not found.")
        return

    # Find the Manager role
    role_service = RoleService(session)
    manager_role = role_service.get_role_by_name("Manager")
    if not manager_role:
        print("Manager role not found.")
        return

    # Update role
    user.role_id = manager_role.role_id
    session.commit()
    print(f"User '{username}' promoted to Manager!")

# Run the function
promote_to_manager("Kance")