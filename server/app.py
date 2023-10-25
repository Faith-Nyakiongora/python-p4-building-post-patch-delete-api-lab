#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        price = data.get('price')
        
        if name is None or price is None:
            return jsonify({"error": "Both name and price are required"}), 400

        new_baked_good = BakedGood(name=name, price=price)
        db.session.add(new_baked_good)
        db.session.commit()

        return jsonify(new_baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    if request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()
        if bakery is None:
            return jsonify({"error": "Bakery not found"}), 404

        data = request.form
        new_name = data.get('name')

        if new_name is not None:
            bakery.name = new_name
            db.session.commit()

        return jsonify(bakery.to_dict()), 200
    
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    if request.method == 'DELETE':
        baked_good = BakedGood.query.get(id)
        if baked_good is None:
            return jsonify({"error": "Baked good not found"}), 404

        db.session.delete(baked_good)
        db.session.commit()

        return jsonify({"message": "Baked good deleted successfully"}), 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)
