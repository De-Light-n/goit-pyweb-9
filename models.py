
import configparser
import pathlib
from mongoengine import connect, Document, ReferenceField, StringField, ListField, CASCADE

file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')

connect(db="authors_and_quotes",
        host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/")

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}
    
class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    meta = {"collection": "quotes"}
    
