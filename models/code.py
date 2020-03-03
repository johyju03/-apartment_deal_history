from app import db


# 10자리 법정동코드
class AddressCodes(db.Model):
    __tablename__ = 'address_codes'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    code = db.Column(db.String(10), primary_key=True)
    address_name = db.Column(db.String(128))
    parent_code = db.Column(db.String(5))
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    price_info = db.relationship('TradeInfo', backref='address_codes', lazy=True)

    def __repr__(self):
        return 'code = %s, name = %s, parent_code=%s, updated_at = %s' % (
            self.code, self.address_name, self.parent_code, self.updated_at)

    @property
    def serialize(self):
        return {
            'code': self.code,
            'address_name': self.address_name,
            'parent_code': self.parent_code,
            'updated_at': self.updated_at,
        }
