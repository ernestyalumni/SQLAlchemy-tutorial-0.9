# SQLalchtut09.py
# following the examples in the 0.9 version of SQLAlchemy and its documentation
# Shout outs to Mike Bayer for SQLAlchemy and the SQLAlchemy documentation
# 20140608
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

import sqlalchemy
sqlalchemy.__version__

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)  # echo flag is a shortcut to setting up SQLAlchemy logging, with it enabled, we'll see all the generated SQL produced
# return value of create_engine() is instance of Engine, represents the core interface to the database, adapted through a dialect that handles the details of the database and DBAPI in use
# first time a method like Engine,execute() or Engine.connect() is caled, Engine establishes a real DBAPI connection to the database, which is then used to emit the SQL. 
# When using the ORM, we typically don't use the Engine directly once created; instead, it's used behind the scenes by the ORM as we'll see shortly.

# Lazy Connecting, Engine, when first returned by create_engine(), hasn't actually tried to connect to the database yet; that happens only the first time it is asked to perform a task against the database


#
# 2.1.3 Declare a Mapping
#

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# Now that we have a "base", we can define any number of mapped classes in terms of it. Start with just a single table called users, which will store records for the end users using our application. 
# A new class called User will be the class to which we map this table.  

from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)



User.__table__

#
# Declarative system is highly recommended: pp. 9 - The Declarative system, though highly recommended, is not required in order to use SQLAlchemy's ORM. any plain Python lcass can be mapped to any Table using the mapper() function directly; this less common usage is described at Classical Mappings
#




# A class using Declarative at a minimum needs a __tablename__ attribute, and at least one Column which is part of a primary key
# EY 20140609 how do we automatically define multiple columns? Maybe here?
# cf. http://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python

# on Mixins
# cf. pp. 286 Mixin and Custom Base Classes
# common need when using declarative (this whole paradigm) is to share some functionality, such as a set of common columns, some common table options, or other mapped properties, across many classes

#
# 2.1.4 Create a Schema  
# what's happening is this - it created a Table object according to our specifications, and associated it with the class by constructing a Mapper object
# This object is a behind-the-scenes object we normally don't need to deal with directly
#
# The Table object is a member of a larger collection known as MetaData. When using Declarative, this object is available using the .metadata attribute of our declarative base class

# EY 20140609 try
# User.metadata.tables
# Base.metadata.tables

# Base.metadata.create_all(engine)

# cf. http://stackoverflow.com/questions/9449840/sqlalchemy-tutorial-example-not-working
# Initialize database schema (create tables)
Base.metadata.create_all(engine)

#
# Minimal Table Descriptions vs. Full descriptions
"""
from sqlalchemy import Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)
"""
# why Sequence? - cf. pp. 10 Ch. 2. SQLAlchemy ORM, Firebird and Oracle require sequences to generate new primary key identifiers, and SQLAlchemy doesn't generate or assume these without being instructed. For that, you use the Sequence construct

#
# 2.1.5. Create an Instance of the Mapped Class
#

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
ed_user.name
ed_user.password
str(ed_user.id)

# cf. 11. 2.1.Object Relational Tutorial
# the __init__() method
# Our User class, as defined using the Declarative system, has been provided with a constructor (e.g. __init__() method) which automatically accepts keyword names that match the columns we've mapped. 
# We are free to define any explicit __init__() method we prefer on our class, which will override the default method provided by Declarative
# EY : 20140609 so this possibly could do stuff we want for the classes, like automatic declaration of Columns

#
# 2.1.6 Creating a Session
# We're now ready to start talking to the database.

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)  # Session class which will serve as a factor for new Session objects

session = Session()

#
# 2.1.7 Adding New Objects
#

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

# pp. 12 Chapter 2. SQLAlchemy ORM
# At this point, the instance is pending - no SQL has yet been issued and the object is not yet represented by a row in the database
# 
# The Session will issue the SQL to persist Ed Jones as soon as is needed, i.e. flush
# If we query the database for Ed jones, all pending information will first be flushed, and query issued immediately thereafter

# create a new Query object
# EY : 20140609 remember to create the tables and schema with Base.metadata.create_all(engine)
# cf. http://stackoverflow.com/questions/9449840/sqlalchemy-tutorial-example-not-working
#
our_user = session.query(User).filter_by(name='ed').first()

