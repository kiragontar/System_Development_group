from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String, Table, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship 

Base = declarative_base()

# Association table for the many-to-many relationship between Role and Permission
role_permission_association = Table(
    'role_permission_association',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.role_id')),
    Column('permission_id', Integer, ForeignKey('permissions.permission_id'))
)




from .booking import Booking
from .cinema import Cinema
from .city import City
from .film import Film
from .permissions import Permission
from .role import Role
from .screen import Screen
from .screening import Screening
from .seat import Seat
from .ticket import Ticket
from .user import User
from .seat_availability import SeatAvailability

# How "from .user import User" works? : a file "user.py" is a module named "user", a package is a folder that contains these modules and it becomes a package when an __init__.py is made.

# Purpose of importing all these "."class" import class " into the models/__init__.py is to make them available when you import the models package 

# Note: To use sqlalchemy library you need to download it --> pip install sqlalchemy pymysql


