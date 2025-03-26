# init_admin.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Role, User
import bcrypt

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_roles():
    # Create default roles
    roles = [
        Role(name="Admin", role_id=1),
        Role(name="User", role_id=2),
        Role(name="Manager", role_id=3)
    ]
    
    for role in roles:
        if not session.query(Role).filter_by(name=role.name).first():
            session.add(role)
    session.commit()

def create_admin_user():
    # Create admin user if doesn't exist
    admin_role = session.query(Role).filter_by(name="Admin").first()
    
    if not admin_role:
        print("Admin role not found!")
        return

    if not session.query(User).filter_by(username="admin").first():
        hashed_pw = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        admin_user = User(
            username="admin",
            password=hashed_pw.decode('utf-8'),
            firstname="Admin",
            lastname="User",
            role_id=admin_role.role_id
        )
        session.add(admin_user)
        session.commit()

if __name__ == "__main__":
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        
        # Initialize roles
        init_roles()
        print("Created default roles")
        
        # Create admin user
        create_admin_user()
        print("Created admin user (username: 'admin', password: 'Admin123!')")
        
    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        session.rollback()
    finally:
        session.close()