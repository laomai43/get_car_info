from sqlalchemy import Column, String, create_engine, Integer, ForeignKey, Float, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    img = Column(String(200))
    url = Column(String(200))

    def __repr__(self):
        return "<Brand(name='%s', img='%s', url='%s')>" % (
            self.name, self.img, self.url)


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(String(20))
    img = Column(String(200))
    url = Column(String(200), unique=True)

    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', backref='my_series')

    def __repr__(self):
        return ','.join([self.NAME, self.img, self.url])


class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, unique=True )
    name = Column(String(20))
    sellingPrice = Column(Float)
    guidancePrice = Column(Float)
    batteryLife = Column(String(20))
    productionStatus = Column(String(20))
    belisted = Column(String(20))

    series_id = Column(Integer, ForeignKey('series.id'))
    series = relationship('Series', backref='my_models')

    def __repr__(self):
        return ','.join(
            [self.name, self.sellingPrice, self.guidancePrice, self.batteryLife, self.belisted, self.productionStatus])


# engine = create_engine('sqlite:///foo.db', echo=True)
engine = create_engine('mysql+mysqlconnector://root:my-secret-pw@localhost:32768/freecar', echo=True)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
