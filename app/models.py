from datetime import datetime

from sqlalchemy.orm import class_mapper

from app.database import db
from . import database


class Customer(db.Model):
    __tablename__ = 'customer'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(64), index=True)
    ckind = db.Column(db.String(64))
    aid = db.Column(db.Integer)

    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, cname, ckind, aid, username, password):
        self.cname = cname
        self.ckind = ckind
        self.aid = aid
        self.username = username
        self.password = password

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def login(username, password, ckind):
        r = Customer.query.filter_by(username=username, password=password, ckind=ckind).first()
        return r

    @staticmethod
    def querytest():
        sql = "select * from {}".format(Customer.__tablename__)
        result = database.query_db(sql)
        print(result)
        return result

    @staticmethod
    def querytest2():
        sql = "select * from {} where cid=:cid".format(Customer.__tablename__)
        result = database.query_db(sql, {'cid': 5})
        print(result)
        return result

    @staticmethod
    def get_by_id(cid):
        c = Customer.query.get(cid)
        print("getbyid",c)
        return c

    @staticmethod
    def get_withaddress(cid):
        sql = "select * from {} LEFT JOIN {} a on customer.aid = a.aid where cid=:cid".format(Customer.__tablename__, Address.__tablename__)
        result = database.query_db(sql, {'cid': cid}, one=True)
        print(result)
        return result



# customer kinds

class Business(db.Model):
    __tablename__ = 'business'
    businessid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.Integer)
    business_category = db.Column(db.String(64), index=True)
    comp_gross_annual_income = db.Column(db.Integer)

    def __init__(self, customerid, business_category, comp_gross_annual_income):
        self.customerid = customerid
        self.business_category = business_category
        self.comp_gross_annual_income = comp_gross_annual_income

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def getbycustomerid(cid):
        c = Business.query.get(cid)
        return c

class Home(db.Model):
    __tablename__ = 'home'
    homeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.Integer)
    income = db.Column(db.Integer)
    marriage_status = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, customerid, income, marriage_state, gender, age):
        self.customerid = customerid
        self.income = income
        self.marriage_state = marriage_state
        self.gender = gender
        self.age = age

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def getbycustomerid(cid):
        c = Home.query.get(cid)
        return c

# end of customer kinds


class Address(db.Model):
    __tablename__ = 'address'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer) #cid customer id
    street = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)
    zcode = db.Column(db.String(64), index=True)

    def __init__(self, street, city, state, zcode):
        self.street = street
        self.city = city
        self.state = state
        self.zcode = zcode

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def getbycustomerid(cid):
        c = Address.query.filter_by(cid=cid).first()
        return c

# product info

class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pname = db.Column(db.String(64))
    price = db.Column(db.Integer)
    inventory_amount = db.Column(db.Integer)
    kindid = db.Column(db.Integer)  # kid in classification

    def __init__(self, pname, price, inventory_amount, kindid):
        self.pname = pname
        self.price = price
        self.inventory_amount = inventory_amount
        self.kindid = kindid

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def get_by_classification(kind):
        sql = 'SELECT * FROM product WHERE pid IN (SELECT pid FROM classification WHERE classification.kind=:kind)'
        result = database.query_db(sql, {'kind': kind})
        return result

    @staticmethod
    def get_all():
        products = Product.query.all()
        return [p.serialize() for p in products]



class Classification(db.Model):
    __tablename__ = 'classification'
    kid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer)
    kind = db.Column(db.String(64))

    def __init__(self, pid, kind):
        self.pid = pid
        self.kind = kind

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def get_all():
        sql = 'SELECT DISTINCT(kind) FROM {}'.format(Classification.__tablename__)
        result = database.query_db(sql)
        return result

    @staticmethod
    def get_by_pid(pid):
        sql = 'SELECT kind FROM {} WHERE pid=:pid'.format(Classification.__tablename__)
        result = database.query_db(sql, {'pid': pid})
        return result



    @staticmethod
    def get_by_pid_list(pid):
        sql = 'SELECT kind FROM {} WHERE pid=:pid'.format(Classification.__tablename__)
        result = database.query_db(sql, {'pid': pid})
        kinds = [k['kind'] for k in result]
        return kinds

# salesperson info

class Region(db.Model):
    __tablename__ = 'region'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rname = db.Column(db.String(64))
    rmanagerid = db.Column(db.Integer)  # salespersonid in salesperson

    def __init__(self, rname, rmanagerid):
        self.rname = rname
        self.rmanagerid = rmanagerid

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def region_salesvolume():
        sql = """
        SELECT region.rid,COUNT(*)
                FROM region,store,salesperson,transaction
                WHERE region.rid=store.rid
                      AND
                      store.rid=salesperson.storeid
                      AND
                      salesperson.said=transaction.said
                GROUP BY transaction.amount
                
        """

        result = database.query_db(sql)
        return result


class Salesperson(db.Model):
    __tablename__ = 'salesperson'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sname = db.Column(db.String(64))
    salesperson_address = db.Column(db.Integer)  # aid in address
    email = db.Column(db.String(64))
    jobtitle = db.Column(db.String(64))
    salary = db.Column(db.Float)
    storeid = db.Column(db.Integer)  # sid in store

    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, sname, salesperson_address, email, jobtitle, salary, storeid, username, password):
        self.sname = sname
        self.salesperson_address = salesperson_address
        self.email = email
        self.jobtitle = jobtitle
        self.salary = salary
        self.storeid = storeid

        self.username = username
        self.password = password

    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    @staticmethod
    def get_all():
        sql = 'SELECT * FROM {}'.format(Salesperson.__tablename__)
        result = database.query_db(sql)
        return result


class Store(db.Model):
    __tablename__ = 'store'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addressid = db.Column(db.Integer)
    smanagerid = db.Column(db.Integer)  # sid in salesperson
    snum = db.Column(db.Integer) #number of salesperson
    rid = db.Column(db.Integer) #region id

    def __init__(self, addressid, smanagerid, snum, rid):
        self.addressid = addressid
        self.smanagerid = smanagerid
        self.snum = snum
        self.rid = rid


    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result

    # def get_all_info(self):
    #     sql = 'SELECT * FROM product WHERE pid IN (SELECT pid FROM classification WHERE classification.kind=:kind)'
    #     result = database.query_db(sql, {'kind': kind})
    #     kinds = [k['kind'] for k in result]
    #     return result




# transaction
class Transaction(db.Model):
    __tablename__ = 'transaction'
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    cid = db.Column(db.Integer)  # cid in customer
    pid = db.Column(db.Integer)  # pid in product
    sid = db.Column(db.Integer)  # sid in salesperson
    createdate = db.Column(db.DateTime, default=datetime.now())
    totalprice = db.Column(db.Float)

    def __init__(self, amount, cid, pid, sid):
        self.amount = amount
        self.cid = cid
        self.pid = pid
        self.sid = sid


    def serialize(self):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(self.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(self, c)) for c in columns)

    def serialize_list(self):
        return [m.serialize() for m in self]

    def add(self):
        db.session.add(self)
        result = db.session.commit()
        return result
