from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField, ObjectIdField
import datetime


class Submission(Document):
    id = ObjectIdField(primary_key=True)
    user_id = IntField(required=True)
    problem_id = ReferenceField('Problem', required=True)
    contest_id = ReferenceField('Contest', required=True)
    language = StringField(required=True, max_length=50)
    code = StringField(required=True)
    submitted_at = DateTimeField(default=datetime.datetime.now(datetime.UTC))
    submission_result_id = ReferenceField('SubmissionResult')

    meta = {
        'collection': 'submissions',
        'indexes': ['user_id', 'problem_id', 'contest_id', 'submitted_at']
    }

    def __repr__(self):
        return f"<Submission(id={self.id}, user_id={self.user_id})>"
