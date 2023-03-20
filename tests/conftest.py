import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
)

from models import Base, Action, Category, Subcategory, User

# load_dotenv()
# DB_NAME = os.getenv("DB_NAME")
engine = create_engine(f"sqlite://", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def valid_income_action(db_session):
    income_action = Action(name="Income")
    db_session.add(income_action)
    db_session.commit()
    return income_action


@pytest.fixture(scope="module")
def valid_expenses_action(db_session):
    expenses_action = Action(name="Expenses")
    db_session.add(expenses_action)
    db_session.commit()
    return expenses_action


@pytest.fixture(scope="module")
def valid_user(db_session):
    user = User(name="Felipe", chat_id="F3l1p3")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="module")
def valid_category(db_session):
    cat = Category(name="Transporte")
    db_session.add(cat)
    db_session.commit()
    return cat


@pytest.fixture(scope="module")
def valid_subcategory(db_session, valid_category):
    subcat = Subcategory(name="gasolina", category_id=valid_category.id)
    db_session.add(subcat)
    db_session.commit()
    return subcat
