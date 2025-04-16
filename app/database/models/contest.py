from mongoengine import Document, StringField, IntField, BooleanField


class Contest(Document):
    DoesNotExist = None

    name = StringField(required=True, max_length=255)
    description = StringField()
    event_id = IntField()
    date_id = IntField()
    track_id = IntField()
    is_active = BooleanField(default=True)

    meta = {
        'collection': 'contests',
        'indexes': ['name', 'event_id', 'date_id', 'track_id', 'is_active']
    }

    def __repr__(self):
        return f"<Contest(id={self.id}, name='{self.name}')>"
