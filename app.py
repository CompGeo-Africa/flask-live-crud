from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Shop(db.Model):
    __tablename__ = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    shopname = db.Column(db.String(120), unique=True, nullable=False)
    areaname = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(80), unique=True, nullable=False)
    areacode = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    desc = db.Column(db.Text)


    def json(self):
        return {'id': self.id,'shopname': self.shopname, 'areaname': self.areaname,'city': self.city,'areacode': self.areacode, 'description': self.description}

with app.app_context():    
    db.create_all()

""" 
    id 
    shopname
    areaname 
    city
    areacode
    created_at
    desc
"""

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# create a shop
@app.route('/shops', methods=['POST'])
def create_shop():
  try:
    data = request.get_json()
    new_shop = Shop(shopname=data['shopname'], areaname=data['areaname '], city=data['city'], areacode=data['areacode'], desc=data['desc'])
    db.session.add(new_shop)
    db.session.commit()
    return make_response(jsonify({'message': 'shop created'}), 201)
  except Exception as e:
    return make_response(jsonify({'message': 'error creating shop\\n' + str(e)}), 500)

# get all shops
@app.route('/shops', methods=['GET'])
def get_shops():
  try:
    shops = Shop.query.all()
    return make_response(jsonify([shop.json() for shop in shops]), 200)
  except Exception as e:
    return make_response(jsonify({'message': 'error getting shops\\n' + str(e)}), 500)

# get a shop by id
@app.route('/shops/<int:id>', methods=['GET'])
def get_shop(id):
  try:
    shop = Shop.query.filter_by(id=id).first()
    if shop:
      return make_response(jsonify({'shop': shop.json()}), 200)
    return make_response(jsonify({'message': 'shop not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error getting shop\\n' + str(e)}), 500)

# update a shop
@app.route('/shops/<int:id>', methods=['PUT'])
def update_shop(id):
  try:
    shop = Shop.query.filter_by(id=id).first()
    if shop:
      data = request.get_json()

      shop.shopname = data['shopname']
      areaname=data['areaname']
      city=data['city']
      areacode=data['areacode']
      desc=data['desc']

      db.session.commit()

      return make_response(jsonify({'message': 'shop updated'}), 200)
    
    return make_response(jsonify({'message': 'shop not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error updating shop\\n' + str(e)}), 500)

# delete a shop
@app.route('/shops/<int:id>', methods=['DELETE'])
def delete_shop(id):
  try:
    shop = Shop.query.filter_by(id=id).first()
    if shop:
      db.session.delete(shop)
      db.session.commit()
      return make_response(jsonify({'message': 'shop deleted'}), 200)
    return make_response(jsonify({'message': 'shop not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting shop\\n' + str(e)}), 500)