ed_user is our_user
# identity map, ensures that all operations upon a particular row within a Session operate upon the same set of data

session.add_all([
        User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')])

ed_user.password = 'f8s7ccs'

session.dirty # Session is paying attention, that modified

session.new   # three new User objects are pending

session.commit()  # commit() flushes whatever remaining changes remain to the database, and commits the transaction. The connection resources references by the session are now returned to the connection pool. Subsequent operations with this session will occur in a new transaction, which will again reacquire connection resources when first needed

ed_user.id

#
# 2.1.8 Rolling Back
#

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='INvalid', password='12345')

session.add(fake_user)

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

session.rollback()

fake_user in session



#
# 2.1.9. Querying
#

for instance in session.query(User).order_by(User.id):
    print instance.name, instance.fullname


for name, fullname in session.query(User.name, User.fullname):  # Query also accepts ORM-instrumented descriptors as arguments
    print name, fullname

for row in session.query(User, User.name).all():
    print row.User, row.name


for row in session.query(User.name.label('name_label')).all():  # control the names of individual column expressions using the label() construct, which is available from any ColumnElement - derived object
    print(row.name_label)

from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')

for row in session.query(user_alias, user_alias.name).all():
    print row.user_alias

# Basic operations with Query include issuing LIMIT and OFFSET, most conveniently using Python array slices and typically in conjunction with ORDER BY
for u in session.query(User).order_by(User.id)[1:3]:
    print u

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print name

# or filter(), which uses more flexible SQL expression language constructs. These allow you to use regular Python operators with the class-level attributes on your mapped class:

for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
    print name

# The Query object is fully generative, meaning that most method calls return a new Query object upon which futher criteria may be added.
# For example, to query for users named "ed" with full name "Ed Jones', call filter() twice, which joins criteria using AND

for user in session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones'):
    print user

# equals
[ out for out in session.query(User).filter(User.name=='ed') ]

# not equals
[ out for out in session.query(User).filter(User.name != 'ed') ]

# LIKE
[ out for out in session.query(User).filter(User.name.like('%ed%') ) ]

# IN
[ out for out in session.query(User).filter(User.name.in_(['ed','wendy','jack'] ) ) ]

# works with query objects too:
[ out for out in session.query(User).filter(User.name.in_( session.query(User.name).filter(User.name.like('%ed%') ) ) )   ]

# IS NULL
[ out for out in session.query(User).filter(User.name== None ) ]

# alternatively, if pep8/linters are a concern
[ out for out in session.query(User).filter(User.name.is_(None) ) ]

# IS NOT NULL
[ out for out in session.query(User).filter(User.name != None) ]

# alternatively, if pep8/linters are a concern

[ out for out in session.query(User).filter(User.name.isnot(None)  )]

# AND

# use and_()
from sqlalchemy import and_
[ out for out in session.query(User).filter(and_(User.name == 'ed', User.fullname == 'Ed Jones')) ]
  
# or send multiple expressions to .filter()
[ out for out in session.query(User).filter(User.name == 'ed', User.fullname == 'Ed Jones') ]

# or chain multiple filter()/filter_by() calls
[ out for out in session.query(User).filter(User.name =='ed').filter(User.fullname == 'Ed Jones') ]

# OR
from sqlalchemy import or_
[ out for out in session.query(User).filter(or_(User.name == 'ed', User.name == 'wendy')) ]

# MATCH
# [ out for out in session.query(User).filter(User.name.match('wendy') ) ]
# Note: match() uses a database-specific MATCH or CONTAINS function; its behavior will vary by backend and is not available on some backends such as SQLite


#
# Returning Lists and Scalars 
#
# a number of methods on Query immediately issue SQL and return a value containing loaded database results. Here's a brief tour.

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
query.all()

# first() applies a limit of one and returns the first result as a scalar
query.first()

# one(), fully fetches all rows, and if not exactly one object identity or composite row is present in the result, raises an error. With multiple rows found: 
from sqlalchemy.orm.exc import MultipleResultsFound
try:
      user = query.one()
except MultipleResultsFound, e:
      print e

# error raised MultipleResultsFoudn

from sqlalchemy.orm.exc import NoResultFound
try:
    user = query.filter(User.id == 99).one()
except NoResultFound, e:
    print e  # No row was found for one() 
# NoResultFound catches this exception

# The one() method is great for systems that expect to handle "no items found" versus "multiple items found" differently, 



#
# Counting
#
# Query includes a convenience method for counting called count():

session.query(User).filter(User.name.like('%ed')).count()

# for situations where the "things to be counted" needs to be indicated specifically, we can specify the "count" function directly using the expression func.count(), available from the func construct. Below we use it to return the count of each distinct user name:

from sqlalchemy import func
session.query(func.count(User.name), User.name).group_by(User.name).all()

session.query(func.count('*')).select_from(User).scalar()  # to achieve SELECT count(*) FROM table

session.query(func.count(User.id)).scalar()  # usage of select_from() can be removed if we express the count in terms of the User primary key directly


#
# 2.1.10 Building a Relationship
#

# cf. pp. 23 Users in our system can store any number of email addresses associated with their username. This implies a basic one to many association from the users to a new table which stores email addresses, which we will call addresses.
# 

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('addresses', order_by=id))
    
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

    # ForeignKey construct is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.  
