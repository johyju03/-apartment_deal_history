from app import db


# 10자리 법정동코드
class TestTable(db.Model):
    __tablename__ = 'test_table'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10))
