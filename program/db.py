from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.orm import Session

# Note: To use sqlalchemy library you need to download it --> pip install sqlalchemy pymysql

DATABASE_URL = "mysql+pymysql://MickelUWE:g<bI1Z11iC]c@localhost:3306/cinema"
engine = create_engine(DATABASE_URL, echo = True) # Initialises connection to the existing database, echo=True enables debugging (Printing out all queries it executes).
SessionLocal = sessionmaker(bind=engine) # Creates database sessions
Base = declarative_base() # Base class for models

def test_db_connection():
    """
    Attempts to connect to the database and prints the status

    Args:
        None
    Returns:
        None
    Raises:
        Exception: If an unexpected error occurs.
    """
    try:
        with engine.connect() as connection: # engine.connect() opens a direct connection to the database, "with" automatically closes connection after execution.
            print("✅ Successfully connected to the database!")
    except Exception as e:
            print("❌ Error:", e)

# User model (Table):
class User(Base):
    """
    
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key = True) # Unique identifier for the user.
    username = Column(String, unique = True, nullable = False) # Username must be unique, and must not be null.
    password = Column(String, nullable = False) # We should hash it.
    firstname = Column(String, nullable = False) # First name of the user.
    lastname = Column(String, nullable = False) # Last name of the user.
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable = False) # Foreign key linking to the Role table.
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id')) #link to a cinema, if the user works at one.

    # Relationship to the Role table
    role = relationship('Role', back_populates='users') # back_populates will cause changes to both sides, for example if you add a new User and assign them a Role, both the User's role and the Role's users attributes in the different tables will be updated automatically.

    def __repr__(self):
        """"""
        return f"<User(username={self.username}, firstname={self.firstname}, lastname={self.lastname})>"
 
# Role model (Table):
class Role(Base):
    """
    """
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key = True) # Unique identifier for the role.
    name = Column(String, unique = True, nullable = False) # The name of the role (e.g., Admin, Staff).
    permissions = Column(String) # Comma-separated string or JSON representing role permissions.

    # Relationship to the User table (a role can have many users)
    users = relationship('User', back_populates='role') # Basically creates a users attribute 

    def __repr__(self):
        return f"<Role(name={self.name}, permissions={self.permissions})>"

# UserService:
class UserService:
    """
    UserService handles operations related to users and roles.
    """
    def __init__(self, session: Session):
        """"""
        self.session = session
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate a user based on the username and password."""
        user = self.get_by_username(username)
        if user and user.password == password: # I need to improve this for password safety.
            return True
        return False
    
    def create_user(self, username: str, password: str, firstname: str, lastname: str, role_id: int, cinema: 'Cinema') -> 'User':
        """Create a new user and assign them a role and cinema."""
        role = self.get_role_by_id(role_id)
        if role:
            user = User(username = username, password = password, firstname = firstname, lastname = lastname, role_id = role.role_id, cinema_id = cinema.cinema_id)
            self.session.add(user)
            self.session.commit()
            return user
        return None
    def get_by_username(self, username: str) -> 'User':
        """Retrieve a user by their username."""
        return self.session.query(User).filter_by(username = username).first() 
    def get_role_by_id(self, role_id: int) -> 'Role':
        """Get a role by its ID."""
        return self.session.query(Role).filter_by(role_id = role_id).first()
    




# Cinema model (Table):
class Cinema(Base):
    """
    Represents a Cinema model, which maps to the 'cinema' table in the database.

    Attributes:
        cinema_id (int): The unique identifier for the cinema.
        city_id (int): The ID representing the city where the cinema is located.
        name (str): The name of the cinema.
        address (str): The address of the cinema.
        films (list): A collection of CinemaFilm objects associated with the cinema.
        screens (list): A collection of CinemaScreen objects associated with the cinema.
        screenings (list): A collection of CinemaScreening objects associated with the cinema.
        staff (list): A list of User objects representing staff members at the cinema.

    Methods:
        get_id(): Returns the unique ID of the cinema.
        get_name(): Returns the name of the cinema.
        get_address(): Returns the address of the cinema.
        get_admin(): Returns the admin (User object) of the cinema.
        get_staff(): Returns a list of staff members (User objects) associated with the cinema.
        set_name(name): Sets the name of the cinema.
        set_address(address): Sets the address of the cinema.
    """
    __tablename__ = "cinemas" # This matches the table name.

    cinema_id = Column(Integer, primary_key = True) # Makes a column of id, making it a primary key and type integer.
    city_id = Column(Integer, ForeignKey('city.city_id'), nullable = False) # City ID references the City table.
    name = Column(String, nullable = False) # name shouldnt be nullable, so its mandatory.
    address = Column(String, nullable = False)

    # Relationships (films, screens, and screenings will still have relationships to other tables)
    films = relationship('CinemaFilm', backref = 'cinema') # backref allows us to reference tables both way , so reference cinema from CinemaFilm.
    screens = relationship('CinemaScreen', backref='cinema')
    screenings = relationship('CinemaScreening', backref='cinema')

    # One-to-many relationship with staff (each cinema has many users as staff)
    staff = relationship('User', backref='cinema', foreign_keys=['User.cinema_id'] ) # Each user can work in one cinema


    def __init__(self, name, address, city_id ): # Initialise Cinema instance with following attributes:
        """
        Initialises a Cinema instance with the following attributes:

        Args:
            - name(str): The name of the cinema.
            - address(str): The address of the cinema.
            - city_id(int): The ID representing where the cinema is located.
        
        This constructor sets up the cinema with the provided details, and links the cinema to a specific city and admin user.
        """
        self.name = name
        self.address = address
        self.city_id = city_id

    def get_id(self):
        """Return the cinema ID."""
        return self.cinema_id
    def get_name(self):
        """Return the cinema name."""
        return self.name
    def get_address(self):
        """Return the cinema address."""
        return self.address
    def get_staff(self):
        """Return the list of staff (User objects) for the cinema."""
        return self.staff
    def set_name(self, name):
        """Sets the name of the class."""
        self.name = name
    def set_address(self, address):
        """Sets the address of the class."""
        self.address = address

j