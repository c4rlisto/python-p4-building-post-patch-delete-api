#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return "Bakery API"


# --------------------
# GET BAKERIES
# --------------------
@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)


# --------------------
# PATCH BAKERY
# --------------------
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):

    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery is None:
        return make_response({"message": "Bakery not found"}, 404)

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.commit()

        return make_response(bakery.to_dict(), 200)


# --------------------
# GET + POST BAKED GOODS
# --------------------
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods, 200)

    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )

        db.session.add(new_baked_good)
        db.session.commit()

        return make_response(new_baked_good.to_dict(), 201)


# --------------------
# DELETE BAKED GOOD
# --------------------
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def baked_good_by_id(id):

    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if baked_good is None:
        return make_response({"message": "Baked good not found"}, 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response(
        {
            "delete_successful": True,
            "message": "Baked good deleted."
        },
        200
    )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
