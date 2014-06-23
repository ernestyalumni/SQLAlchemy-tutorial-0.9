# playgrnd2.py
# following the examples in the 0.9 version of SQLAlchemy and its documentation
# Shout outs to Mike Bayer for SQLAlchemy and the SQLAlchemy documentation
# Based on playgrnd.py but I have to get the querying right
# 20140623
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

#
#
# the below are from my own package, doSQL
#
#

def PutinSQLAlch( cls, dic ):
    """
    PutinSQLAlch - Put into SQLAlch puts in the dic, that gives the values to populate the columns for a row

    e.g. for usage, try 

    Tbl = TblinSet( 'Tblrow', Tbldiceg)
    type(Tbl)  # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>

    Tbl0dic = { 'id' : 0 , 'name' : 'Tbl0' , 'desc' : 'Table 0 in Set', 'created' : datetime.utcnow() }
    Tbl1dic = { 'id' : 1 , 'name' : 'Tbl1' , 'desc' : 'Table 1 in Set', 'created' : datetime.utcnow() }

    # So it works
    Tbl0 = Tbl()
    Tbl0 = PutinSQLAlch( Tbl0, Tbl0dic)
    Tbl1 = Tbl()
    Tbl1 = PutinSQLAlch( Tbl1, Tbl1dic)

    """

    for key in dic:
        setattr( cls, key, dic[key] )
    return cls


# cf. 2.1.10 Building a Relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

#
# let's go from 1-to-many relationship
# 


def build1tomany( Parent, Child, relationshipname, parentid , childid):
    """
    build1tomany - this builds a one-to-many relationship between Parent and a Child.  A single parent can have many children.
    
    INPUT - format
    Parent   - this must be a declarative meta, not an instance e.g. Parent
    relationshipname - this is a string, relationship name for the Parent, in the Parent, to the Child, e.g. "children"
    parentid - this is a string, with the attribute that will be the parentid for the ForeignKey, e.g. "parent.id"
    Child    - this must be a declarative meta, not an instance, e.g. Child 
    Childclsname - this must be a string, the name of the Child class, which is different from the table it belongs to
    childid  - this is a string, with the attribute that will the childid for the ForeignKey e.g. "parent_id"

    e.g.
    class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     children = relationship("Child", backref="parent")
     
    class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer,primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))

# Parent needs 
- to set the relationship, relationship name, the name of the Child class, not the child's instance, and the backref back to the parent

    """
    
    setattr( Child , childid , Column( String, ForeignKey( parentid ) ) )

    parent_relation = relationship( Child.__name__ , backref= Parent.__tablename__ )
    setattr( Parent , relationshipname, parent_relation )
    return Parent, Child

#
#
# END of doSQL
#
#


class SetinSets( Base ):
    __tablename__ = 'sets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)

    def __repr__(self):
        return "<Set(name='%s', description='%s')>" % ( self.name, self.desc )


#
# test code test data
#
set0dic = { 'id' : 0 , 'name' : 'Set0' , 'desc' : 'Set 0 in Sets' }
set1dic = { 'id' : 1 , 'name' : 'Set1' , 'desc' : 'Set 1 in Sets' }
set2dic = { 'id' : 2 , 'name' : 'Set2' , 'desc' : 'Set 2 in Sets' }
set3dic = { 'id' : 3 , 'name' : 'Set3' , 'desc' : 'Set 3 in Sets' }

#set0 = SetinSets
#print type(Set0)  # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'> it's a Meta.  hmmm.


# cf. http://stackoverflow.com/questions/6474549/error-with-dynamic-classes-and-sqlalchemy

def Repr(self):
    return "<Tbl(id='%s', name='%s', description='%s')>" % ( self.id, self.name, self.desc )


# cf. https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA
# the necessity of this guy is that different tables might have completely different types and number of columns

