from mongoengine import (
    Document, StringField, IntField, ReferenceField,
    FloatField, ObjectIdField
)


class Problem(Document):
    DoesNotExist = None
    title = StringField(required=True, max_length=255)
    description = StringField()
    contest_id = ReferenceField('Contest', required=True)
    input_type_id = ReferenceField('InputType')
    output_type_id = ReferenceField('OutputType')
    time_limit = FloatField(default=1.0)
    memory_limit = IntField(default=256)

    meta = {
        'collection': 'problems',
        'indexes': ['contest_id', 'title']
    }

    def __repr__(self):
        return f"<Problem(id={self.id}, title='{self.title}')>"
    