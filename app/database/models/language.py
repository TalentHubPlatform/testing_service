from mongoengine import Document, StringField, ObjectIdField


class Language(Document):
    id = ObjectIdField(primary_key=True)
    name = StringField(required=True, max_length=100)
    version = StringField(max_length=50)

    meta = {
        'collection': 'languages',
        'indexes': ['name']
    }

    def __repr__(self):
        return f"<Language(id={self.id}, name='{self.name}', version='{self.version}')>"
    