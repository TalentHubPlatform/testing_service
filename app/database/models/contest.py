from mongoengine import Document, StringField, IntField, ObjectIdField


class Contest(Document):
    DoesNotExist = None
    id = ObjectIdField(primary_key=True)
    name = StringField(required=True, max_length=255)
    description = StringField()
    event_id = IntField()
    date_id = IntField()

    meta = {
        'collection': 'contests',
        'indexes': ['name', 'event_id', 'date_id']
    }

    def __repr__(self):
        return f"<Contest(id={self.id}, name='{self.name}')>"
