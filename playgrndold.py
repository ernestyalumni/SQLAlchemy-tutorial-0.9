# playgrnd.py
# following the examples in the 0.9 version of SQLAlchemy and its documentation
# Shout outs to Mike Bayer for SQLAlchemy and the SQLAlchemy documentation
# 20140620
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
# the purpose of this script is to play with SQLAlchemy and to test out code

import sqlalchemy

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:',echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, Numeric, DateTime
from datetime import datetime

class SetinSets( Base ):
    __tablename__ = 'Sets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)

    def __repr__(self):
        return "<Set(name='%s', description='%s')>" % ( self.name, self.desc )

#
# test code test data
#
Set0dic = { 'id' : 0 , 'name' : 'Set0' , 'desc' : 'Set 0 in Sets' }
Set1dic = { 'id' : 1 , 'name' : 'Set1' , 'desc' : 'Set 1 in Sets' }

Set0 = SetinSets
print type(Set0)  # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'> it's a Meta.  hmmm.
Set0 = SetinSets()
print type(Set0) # <class '__main__.SetinSets'>

# ok good, the following works
for key in Set0dic:
    setattr( Set0, key, Set0dic[key] )

Set1 = SetinSets()

for key in Set1dic:
    setattr( Set1, key, Set1dic[key] )

Set1

# Note that
Set2 = SetinSets
Set2.id = 2
print Set1.__table__ == Set2.__table__ # this means that the initialization manner by setattr is all good, does what we expect and keeps the Columns

# cf. http://stackoverflow.com/questions/6474549/error-with-dynamic-classes-and-sqlalchemy

# the definition for the function TblinSet immediately below isn't that great because it can only be used once to make a TblinSetcls and the only added benefit is the arbitrary tblname; see the warning below for Tbl1 = TblinSet( 'Tbl1' )
#
"""
def TblinSet( tblname ):
    class TblinSetcls( Base ):
        __tablename__ = tblname
        id      = Column(Integer, primary_key=True)
        created = Column(DateTime, default=datetime.utcnow())
        desc    = Column(String, nullable=True, unique=True) 
        name    = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "<Set(name='%s', description='%s')>" % ( self.name, self.desc )


    return TblinSetcls

Tbl0 = TblinSet( 'Tbl0' )
print type(Tbl0) # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>
dir(Tbl0)
# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__mapper__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__', '__tablename__', '__weakref__', '_decl_class_registry', '_sa_class_manager', 'created', 'desc', 'id', 'metadata']



Tbl0 = Tbl0()  # <__main__.TblinSetcls object at 0x10302ac50>
print type(Tbl0) # <class '__main__.TblinSetcls'>

Tbl0dic = { 'id' : 0 , 'name' : 'Tbl0' , 'desc' : 'Table 0 in Set', 'created' : datetime.utcnow() }
Tbl1dic = { 'id' : 1 , 'name' : 'Tbl1' , 'desc' : 'Table 1 in Set', 'created' : datetime.utcnow() }

#>>> Tbl1 = TblinSet( 'Tbl1' )
#/Library/Python/2.7/site-packages/SQLAlchemy-0.9.4-py2.7-macosx-10.9-intel.egg/sqlalchemy/ext/declarative/clsregistry.py:160: SAWarning: This declarative base already contains a class with the same class name and module name as __main__.TblinSetcls, and will be replaced in the string-lookup table.
# can only use once
"""

def Repr(self):
    return "<Tbl(id='%s', name='%s', description='%s')>" % ( self.id, self.name, self.desc )


# cf. https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA
# the necessity of this guy is that different tables might have completely different types and number of columns

""" 
def TblinSet( clsname, tblname ):
    """
#    TblinSet
#    -the necessity of this class is that different tables might have completely different types and number of columns

#    cf. https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA 
"""

    Tbl = type( clsname , (Base, ), {'__tablename__' : tblname , 
                                     'id'            : Column(Integer, primary_key=True) ,
                                     'created'       : Column(DateTime, default=datetime.utcnow()) ,
                                     'desc'          : Column(String, nullable=True, unique=True) ,
                                     'name'          : Column(String, nullable=False, unique=True) } )
    setattr(Tbl,"__repr__", classmethod(Repr) )

    return Tbl # or Tbl() ?
"""
Tbl0dic = { 'id' : 0 , 'name' : 'Tbl0' , 'desc' : 'Table 0 in Set', 'created' : datetime.utcnow() }
Tbl1dic = { 'id' : 1 , 'name' : 'Tbl1' , 'desc' : 'Table 1 in Set', 'created' : datetime.utcnow() }

"""
Tbl0 = TblinSet( 'Tbl0row', 'Tbl0' )
type( Tbl0 ) # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>

Tbl1 = TblinSet('Tbl1row', 'Tbl1' )
Tbl1 = Tbl1()  # this poses no problems now
type(Tbl1) # <class '__main__.Tbl1row'>
"""

