from app import db
import uuid
from sqlalchemy.dialects.postgresql import JSON, UUID

class Result(db.Model):
    __tablename__ = 'test'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = db.Column(db.String())
    # result_all = db.Column(JSON)
    # result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        # self.result_all = result_all
        # self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)

# class Photo(db.Model):
#     __tablename__ = 'photo'

#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
#     url = db.Column(db.String())
#     # result_all = db.Column(JSON)
#     # result_no_stop_words = db.Column(JSON)

#     def __init__(self, url, result_all, result_no_stop_words):
#         self.url = url
#         # self.result_all = result_all
#         # self.result_no_stop_words = result_no_stop_words

#     def __repr__(self):
#         return '<id {}>'.format(self.id)