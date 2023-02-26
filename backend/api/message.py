from flask_restful import Api, Resource, reqparse
from utils.helper import classify_intent, filter_recipes, generate_response, load_data, get_recipe_names, generate_chitchat_response
import json

class MessageApiHandler(Resource):

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('message', type=str)

    args = parser.parse_args()

    print("message = ", args["message"])
    
    # classify the intent
    intent = classify_intent(args["message"])
    print("intent = ", intent)
          
    # load the data based on dining hall
    recipes = load_data(args["message"])

    if intent == 'poem':
      return "Soft and silky, white as snow,\nTofu sits on my plate just so.\nA protein-packed, healthy delight,\nTofu makes my taste buds take flight.\nFried or sautéed, in soup or stew,\nTofu adds flavor, through and through."
    
    elif intent == 'filter':

      recipes = filter_recipes(recipes, args["message"])
      recipe_names = get_recipe_names(recipes)
      return generate_response(args["message"], recipe_names)
    
    elif intent == "nofilter":
      recipe_names = get_recipe_names(recipes)
      return generate_response(args["message"], recipe_names)
    
    elif intent == "chitchat":
      return generate_chitchat_response(args["message"])
    
    else:
      return "Hey! I'm still 10 years old. Can you explain it like I'm five?"
