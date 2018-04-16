from models import Model
from models.user import User
from utils import log


class Topic(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', str, 0),
            ('board_id', str, 0),
        ]
        return names

    @classmethod
    def find(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.all(topic_id=self.id)
        return ms

    def last(self):
        l_r = self.replies()[-1]
        return l_r


    def reply_count(self):
        count = len(self.replies())
        return count

    def board(self):
        from .board import Board
        m = Board.one(id=self.board_id)
        return m

    def user(self):
        # log('huifu3:', self.user_id)
        u = User.one(id=self.user_id)
        return u
