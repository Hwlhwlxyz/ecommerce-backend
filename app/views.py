import datetime

import flask
from flask import render_template, request, jsonify, Response, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful.representations import json

from app import app, database

from app.models import *

import re



def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.route('/index')
def index():
    return "hello world"


@app.route('/login', methods=['POST'])
def login():
    print(request.json)
    print(request)
    return jsonify({'test':'test'})

@app.route('/q', methods=['GET'])
def querytest():
    print(Customer.querytest())
    result = Customer.querytest()
    #return {'result',Customer.querytest()}
    return jsonify(result)

@app.route('/q2', methods=['GET'])
def querytest2():
    print(Customer.querytest2())
    result = Customer.querytest2()
    #return {'result',Customer.querytest()}
    return jsonify(result)

@app.route('/qadd', methods=['GET'])
def qadd():
    c = Customer('cname', 'home', '1', 'u1', 'p1')
    result = c.add()
    return {'result':result}

#customer
@app.route('/customer/<ckind>/login', methods=['POST'])
def customer_login(ckind):
    username = request.json['username']
    password = request.json['password']
    c = Customer.login(username, password, ckind)
    if c:
        return jsonify(c.serialize())
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
    if ckind=="home":
        c = Home.getbycustomerid(cid)
    elif ckind=="business":
        c = Business.getbycustomerid(cid)
    print(c)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": ckind+ " " + cid +" not found"}, 400


@app.route('/customer/update/<ckind>/<cid>', methods=['POST'])
def customerinfo_update_home_business(ckind, cid):
    c = None
    info = request.json
    print(info)
    if ckind=="home":
        homejson={
            'income':info['income'],
            'marriage_status': info['marriage_status'],
            'gender':info['gender'],
            'age':info['age']
        }
        c = Home.query.filter_by(customerid=cid).update(homejson)
    elif ckind=="business":
        businessjson={
            'business_category':info['business_category'],
            'comp_gross_annual_income':info['comp_gross_annual_income']
        }
        c = Business.query.filter_by(customer=cid).update(businessjson)
    print(c)
    if c:
        return {"success":"updated", "result":c}
    else:
        return {"error": ckind+ " " + cid +" update error"}, 400




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

    print('getaddress!!',c)
    if c:
        return jsonify(c.serialize())
    else:
        return {"error": "get with address error"}, 400



#classification
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


#product
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


@app.route('/transaction/getbycid/<cid>/submit', methods=['GET']) #submit list of transactions
def transactions_submit(cid):
    print(request.json)
    print(cid)
    return {'m':'test'}

@app.route('/transaction', methods=['GET']) #get all transactions
def get_all_transactions():
    results = Transaction.query.all()
    newstore = Store(1,1,1,1)
    newstore.add()
    if results:
        return json.dumps(Transaction.serialize_list(results), default=datetime_handler)
    else:
        return {"error","no transaction"}, 400

@app.route('/transactionlist/<cid>/submit', methods=['POST']) #get all transactions
def transactionlist_submit(cid):
    print(request.json)
    transactionlist = request.json
    for t in transactionlist:
        if t['inventory_amount']<t['select_amount']:
            return {"error", "out of stock"}, 400

    result = []
    for t in transactionlist:
        newtransaction = Transaction(t['select_amount'],cid,t['pid'],t['sid'])
        newtransaction.add()
        result.append(newtransaction.serialize())
    return result

#store
@app.route('/store', methods=['GET']) #get all transactions
def get_all_stores():
    results = Store.query.all()
    if results:
        return {'info','not finished'}
    else:
        return {"error","no transaction"}, 400



#region
@app.route('/region/salesvolume', methods=['GET']) #get all transactions
def region_salesvolume():
    results = Region.region_salesvolume()
    if results:
        return json.dumps(Region.serialize_list(results))
    else:
        return {"error", "no transaction"}, 400



#salesperson
@app.route('/allsalespersons', methods=['GET']) #get all transactions
def get_all_salespersons():
    results = Salesperson.get_all()
    if results and len(results)>0:
        return json.dumps(results)
    else:
        return {"error","no transaction"}, 400