# ForeignKey above expresses that values in the addresses.user_id column should be constrained to those values in the users.id column, i.e. its primary key
# second directive, relationship(), tells ORM that Address class itself should be linked to the User class, using attribute Address.user.  
# relationship() uses foreign key relationships between 2 tables to determine the nature of this linkage, determining that Address.user will be many to 1
# subdirective of relationship() called backref() is placed inside of relationship(), providing details about the relationship as expressed in reverse, that of a collection of Address objects on User referenced by User.addresses.
# cf. Basic Relational Patterns, full catalog of available relationship() configurations pp. 23 2.1. Object Relational Tutorial

# The two complementing relationships Address.user and User.addresses are referred to as a bidirectional relationship, and is a key feature of the SQLAlchemy ORM. The section Linking Relationships with Backref discusses the "backref" feature in detail

Base.metadata.create_all(engine)

# 2.1.11 Working with Related Objects

jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses

jack.addresses = [ Address(email_address='jack@google.com'),
                   Address(email_address='j25@yahoo.com')]

jack.addresses[1]
jack.addresses[1].user

session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()

jack.addresses


#
# 2.1.12 Querying with Joins
#

# to construct a simple implicit join between User and Address, we can use Query.filter() to equate their related columns together
for u, a in session.query(User, Address).filter(User.id==Address.user_id).filter(Address.email_address=='jack@google.com').all():
    print u
    print a

# the actual SQL JOIN syntax acheived using Query.join()
session.query(User).join(Address).filter(Address.email_address=='jack@google.com').all()

# Query.join() knows how to join between User and Address because there's only one foreign key between them. 
# If there were no foreign keys, or several, Query.join() works better when one of the following forms are used:

session.query(User).join(Address, User.id==Address.user_id)  # explicit condition
session.query(User).join(User.addresses)                     # specify relationship from left to right
session.query(User).join(Address, User.addresses)            # same, with explicit target
session.query(User).join("addresses")                        # same, using a string

# outerjoin() function
session.query(User).outerjoin(User.addresses)                # LEFT OUTER JOIN

#
# Using Aliases
#
# When querying across multiple tables, if the same table needs to be referenced more than once, SQL typically requires that table be aliased with another name, so that it can be distinguihsed against other occurrences of that table.

from sqlalchemy.orm import aliased
adalias1 = aliased(Address)
adalias2 = aliased(Address)

for username, email1, email2 in session.query(User.name, adalias1.email_address, adalias2.email_address).join(adalias1, User.addresses).join(adalias2, User.addresses).filter(adalias1.email_address=='jack@google.com').filter(adalias2.email_address=='j25@yahoo.com'):
    print username, email1, email2

#
# Using Subqueries
# 
# The Query is suitable for generating statements which can be used as subqueries.
# Suppose we wanted to load User objects along with a count of how many Address records each user has.

from sqlalchemy.sql import func
stmt = session.query(Address.user_id, func.count('*').label('address_count')).group_by(Address.user_id).subquery()

