import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
      type=float,
      required=True,
      help='This cannot be left blank!'
    )

  parser.add_argument('store_id',
      type=int,
      required=True,
      help='Every item needs a store ID!'
    )

  @jwt_required()  # this will make user to provide jwt token using 'Authorization' : 'JWT JWT_TOKEN'
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()
    return {'message': 'Item not found!'}, 404


  def post(self, name):
    if ItemModel.find_by_name(name):
      return {'message': "An item with the name '{}' already exists".format(name)}, 400

    data = Item.parser.parse_args()
    item = ItemModel(name, data['price'], data['store_id'])

    try:
      item.save_to_db()
    except:
      return {'message': 'An error occured while inserting items!'}, 500
      
    return item.json(), 201
    

  def delete(self, name):
    # global items
    # items = list(filter(lambda x: x['name'] != name, items))
    item = ItemModel.find_by_name(name)
    if item: 
      item.delete_from_db()

    return {'message': "Item '{}' deleted".format(name)}

  def put(self, name):
    data = Item.parser.parse_args()
    # item = next(filter(lambda x: x['name'] == name, items), None)
    item = ItemModel.find_by_name(name)

    if item is None:
      # item = { 'name': name, 'price': data['price']}
      # items.append(item)
      item = ItemModel(name, data['price'], data['store_id'])
    else:
      item.price = data['price']
      item.store_id = data['store_id']
    
    item.save_to_db()

    return item.json()
    
  

class ItemList(Resource):
  def get(self):
    return {'items': [item.json() for item in ItemModel.query.all()]}  # list comprehension