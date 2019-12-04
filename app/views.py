import datetime
import decimal

import flask
from flask import render_template, request, jsonify, Response, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful.representations import json

from app import app, database

from app.models import *


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def decimal_handler(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    raise TypeError("Unknown type")


def serialize_list(self):
    return [m.serialize() for m in self]


@app.route('/index')
def index():
    return "hello world"


@app.route('/login', methods=['POST'])
def login():
    print(request.json)
    print(request)
    return jsonify({'test': 'test'})


@app.route('/q', methods=['GET'])
def querytest():
    print(Customer.querytest())
    result = Customer.querytest()
    # return {'result',Customer.querytest()}
    return jsonify(result)


@app.route('/q2', methods=['GET'])
def querytest2():
    print(Customer.querytest2())
    result = Customer.querytest2()
    # return {'result',Customer.querytest()}
    return jsonify(result)


@app.route('/qadd', methods=['GET'])
def qadd():
    c = Customer('cname', 'home', '1', 'u1', 'p1')
    result = c.add()
    return {'result': result}


# customer
@app.route('/customer/<ckind>/login', methods=['POST'])
def customer_login(ckind):
    username = request.json['username']
    password = request.json['password']
    c = Customer.login(username, password, ckind)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": "wrong password"}, 400


@app.route('/customer/update/<cid>', methods=['POST'])
def customer_info_update(cid):
    accountinfojson = request.json
    print(accountinfojson)
    c = Customer.query.filter_by(cid=cid).update(accountinfojson)
    db.session.commit()
    if c:
        return {"success": "updated", "return": c}
    else:
        return {"error": "wrong password"}, 400


@app.route('/customer/getbyid/<cid>', methods=['GET'])
def customer_getbyid(cid):
    c = Customer.get_by_id(cid)
    print(c)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": "wrong password"}, 400


@app.route('/customer/<ckind>/<cid>', methods=['GET'])
def customerinfo_home_business(ckind, cid):
    c = None
    if ckind == "home":
        c = Home.getbycustomerid(cid)
    elif ckind == "business":
        c = Business.getbycustomerid(cid)
    print(c)
    if c:
        return json.dumps(c.serialize())
    else:
        return {"error": ckind + " " + cid + " not found"}, 400


@app.route('/customer/update/<ckind>/<cid>', methods=['POST'])
def customerinfo_update_home_business(ckind, cid):
    c = None
    info = request.json
    print(info)
    if ckind == "home":
        homejson = {
            'income': info['income'],
            'marriage_status': info['marriage_status'],
            'gender': info['gender'],
            'age': info['age']
        }
        c = Home.query.filter_by(customerid=cid).update(homejson)
        db.session.commit()
    elif ckind == "business":
        businessjson = {
            'business_category': info['business_category'],
            'comp_gross_annual_income': info['comp_gross_annual_income']
        }
        c = Business.query.filter_by(customerid=cid).update(businessjson)
        db.session.commit()
    print(c)
    if c:
        return {"success": "updated", "result": c}
    else:
        return {"error": ckind + " " + cid + " update error"}, 400


@app.route('/customer/getwithaddress/<cid>', methods=['GET'])
def customer_getwithaddress(cid):
    c = Customer.get_withaddress(cid)
    print(c)
    if c:
        return jsonify(c)
    else:
        return {"error": "get with address error"}, 400


@app.route('/address/getbycid/<cid>', methods=['GET'])
def address_getbycid(cid):
    c = Address.getbycustomerid(cid)
    print('getaddress!!', c)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": "get with address error"}, 400


@app.route('/address/update/<cid>', methods=['POST'])
def address_update(cid):
    addressjson = request.json
    print(addressjson)

    c = Address.query.filter_by(aid=addressjson['aid']).update(addressjson)
    db.session.commit()
    print('getaddress!!', c)
    if c:
        return {"success": "updated", "result": c}
    else:
        return {"error": "get with address error"}, 400


# classification
@app.route('/classification', methods=['GET'])
def get_all_classification():
    c = Classification.get_all()
    kinds = [k['kind'] for k in c]
    if c:
        return json.dumps(kinds)
    else:
        return {"error": "error"}, 400


@app.route('/classification/getbypid/<pid>', methods=['GET'])
def get_classification_by_pid(pid):
    c = Classification.get_by_pid(pid)
    kinds = [k['kind'] for k in c]
    if c:
        return json.dumps(kinds)
    else:
        return {"error": "error"}, 400


@app.route('/classification/topcategories', methods=['GET'])  # get all transactions
def topcategories():
    results = Classification.get_top_classification()
    if results:
        return json.dumps(results, default=decimal_handler)
    else:
        return {"error", "no transaction"}, 400



# product
@app.route('/product/getbyclassification/<kind>', methods=['GET'])
def get_products_byclassification(kind):
    print(kind)
    p_list = Product.get_by_classification(kind)
    for p in p_list:
        p['kind'] = Classification.get_by_pid_list(p['pid'])
    if p_list:
        return json.dumps(p_list)
    else:
        return {"error": "error"}, 400

@app.route('/product/<text>', methods=['GET'])
def search_text(text):
    p_list = Product.search_name(text)
    if p_list:
        return json.dumps(p_list)
    else:
        return {"error": "error"}, 400


@app.route('/product/all', methods=['GET'])
def get_all_products():
    p_list = Product.get_all()
    print(p_list)
    for p in p_list:
        p['kind'] = Classification.get_by_pid_list(p['pid'])
    if p_list:
        return json.dumps(p_list)
    else:
        return {"error": "error"}, 400


@app.route('/product/add', methods=['POST'])
def product_add():
    jsoninfo = request.json
    print(jsoninfo)
    productinfo = jsoninfo['product']
    kindsinfo = jsoninfo['kinds']
    p = Product(productinfo['pname'], productinfo['price'], productinfo['inventory_amount'], None)
    p.add()

    print(p.pid)
    for k in kindsinfo:
        newk = Classification(p.pid, k)
        newk.add()
    print(productinfo, kindsinfo)
    return p.serialize()


@app.route('/product/edit', methods=['POST'])
def product_edit():
    print("edit" * 10)
    jsoninfo = request.json
    print(jsoninfo)
    productinfo = jsoninfo['product']
    kindsinfo = jsoninfo['kinds']
    newproductinfo = {
        'pid': productinfo['pid'],
        'pname': productinfo['pname'],
        'price': productinfo['price'],
        'inventory_amount': productinfo['inventory_amount']
    }
    result = Product.query.filter_by(pid=productinfo['pid']).update(newproductinfo)
    db.session.commit()
    # delete all kinds of this product then add new kinds
    Classification.query.filter_by(pid=productinfo['pid']).delete()
    db.session.commit()

    for k in kindsinfo:
        newk = Classification(productinfo['pid'], k)
        newk.add()
    print(productinfo, kindsinfo)
    return {"success": "updated"}


#transaction
@app.route('/transaction/getbycid/<cid>/submit', methods=['GET'])  # submit list of transactions
def transactions_submit(cid):
    print(request.json)
    print(cid)
    return {'m': 'test'}


@app.route('/transaction', methods=['GET'])  # get all transactions
def get_all_transactions():
    results = Transaction.query.all()
    if results:
        return json.dumps(Transaction.serialize_list(results), default=datetime_handler)
    else:
        return {"error", "no transaction"}, 400


@app.route('/transactionlist/<cid>/<sid>/submit', methods=['POST'])  # get all transactions
def transactionlist_submit(cid, sid):
    print(request.json)
    transactionlist = request.json
    for t in transactionlist:
        if t['inventory_amount'] < t['select_amount']:
            return {"error": "out of stock", "pid": t['pid']}, 400
    print(sid)
    result = []

    for t in transactionlist:
        # add transactions
        newtransaction = Transaction(t['select_amount'], cid, t['pid'], sid)
        newtransaction.add()
        result.append(newtransaction.serialize())
        # update totalprice
        newtransaction.update_totalprice()
        # decrease product
        newtransaction.decrease_product_inventoryamount()


    return {"success": "updated"}


@app.route('/transaction/salesandprofit', methods=['GET'])
def get_salesandprofit():
    results = Transaction.get_sales_and_profit()
    if results:
        return json.dumps(results, default=decimal_handler)
    else:
        return {"error", "no transaction"}, 400


@app.route('/transaction/mostgivenproducts_boughtbyc/<pid>', methods=['GET'])
def get_mostgivenproducts(pid):
    results = Transaction.most_given_products(pid)
    print(results, len(results),len(results)>0)
    if ((len(results)) > 0):
        print("true")
        return json.dumps(results, default=decimal_handler)
    else:
        print("false")
        return {"error", "no transaction"}





# store
@app.route('/store/getall', methods=['GET'])  # get all transactions
def get_all_stores():
    results = Store.query.all()
    if results:
        return json.dumps(Store.serialize_list(results))
    else:
        return {"error", "no transaction"}, 400


@app.route('/store', methods=['GET'])
def get_all_stores_info():
    results = Store.get_all_store_info()
    if results:
        return json.dumps(results)
    else:
        return {"error", "no transaction"}, 400


# region
@app.route('/region/salesvolume', methods=['GET'])  # get all transactions
def region_salesvolume():
    results = Region.region_salesvolume()
    if results:
        return json.dumps(Region.serialize_list(results))
    else:
        return {"error", "no transaction"}, 400


@app.route('/region', methods=['GET'])
def all_region():
    results = Region.query.all()
    if results:
        return json.dumps(serialize_list(results))
    else:
        return {"error", "no transaction"}, 400

@app.route('/region/sales', methods=['GET'])
def get_all_sales_of_region():
    results = Region.get_region_sales()
    if results:
        return json.dumps(results, default=decimal_handler)
    else:
        return {"error", "no transaction"}, 400




# salesperson
@app.route('/allsalespersons', methods=['GET'])  # get all transactions
def get_all_salespersons():
    results = Salesperson.get_all()
    if results and len(results) > 0:
        return json.dumps(results)
    else:
        return {"error", "no transaction"}, 400


@app.route('/salesperson/login', methods=['POST'])
def saleperson_login():
    username = request.json['username']
    password = request.json['password']
    c = Salesperson.login(username, password)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": "wrong password"}, 400


@app.route('/salesperson/<sid>', methods=['GET'])
def get_salesperson_info(sid):
    result = Salesperson.get_all_info(sid)
    if result:
        return jsonify(result)
