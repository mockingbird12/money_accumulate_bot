from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///database.db")
Base = declarative_base()


class Saving(Base):
    __tablename__ = 'savings'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    saving_value = relationship("SavingValue")

    def __str__(self):
        # return f"{self.name} {self.saving_value[-1].value}"
        return f"{self.name}"


class SavingValue(Base):
    __tablename__ = 'saving_value'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    saving_id = Column(Integer, ForeignKey("savings.id"))

    def __str__(self):
        return f"{self.id} {self.value}"


Base.metadata.create_all(engine)

class DB_driver():

    def __init__(self):
        self.session = Session(engine)

    def create_savings(self, name:str):
        saving = Saving(name=name)
        self.session.add(saving)
        self.session.commit()


    def set_saving_value(self, saving_name: str, value:int):
        saving = self.get_savings(saving_name)
        saving_value = SavingValue(value=value, saving_id = saving.id)
        self.session.add(saving_value)
        self.session.commit()


    def get_saving_value(self, saving_name: str):
        saving = self.session.query(Saving).filter(Saving.name==saving_name).one()
        print(type(saving.saving_value))
        print([i for i in saving.saving_value])
        if saving.saving_value:
            return saving.saving_value[-1].value
        else:
            return 0


    def get_savings(self, saving_name:str=None)->[]:
        if saving_name == None:
            return self.session.query(Saving).all()
        else:
            return self.session.query(Saving).filter(Saving.name==saving_name).one()

    def get_savings_value(self)->[]:
        return self.session.query(SavingValue).all()

    def delete_saving(self, saving_name:str)->True:
        delete_item = self.session.query(Saving).filter(Saving.name==saving_name).one()
        self.session.delete(delete_item)
        self.session.commit()
        return True


if __name__ == '__main__':
    db_test = DB_driver()
    # create_savings('Портфель Открытие')
    # create_savings('Портфель Тинькоф')
    # create_savings('Наличные')
    # create_savings('Jetlend')
    db_test.set_saving_value('портфель открытие', 1000)
    for i in db_test.get_savings():
        print(i.name)
        print(db_test.get_saving_value(i.name))
    # set_saving_value('Наличные', 1000)
    # print(get_savings('Jetlend'))
    [print(i) for i in db_test.get_savings_value()]
    # print(get_saving_value('Наличные'))
    # [print(i) for i in get_savings_value()]

