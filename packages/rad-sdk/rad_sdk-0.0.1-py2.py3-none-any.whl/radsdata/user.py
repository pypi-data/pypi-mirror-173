from mongoengine import Document, EmailField, StringField, IntField, BooleanField


class MongoUser(Document):
    meta = {'collection': 'user'}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8, sensitive=True)
    organization_id = StringField(required=True)
    profile_type = IntField(required=True)
    is_verified = BooleanField(required=True, default=False)
    clear_password = StringField(required=False, min_length=8, sensitive=True, clear_before_save=True)
