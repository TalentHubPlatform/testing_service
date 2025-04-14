from mongoengine import Document, IntField, ReferenceField, ObjectIdField


class ContestResult(Document):
    DoesNotExist = None
    id = ObjectIdField(primary_key=True)
    contest_id = ReferenceField('Contest', required=True)
    user_id = IntField(required=True)
    total_score = IntField(default=0)
    solved_score = IntField(default=0)
    penalty = IntField(default=0)

    meta = {
        'collection': 'contest_results',
        'indexes': ['contest_id', 'user_id', 'total_score'],
        'unique_together': ['contest_id', 'user_id']
    }

    def __repr__(self):
        return (f"<ContestResult(id={self.id}, contest_id={self.contest_id}, user_id={self.user_id}, "
                f"total_score={self.total_score})>")
    
