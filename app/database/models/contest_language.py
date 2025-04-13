from mongoengine import Document, ReferenceField


class ContestLanguage(Document):
    contest_id = ReferenceField('Contest', required=True)
    language_id = ReferenceField('Language', required=True)

    meta = {
        'collection': 'contest_languages',
        'indexes': ['contest_id', 'language_id'],
        'unique_together': ['contest_id', 'language_id']
    }

    def __repr__(self):
        return f"<ContestLanguage(id={self.id}, contest_id={self.contest_id}, language_id={self.language_id})>"
