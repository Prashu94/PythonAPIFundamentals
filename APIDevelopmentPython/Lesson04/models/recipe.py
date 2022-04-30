from extensions import db

# Declare the recipe list
recipe_list = []


# Method to get the last_id in the recipe_list
def get_last_id():
    # if recipe_list is not empty
    if recipe_list:
        # store the last value in the list
        last_recipe = recipe_list[-1]
    else:
        return 1
    return last_recipe.id


"""
Class Representation for Recipe Table
"""


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    num_of_servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    directions = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    # Foreign Key of User in Recipe - i.e One User can have multiple recipes.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
