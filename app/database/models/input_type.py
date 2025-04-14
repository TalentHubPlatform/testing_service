from mongoengine import Document, StringField, ObjectIdField


class InputType(Document):
    DoesNotExist = None
    id = ObjectIdField(primary_key=True)
    name = StringField(required=True, max_length=100)
    description = StringField()

    meta = {
        'collection': 'input_types',
        'indexes': ['name']
    }

    def __repr__(self):
        return f"<InputType(id={self.id}, name='{self.name}')>"
    