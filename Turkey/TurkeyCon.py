#!/bin/python
#-*-coding:utf-8-*-

from sqlalchemy import create_engine,or_,and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger,Text

engine = create_engine("postgresql+psycopg2://postgres:postgres@192.168.1.106:5432/postgres", echo=True)
DB_session = sessionmaker(bind = engine)
session = DB_session()
Base = declarative_base()


class Turkey(Base):

    __tablename__="citizen";

    uid = Column(BigInteger,primary_key=True)
    national_identifier = Column(Text)
    first = Column(Text)
    last = Column(Text)
    mother_first = Column(Text)
    father_first = Column(Text)
    gender = Column(String(1))
    birth_city = Column(Text)
    date_of_birth = Column(Text)
    id_registration_city = Column(Text)
    id_registration_district = Column(Text)
    address_city = Column(Text)
    address_district = Column(Text)
    address_neighborhood = Column(Text)
    street_address = Column(Text)
    door_or_entrance_number = Column(Text)
    misc = Column(Text)

def countTail(fun):
    def wrapper(*a):
        obj = fun(*a)
        obj.append(len(obj))
        return obj
    return wrapper
    

@countTail
def getAllbyName(fisrt="", last="", fuzzing = False, page=0):
    """
    Get uesr all informatino by name.
    :param name:
    :return:
    """
    if fuzzing!=True :
        trPeo = session.query(Turkey).filter(and_(Turkey.first==fisrt, Turkey.last==last)).order_by(Turkey.uid).offset(page*50).limit(50).all()
    else:
        trPeo = session.query(Turkey).filter(or_(Turkey.first.like(fisrt+"%"),Turkey.last.like(last+"%"))).\
            order_by(Turkey.uid).offset(page*50).limit(50).all()
    return trPeo

@countTail
def getAllbyFirst(first="", page=0):

    trPeo = session.query(Turkey).filter(Turkey.first==first).order_by(Turkey.first).offset(page*50).limit(50).all()
    return trPeo


@countTail
def getAllbyLast(last="", page=0):

    trPeo = session.query(Turkey).filter(Turkey.last==last).order_by(Turkey.last).offset(page*50).limit(50).all()
    return trPeo


@countTail
def getAllbyFirst_F(first="", page=0):

    trPeo = session.query(Turkey).filter(Turkey.first.like(first+"%")).order_by(Turkey.first).offset(page*50).limit(50).all()
    return trPeo


@countTail
def getAllbyLast_F(last="", page=0):

    trPeo = session.query(Turkey).filter(Turkey.last.like(last+"%")).order_by(Turkey.last).offset(page*50).limit(50).all()
    return trPeo

def sqlExec(sql):

    try:
        trPeo = session.execute(sql).fetchall()
    except Exception,e:
        return e
    return trPeo
