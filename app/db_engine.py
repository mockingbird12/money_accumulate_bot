from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from datetime import datetime


engine = create_engine("sqlite:///database.db")
Base = declarative_base()


class Assert(Base):
    """"
    Класс активов
    """
    __tablename__ = 'assert'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    assert_value = relationship("AccountingAssert")

    def __str__(self):
        # return f"{self.name} {self.saving_value[-1].value}"
        return f"{self.name}"


class AccountingAssert(Base):
    """"
    Класс учета активов
    """
    __tablename__ = 'accounting_assert'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    saving_id = Column(Integer, ForeignKey("assert.id"))
    currency_id = Column(Integer, ForeignKey("currency.id"))
    update_time = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"{self.id} {self.value} {self.update_time}"

class Currency(Base):
    """"
    Класс валют
    """
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    accounting_assert_id = relationship("AccountingAssert")

    def __str__(self):
        return f"{self.id} {self.name}"


Base.metadata.create_all(engine)

class DB_driver():

    def __init__(self):
        self.session = Session(engine)

    def create_assert(self, name:str):
        saving = Assert(name=name)
        self.session.add(saving)
        self.session.commit()

    def set_assert_value(self, assert_name: str, value:int):
        assert_unit = self.get_asserts(assert_name)
        assert_value = AccountingAssert(value=value, saving_id = assert_unit.id)
        self.session.add(assert_value)
        self.session.commit()

    def get_assert_value(self, assert_name: str):
        assert_unit = self.session.query(Assert).filter(Assert.name==assert_name).one()
        print(type(assert_unit.assert_value))
        print([i for i in assert_unit.assert_value])
        if assert_unit.assert_value:
            return assert_unit.assert_value[-1].value
        else:
            return 0

    def get_asserts(self, assert_name:str=None)->[]:
        if assert_name == None:
            return self.session.query(Assert).all()
        else:
            return self.session.query(Assert).filter(Assert.name == assert_name).one()

    def get_asserts_value(self)->[]:
        return self.session.query(AccountingAssert).all()

    def delete_assert(self, assert_name:str)->True:
        delete_item = self.session.query(Assert).filter(Assert.name == assert_name).one()
        self.session.delete(delete_item)
        self.session.commit()
        return True

    def create_currency(self, currency_name:str)->None:
        currency = Currency(name=currency_name)
        self.session.add(currency)
        self.session.commit()

    def get_all_currency(self)->[]:
        res = self.session.query(Currency).all()
        return res


if __name__ == '__main__':
    db_test = DB_driver()
    db_test.create_currency('USD')
    db_test.create_currency('RUB')
    for i in db_test.get_all_currency():
        print(i.name)
    # set_saving_value('Наличные', 1000)
    # print(get_savings('Jetlend'))
    [print(i) for i in db_test.get_asserts_value()]
    # print(get_saving_value('Наличные'))
    # [print(i) for i in get_savings_value()]

