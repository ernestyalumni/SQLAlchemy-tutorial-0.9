# egmoviedyn.py
# following the examples in the 0.9 version of SQLAlchemy and its documentation
# based on here https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA
# Shout outs to Mike Bayer for SQLAlchemy and the SQLAlchemy documentation
# 20140616
# 
# Fund Science! & Help Ernest finish his Physics Research! : quantum super-A-polynomials - Ernest Yeung
#                                               
# http://igg.me/at/ernestyalumni2014                                                                             
#                                                              
# Facebook     : ernestyalumni  
# github       : ernestyalumni                                                                     
# gmail        : ernestyalumni                                                                     
# linkedin     : ernestyalumni                                                                             
# tumblr       : ernestyalumni                                                               
# twitter      : ernestyalumni                                                             
# youtube      : ernestyalumni                                                                
# indiegogo    : ernestyalumni                                                                        
# 
# Ernest Yeung was supported by Mr. and Mrs. C.W. Yeung, Prof. Robert A. Rosenstone, Michael Drown, Arvid Kingl, Mr. and Mrs. Valerie Cheng, and the Foundation for Polish Sciences, Warsaw University.  
#
# make sure you have SQLalchemy installed on your admin or at least have that PYTHONPATH set to include SQLalchemy
#
#
# from Lars

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

def Init(self, title=None, year=None):
    self.title = title
    self.year = year
def Repr(self):
    return "Movie(%r, %r, %r)" % (self.title, self.year, self.director)

Movie = type("Movie", (Base,),{'__tablename__': "movies", 
                               "__init__": Init
                               "id": Column(Integer, primary_key=True), "title": Column(String(255), nullable=False), "year":Column(Integer), "directed_by": Column(Integer, ForeignKey('directors.id')), "director": relation("Director", backref='movies', lazy=False) } )

#setattr( Movie, "__init__", classmethod(Init))  # your __init__ monkeypatch is interfering with SQLA's wrapping of this method.


setattr( Movie, "__repr__", classmethod(Repr))

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    def __init__(self,name=None):
        self.name = name

    def __repr__(self):
        return "Director(%r)" % (self.name)

engine = create_engine('sqlite:///meta.db', echo=True)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session=Session()

    m1 = Movie("Star Trek", 2009)
    m1.director = Director("JJ Abrams")

    d2 = Director("George Lucas")
    d2.movies = [Movie("Star Wars", 1977), Movie("THX 1138", 1971) ]

    try:
        session.add(m1)
        session.add(d2)
        session.commit()
    except:
        session.rollback()

    alldata = session.query(Movie).all()
    for somedata in alldata:
        print somedata