tbldiceg = { '__tablename__' : 'Cool' , 
                                     'id'            : Column(Integer, primary_key=True) ,
                                     'created'       : Column(DateTime, default=datetime.utcnow()) ,
                                     'desc'          : Column(String, nullable=True, unique=True) ,
                                     'name'          : Column(String, nullable=False, unique=True) }
# tbldiceg - table dictionary eg example
del tbldiceg['__tablename__']

from copy import deepcopy

#
#
# EY : 20140620 SQLAlchemy usage warning 
# 
#

#tbldiceg1 = deepcopy( tbldiceg)

Tbldiceg = dict( { '__tablename__' : 'TblsinSets' } , **tbldiceg )
#Tbl1diceg = dict( { '__tablename__' : 'TblsinSets' } , **tbldiceg1 )

def TblinSet( clsname, dic  ):
    """
    TblinSet
    -the necessity of this class is that different tables might have completely different types and number of columns

    cf. https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA 
    """

    Tbl = type( clsname , (Base, ), dic )
#    setattr(Tbl,"__repr__", classmethod(Repr) )

    return Tbl # or Tbl() ?




def PutinSQLAlch( cls, dic ):
    for key in dic:
        setattr( cls, key, dic[key] )
    return cls


Tbl = TblinSet( 'Tblrow', Tbldiceg)
type(Tbl)  # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>


"""
#Tbl0 = PutinSQLAlch( Tbl0, Tbl0dic )
#print Tbl0.__repr__()

#Tbl1 = TblinSet( 'Tbl1row', Tbl1diceg)
#Tbl1 = PutinSQLAlch( Tbl1, Tbl1dic ) 
"""

setattr(Tbl,"__repr__", classmethod(Repr) )

# So it works
Tbl0 = Tbl()
Tbl0 = PutinSQLAlch( Tbl0, Tbl0dic)
Tbl1 = Tbl()
Tbl1 = PutinSQLAlch( Tbl1, Tbl1dic)





#>>> Tbl1 = TblinSet( "Tblrow"  , Tbl1diceg )
#/Library/Python/2.7/site-packages/SQLAlchemy-0.9.4-py2.7-macosx-10.9-intel.egg/sqlalchemy/ext/declarative/clsregistry.py:160: SAWarning: This declarative base already contains a class with the same class name and module name as __main__.Tblrow, and will be replaced in the string-lookup table.

# cf. 2.1.10 Building a Relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

#
# let's go from 1-to-many relationship
# 

# Now
print Set0.__tablename__
print Set1.__tablename__
# in SetinSets, each set can have many tables, even if the tables have different numbers of and different types of columns (distinct tables!)

toTbl0 = relationship("TblsinSets",backref="Sets")
toTbl1 = relationship("TblsinSets",backref="Sets")
setattr( Set0, 'toTbl0', toTbl0 )
setattr( Set0, 'toTbl1', toTbl1 )

setattr( Tbl0, 'set_id' , Column(Integer, ForeignKey( 'Sets.id' ) ) )
setattr( Tbl1, 'set_id' , Column(Integer, ForeignKey( 'Sets.id' ) ) )

#Tbl0 = PutinSQLAlch( Tbl0, Tbl0dic )
print Tbl0.__repr__()


#Tbl1 = PutinSQLAlch( Tbl1, Tbl1dic ) 
# So it works


#
# making another layer, another 1-to-many relationship
#
coldiceg = { 
                                     'series'            : Column(String, primary_key=True) ,
                                     'desc'          : Column(String, nullable=True, unique=True) ,
                                     'mul'          : Column(Integer, nullable=False, unique=False) }

coldiceg1 = deepcopy(coldiceg)


def coldicmkr( seriesname , coldiceg ): # column dictionary maker
    """
    coldicmkr - column dictionary maker

    this is another deeper layer, another 1-to-many relationship

    
    """
    
    coldiceg = dict( { '__tablename__' : seriesname }, **coldiceg )
    
    return TblinSet( seriesname, coldiceg )



Col00 = coldicmkr( "ColinTbl0", coldiceg )
#Col1 = coldicmkr( "ColinTbl0", coldiceg1 ) # it works

Col0 = Col00()
Col1 = Col00()
#
# sample data
Col0dic = { 'series' : 'Col0' , 'desc' : 'Column 0 in Table 0', 'mul' : 1 }
Col1dic = { 'series' : 'Col1' , 'desc' : 'Column 1 in Table 0', 'mul' : 1 }


Col0 = PutinSQLAlch( Col0, Col0dic )
Col1 = PutinSQLAlch( Col1, Col1dic )


toCol0 = relationship("ColinTbl0", backref="Tbl0")
toCol1 = relationship("ColinTbl0", backref="Tbl0")
setattr( Tbl0, 'toCol0', toCol0 )
setattr( Tbl0, 'toCol1', toCol1 )

setattr( Col0, 'tbl_id' , Column(String,ForeignKey( 'Tbl0.name' ) ) )
setattr( Col1, 'tbl_id' , Column(String,ForeignKey( 'Tbl0.name' ) ) )

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
session.commit()
