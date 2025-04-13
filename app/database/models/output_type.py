from mongoengine import Document, StringField, ObjectIdField


class OutputType(Document):
    id = ObjectIdField(primary_key=True)
    name = StringField(required=True, max_length=100)
    description = StringField()

    meta = {
        'collection': 'output_types',
        'indexes': ['name']
    }

    def __repr__(self):
        return f"<OutputType(id={self.id}, name='{self.name}')>"
    