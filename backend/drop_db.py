from api import db, create_app

#create app and push context
app = create_app()
app.app_context().push()

#create and commit database
db.drop_all()
db.session.commit()

print('committed')