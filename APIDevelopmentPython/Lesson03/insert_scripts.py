from app import *
from models.user import User
from models.recipe import Recipe
app = create_app()
app.app_context().push()

user = User(username='jack', email='jack@gmail.com', password='WkQa')
db.session.add(user)
db.session.commit()

print(user.username)
print(user.email)

pizza = Recipe(name='Cheese Pizza', description='This is a lovely cheese pizza recipe',
               num_of_servings=2, cook_time=30, directions='This is how you make it', user_id=user.id)
db.session.add(pizza)
db.session.commit()

pasta = Recipe(name='Tomato Pasta', description='This is a lovely tomato pasta recipe',
               num_of_servings=3, cook_time=20, directions='This is how you make it', user_id=user.id)
db.session.add(pasta)
db.session.commit()


user = User.query.filter_by(username='jack').first()
print(user.recipes)

for recipe in user.recipes:
    print('{} recipe made by {} can serve {} people'.format(recipe.name,
                                                            recipe.user.username,
                                                            recipe.num_of_servings))
