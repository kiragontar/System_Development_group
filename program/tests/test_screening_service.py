import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.screening_service import ScreeningService
from models import Screening, Screen, Film
from datetime import datetime
