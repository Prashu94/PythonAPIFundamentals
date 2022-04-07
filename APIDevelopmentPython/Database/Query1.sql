use smilecook;
-- flask db init - starts the database migration using alembic
-- flask db migrate - will create a python file to create the database table
-- flask db upgrade - will run the python code in the version folder and create the database tables.
select * from user;
select * from recipe;
-- one user can have many recipes
/*
- Recipe class will contain the foreign key relation to user (user_id = db.Column(db.Integer(), db.ForeignKey("user.id")))
- User class will have a recipes Object with backref to user through Recipe class (db.relationship('Recipe', backref='user'))
*/
delete from recipe;
delete from user;
-- adding a new field created to the database.
/*
1. Add a new attribute to the user class
2. run the command flask db migrate
3. flask db upgrade
Note: To refresh the column attribute before upgrade use
flask db stamp head
*/