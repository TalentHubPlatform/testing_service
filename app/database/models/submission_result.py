from mongoengine import Document, StringField, IntField, FloatField, ReferenceField, ObjectIdField


class SubmissionResult(Document):
    id = ObjectIdField(primary_key=True)
    submission_id = ReferenceField('Submission', required=True)
    test_case_id = ReferenceField('TestCase', required=True)
    status = StringField(required=True, max_length=50)
    execution_time = FloatField()
    memory_used = IntField()
    error = StringField()

    meta = {
        'collection': 'submission_results',
        'indexes': ['submission_id', 'test_case_id', 'status']
    }

    def __repr__(self):
        return f"<SubmissionResult(id={self.id}, submission_id={self.submission_id}, status='{self.status}')>"