# columns on the statement are accessible through an attribute called c:
for u, count in session.query(User, stmt.c.address_count).outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
    print u, count

#
# Selecting Entitles from Subqueries
#
# Above, we just selected a result that included a column from a subquery. What if we wanted our subquery to map to an entity?  

stmt = session.query(Address).filter(Address.email_address != 'j25@yahoo.com').subquery()

adalias = aliased(Address, stmt)
for user, address in session.query(User, adalias).join(adalias, User.addresses):
    print user
    print address

#
# Using EXISTS
#

from sqlalchemy.sql import exists
stmt = exists().where(Address.user_id==User.id)
for name, in session.query(User.name).filter(stmt):
    print name

# The Query features several operators which make usage of EXISTS automatically.  EY : 20140609 AUTOMATICALLY

for name, in session.query(User.name).filter(User.addresses.any()):
    print name

# any() takes criterion as well, to limit the rows matched
for name, in session.query(User.name).filter(User.addresses.any(Address.email_address.like('%google%'))):
    print name

# has() is the same operator as any() for many-to-1 relationships
session.query(Address).filter(~Address.user.has(User.name=='jack')).all()


#
# Common Relationship Operators
#

# __eq__() (many-to-1 "equals" comparsion)

# session.query(Address).filter(Address.user == ed)

# __ne__() (many-to-1 "not equals" comparison)

# session.query(Address).filter(Address.user != ed)

# IS NULL (many-to-1 comparison, also uses __eq__() )

session.query(Address).filter(Address.user == None)

# contains() (used for one-to-many collections)

# session.query(User).filter(User.addresses.contains(someaddress))

# any() (used for collections)

session.query(User).filter(User.addresses.any(Address.email_address == 'bar'))

# also takes keyword arguments:
session.query(User).filter(User.addresses.any(email_address='bar'))

# has() (used for scalar references)
session.query(Address).filter(Address.user.has(name='ed'))

# Query.with_parent() (used for any relationship)

# session.query(Address).with_parent( someuser, 'addresses')

#
# 2.1.13 Eager Loading
#
# Recall earlier that we illustrated a lazy loading operation, when we accessed the User.addresses collection of a User and SQL was emitted.  If you want to reduce the number of queries (dramatically, in many cases), we can apply an eager load to the query operation.
# EY : 20140609 the point immediately above is something I don't understand 
# SQLAlchemy offers 3 types of eager loading, 2 automatic, 3rd involves custom criterion
# all 3 usually invoked via functions known as query options
#
# Subquery Load

from sqlalchemy.orm import subqueryload
jack = session.query(User).options(subqueryload(User.addresses)).filter_by(name='jack').one()
jack

jack.addresses





#
# 2.1.14 Deleting
#

session.delete(jack)
session.query(User).filter_by(name='jack').count()

session.query(Address).filter( Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()

#
# Configuring delete/delete-orphan Cascade
#

session.close()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")  # EY : 20140609 only difference is here, in the relationship, backref to the user, user is in Address

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password'%s')>" % ( self.name, self.fullname, self.password)

# Then we recreate Address, noting that in this case we've created the Address.user relationship via the User class already 

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    def __repy__(self):
        return "<Address(email_address='%s')>" % self.email_addresses

# Now when we load the user jack (below using get(), which loads by primary key), removing an address from the corresponding addresses collection will result in that Address being deleted

# load Jack by primary key, EY : 20140609 it's the fifth one, just check out session.query(User).all()

jack = session.query(User).get(5)

del jack.addresses[1]

session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()

session.delete(jack)

session.query(User).filter_by(name='jack').count()

session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()

#
# More on Cascades
# Further detail on configuration of cascades is at Cascades

#
# 2.1.15 Building a Many to Many Relationship
#
# users write BlogPost items, which have Keyword items associated with them 

# for a plain many-to-many, we need to create an un-zipped Table construct to serve as the association table.
from sqlalchemy import Table, Text
# association table
post_keywords = Table('post_keywords', Base.metadata, Column('post_id', Integer, ForeignKey('posts.id') ), Column('keyword_id', Integer, ForeignKey('keywords.id')) )

