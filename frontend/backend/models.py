from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

# ====== Association Tables ======
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.role_id')),
    Column('permission_id', Integer, ForeignKey('permissions.permission_id'))
)

# ====== Existing Models ======
class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    cinemas = relationship('Cinema', back_populates='city')

class Cinema(Base):
    __tablename__ = 'cinemas'
    cinema_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200))
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    city = relationship('City', back_populates='cinemas')
    users = relationship('User', back_populates='cinema')

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', back_populates='role')
    permissions = relationship(
        'Permission', 
        secondary=role_permission, 
        back_populates='roles'
    )

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), nullable=True)
    role = relationship('Role', back_populates='users')
    cinema = relationship('Cinema', back_populates='users')

# ====== Permission Models ======
class Permission(Base):
    __tablename__ = 'permissions'
    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    roles = relationship(
        'Role', 
        secondary=role_permission, 
        back_populates='permissions'
    )
