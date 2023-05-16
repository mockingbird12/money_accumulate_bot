from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///database.db")
Base = declarative_base()


class Saving(Base):
    __tablename__ = 'savings'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    saving_value = relationship("SavingValue")

    def __str__(self):
        return f"{self.name} {self.saving_value}"


class SavingValue(Base):
    __tablename__ = 'saving_value'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    saving_id = Column(Integer, ForeignKey("savings.id"))

    def __str__(self):
        return f"{self.value}"


Base.metadata.create_all(engine)
session = Session(engine)

def create_savings(name:str):
    saving = Saving(name=name)
    session.add(saving)
    session.commit()

def set_saving_value(saving_name: str, value:int):
    saving = get_savings(saving_name)
    saving_value = SavingValue(value=value, saving_id = saving.id)
    session.add(saving_value)
    session.commit()

def get_saving_value(saving_name: str):
    return session.query(Saving).filter(Saving.name==saving_name).one().saving_value

def get_savings(saving_name:str=None)->[]:
    if saving_name == None:
        return session.query(Saving).all()
    else:
        return session.query(Saving).filter(Saving.name==saving_name).one()


if __name__ == '__main__':
    # create_savings('Портфель Открытие')
    # create_savings('Портфель Тинькоф')
    # create_savings('Наличные')
    # create_savings('Jetlend')
    # set_saving_value('Наличные', 1000)
    print(get_savings('Jetlend'))
    [print(i) for i in get_savings()]
    print (get_saving_value('Наличные'))

