from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, ObjectIdField


class TestCase(Document):
    id = ObjectIdField(primary_key=True)
    problem_id = ReferenceField('Problem', required=True)
    input_data = StringField()
    expected_output = StringField()
    weight = IntField(default=1)
    is_sample = BooleanField(default=False)

    meta = {
        'collection': 'test_cases',
        'indexes': ['problem_id', 'is_sample']
    }

    def __repr__(self):
        return f"<TestCase(id={self.id}, problem_id={self.problem_id}, is_sample={self.is_sample})>"
    