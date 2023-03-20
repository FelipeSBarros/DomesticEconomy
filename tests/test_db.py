import pytest
from sqlalchemy.exc import IntegrityError

from models import Action, Subcategory, General


class TestDB:
    def test_action_valid(self, db_session, valid_income_action):
        income = db_session.query(Action).first()
        assert income.name == "Income"

    @pytest.mark.xfail(raises=IntegrityError)
    def test_subcategory_wout_category(self, db_session):
        subcat = Subcategory(name="Missing category")
        db_session.add(subcat)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

    # todo add teste para income
    # def test_general_income_creation(
    #     self, db_session, valid_income_action, valid_user, valid_subcategory
    # ):
    #     income = General(
    #         action_id=valid_income_action.id,
    #         user=valid_user.id,
    #         value=9000,
    #     )
    #     db_session.add(income)
    #     db_session.commit()
    #     exist_registry = db_session.query(General).filter_by(action_id=valid_income_action.id)
    #     assert exist_registry

    def test_general_expenses_creation(
        self, db_session, valid_expenses_action, valid_user, valid_subcategory
    ):
        general = General(
            action_id=valid_expenses_action.id,
            user=valid_user.id,
            category=valid_subcategory.category_id,
            subcategory=valid_subcategory.id,
            value=9000,
        )
        db_session.add(general)
        db_session.commit()
        exist_registry = db_session.query(General).first()
        assert exist_registry
