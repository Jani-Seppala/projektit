from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    passwordHash = db.StringField(required=True)
    favorites = db.ListField(db.ReferenceField('Stock'))

class Stock(db.Document):
    ticker = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    sector = db.StringField()

class News(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    datePublished = db.DateTimeField()
    stock = db.ReferenceField(Stock)

class Analysis(db.Document):
    newsId = db.ReferenceField(News, required=True)
    analysisContent = db.StringField(required=True)
    dateAnalyzed = db.DateTimeField()