# define BlogPost and Keyword, with a relationship() linked via the post_keywords table
class BlogPost(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')

    def __init__(self, headline, body, author):
        self.headline = headline
        self.body = body
        self.author = author

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

class Keyword(Base):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    def __init__(self, keyword):
        self.keyword = keyword

# Note: The above class declarations illustrate explicit __init__() methods. Remember, when using Declarative, it's optional!

# defining feature of a many-to-many relationship is the secondary keyword argument which references a Table object representing the association table.
# This table only contains columns which reference the 2 sides of the relatioship; if it has any other columns, such as its own primary key, or foreign keys to other tables, SQLAlchemy requires a different usage pattern called the "association object", described at Association Object

# When we access User.posts, we'd like to be able to filter results further so as not to load the entire collection. For this we use a setting accepted by relationship() called lazy='dynamic', which configures an alternate loader strategy on the attribute. To use it on the "reverse" side of a relationship(), we use the backref() function:

from sqlalchemy.orm import backref
# "dynamic" loading relationship to User
BlogPost.author = relationship(User, backref=backref('posts', lazy='dynamic'))

Base.metadata.create_all(engine)

wendy = session.query(User).filter_by(name='wendy').one()

post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
session.add(post)

# We're storing keywords uniquely in the database, but we know that we don't have any yet, so we can just create them:
post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))

# We can now look up all blog posts with the keyword 'firstpost'. We'll use the any operator to locate "blog posts where any of its keywords has the keyword string 'firstpost'
session.query(BlogPost).filter(BlogPost.keywords.any(keyword='firstpost')).all()

session.query(BlogPost).filter(BlogPost.author==wendy).filter(BlogPost.keywords.any(keyword='firstpost')).all()

# use Wendy's own posts relationship, which is a "dynamic"relationship, to query straight from there:
wendy.posts.filter(BlogPost.keywords.any(keyword='firstpost')).all()


#
#
# cf. SQLAlchemy Documentation Release 0.9.4.
# 2.6 Using the Session
#

#
# 2.6.2 Getting a Session
#

from sqlalchemy import create_engine

# an Engine, which the Session will use for connection resources
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.orm import sessionmaker

# create a configured "Session" class
Session = sessionmaker(bind=engine)  # Session class which will serve as a factor for new Session objects

# create a Session
session = Session()

# later, some unit of code wants to create a 
# Session that is bound to a specific Connection

# conn = engine.connect()
# session = Session(bind=conn)

#
# 2.6.3 Using the Session 
#
# Quickie Intro to Object States
# Pending - when you add() a transient instance, it becomes pending
# Persistent - an instance which is present in the session and has a record in the database
# Detached - an instance which has a record in the database, but is not in any session

#
# Getting the Current State of an Object

from sqlalchemy import inspect

inspect(wendy).transient
inspect(wendy).pending
inspect(wendy).persistent
inspect(wendy).detached

# Session Frequently Asked Questions
# When do I make a sessionmaker?
# Just 1 time, somewhere in your application's global scope. It should be looked upon as part of your application's configuration. 
# If your application has 3 .py files in a package, you could, for example, place the sessionmaker line in your __init__.py file; from that point on your other modules say "from mypackage import Session"

# When do I construct a Session, when do I commit it, and when do I close it?

# A Session is typically constructed at the beginning of a logical operation where database access is potentially anticipated

# as a general rule, keep the lifecycle of the session separate and external fro functions nad objects that access and/or manipulate database data.

# A Session is typically constructed at the beginning of a logical operation where database access is potentially anticipated.
# The Session, whenever it is used to talk to the database, begins a database transaction as soon as it starts communicating.
# Assuming the autocommit flag is left at its recommended default of False, this transaction remains in progress until the Session is rolled back, committed, or closed

#
# pp. 154
#        

# When to Expire or Refresh
# The Session uses the expiration feature automatically whenever the transaction referred to by the session ends.
# Meaning, whenever Session.commit() or Session.rollback() is called, all objects within the Session are expired, using a feature equivalent to that of the Session.expire_all() method.  
# The rationale is that the end of a transaction is a demarcating point at which there is no more context available in order to know what the current state of the database is, as any number of other transactions may be affecting it.

             