tbl0dic = { 'id' : 0 , 'name' : 'Tbl0' , 'desc' : 'Table 0 in Set', 'created' : datetime.utcnow() }
tbl1dic = { 'id' : 1 , 'name' : 'Tbl1' , 'desc' : 'Table 1 in Set', 'created' : datetime.utcnow() }
tbl2dic = { 'id' : 2 , 'name' : 'Tbl2' , 'desc' : 'Table 2 in Set', 'created' : datetime.utcnow() }
tbl3dic = { 'id' : 3 , 'name' : 'Tbl3' , 'desc' : 'Table 3 in Set', 'created' : datetime.utcnow() }
tbl4dic = { 'id' : 4 , 'name' : 'Tbl4' , 'desc' : 'Table 4 in Set', 'created' : datetime.utcnow() }
tbl5dic = { 'id' : 5 , 'name' : 'Tbl5' , 'desc' : 'Table 5 in Set', 'created' : datetime.utcnow() }

# after one does the Foreign ID, one could specify the foreign id
tbldiceg = { '__tablename__' : 'cool' , 
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

tbldiceg = dict( { '__tablename__' : 'tbls_in_sets' } , **tbldiceg )
#Tbl1diceg = dict( { '__tablename__' : 'TblsinSets' } , **tbldiceg1 )

def TblinSet( clsname, dic  ):
    """
    TblinSet
    -the necessity of this class is that different tables might have completely different types and number of columns

    20140623 - EY : notice that clsname, an input argument, is a string, and is the name of the class itself, accessible by Tbl.__name__

    cf. https://groups.google.com/forum/#!topic/sqlalchemy/hs2yx--0lRA 
    """

    Tbl = type( clsname , (Base, ), dic )
#    setattr(Tbl,"__repr__", classmethod(Repr) )

    return Tbl # or Tbl() ?


# what's the difference in naming the class name in type to be something else than how it is "instantiated"? when making an instance of the class?  
# Tbl.__name__
# 'Tblrow'

Tbl = TblinSet( 'Tbl', tbldiceg)
type(Tbl)  # <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>

# setattr(tbl,"__repr__", classmethod(Repr) ) # doesn't work, something wrong with that dude, Lars', implementation
setattr(Tbl,"__repr__", Repr)


SetinSets, Tbl = build1tomany( SetinSets, Tbl, 'toTbl', 'sets.name', 'toSet')

set0 = SetinSets()
set1 = SetinSets()
set2 = SetinSets()
set3 = SetinSets()
set0 = PutinSQLAlch( set0, set0dic)
set1 = PutinSQLAlch( set1, set1dic)
set2 = PutinSQLAlch( set2, set2dic )
set3 = PutinSQLAlch( set3, set3dic )


# So it works
tbl0 = Tbl()
tbl0 = PutinSQLAlch( tbl0, tbl0dic)
tbl1 = Tbl()
tbl1 = PutinSQLAlch( tbl1, tbl1dic)
tbl2 = Tbl()
tbl2 = PutinSQLAlch( tbl2, tbl2dic)
tbl3 = Tbl()
tbl3 = PutinSQLAlch( tbl3, tbl3dic)
tbl4 = Tbl()
tbl4 = PutinSQLAlch( tbl4, tbl4dic)
tbl5 = Tbl()
tbl5 = PutinSQLAlch( tbl5, tbl5dic)

#
# playing with stuff, adding the foreign key attribute values
#
tbl0 = PutinSQLAlch( tbl0, { 'toSet' : set0.name } )
tbl1 = PutinSQLAlch( tbl1, { 'toSet' : set0.name } )
tbl2 = PutinSQLAlch( tbl2, { 'toSet' : set0.name } )
tbl3 = PutinSQLAlch( tbl3, { 'toSet' : set0.name } )
tbl4 = PutinSQLAlch( tbl4, { 'toSet' : set1.name } )
tbl5 = PutinSQLAlch( tbl5, { 'toSet' : set1.name } )

# Now
print set0.__tablename__
print set1.__tablename__
# in SetinSets, each set can have many tables, even if the tables have different numbers of and different types of columns (distinct tables!)


#Tbl0 = PutinSQLAlch( Tbl0, Tbl0dic )
print tbl0.__repr__()


#
# making another layer, another 1-to-many relationship
#
coldiceg = { 
                                     'series'            : Column(String, primary_key=True) ,
                                     'desc'          : Column(String, nullable=True, unique=True) ,
                                     'mul'          : Column(Integer, nullable=False, unique=False) }

coldiceg1 = deepcopy(coldiceg)

coldiceg2 = { 
    'series'            : Column(String, primary_key=True) ,
    'desc'          : Column(String, nullable=True, unique=True) ,
    'mul'          : Column(Integer, nullable=False, unique=False)  , 
    'terms'        : Column(String) }

tbl0.name


def colsdescmkr( clsname, seriesname , coldiceg ): # column desc maker
    """
    colsdescmkr - column dictionary maker

    this is another deeper layer, another 1-to-many relationship

    # be careful, it's not good to make the class name as the same as the series or table name
    OUTPUT - it should return a DeclarativeMeta
    """
    
    coldiceg = dict( { '__tablename__' : seriesname }, **coldiceg )
    
    return TblinSet( clsname, coldiceg )



Col00 = colsdescmkr( "ColinTbl0", "colsintbl0", coldiceg )
#Col1 = coldicmkr( "ColinTbl0", coldiceg1 ) # it works
Col11 = colsdescmkr( "ColinTbl1" , "colsintbl1" , coldiceg2)

Tbl, Col00 = build1tomany( Tbl, Col00, "toColofTbl0" , "tbls_in_sets.name" , "toTbl"  )
Tbl, Col11 = build1tomany( Tbl, Col11, "toColofTbl1" , "tbls_in_sets.name" , "toTbl" )

col0 = Col00()
col1 = Col00()
col2 = Col00()
col3 = Col00()
col4 = Col00()

col5 = Col11()
col6 = Col11()

#
# sample data


Col0dic = { 'series' : 'Col0' , 'desc' : 'Column 0 in Table 0', 'mul' : 1 , 'toTbl' : tbl0.name }
Col1dic = { 'series' : 'Col1' , 'desc' : 'Column 1 in Table 0', 'mul' : 1 , 'toTbl' : tbl0.name }
Col2dic = { 'series' : 'Col2' , 'desc' : 'Column 2 in Table 0', 'mul' : 1 , 'toTbl' : tbl0.name }
Col3dic = { 'series' : 'Col3' , 'desc' : 'Column 3 in Table 0', 'mul' : 1 , 'toTbl' : tbl0.name }
Col4dic = { 'series' : 'Col4' , 'desc' : 'Column 4 in Table 0', 'mul' : 1 , 'toTbl' : tbl0.name }

Col5dic = { 'series' : 'Col5' , 'desc' : 'Column 5 in Table 1', 'mul' : 1 , 'terms' : 'in Table 1, col 5' , 'toTbl' : tbl1.name }
Col6dic = { 'series' : 'Col6' , 'desc' : 'Column 6 in Table 1', 'mul' : 1 , 'terms' : 'in Table 1, col 6' , 'toTbl' : tbl1.name }

#Col0 = PutinSQLAlch( Col0, Col0dic )
#Col1 = PutinSQLAlch( Col1, Col1dic )

col0 = PutinSQLAlch( col0, Col0dic )
col1 = PutinSQLAlch( col1, Col1dic )
col2 = PutinSQLAlch( col2, Col2dic )
col3 = PutinSQLAlch( col3, Col3dic )
col4 = PutinSQLAlch( col4, Col4dic )

col5 = PutinSQLAlch( col5, Col5dic )
col6 = PutinSQLAlch( col6, Col6dic )



from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


session.add_all( [ set0, set1, set2, set3, tbl0, tbl1, tbl2, tbl3, tbl4, tbl5 , col0, col1, col2, col3, col4, col5, col6 ] )
session.commit()

for instance in session.query(SetinSets).all():
    print instance

for instance in session.query(Tbl).all(): print instance

for instance in session.query( SetinSets, Tbl).filter( SetinSets.name == Tbl.toSet).all(): print instance





