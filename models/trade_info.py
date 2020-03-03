from app import db


# 실거래 가격
class TradeInfo(db.Model):
    __tablename__ = 'trade_info'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.String(14))  # 일련번호
    trade_price = db.Column(db.String(10))  # 거래금액
    name= db.Column(db.String(128)) # 아파트명
    year = db.Column(db.String(4))  # 거래년도
    month = db.Column(db.String(2))  # 거래월
    day = db.Column(db.String(2))  # 거래일
    road_name = db.Column(db.String(32))  # 도로명
    si_gun_code = db.Column(db.String(5))  # 법정동시군구코드
    dong_code = db.Column(db.String(5))  # 법정동읍면동코드
    ep_area = db.Column(db.String(20))  # 전용면적
    floor = db.Column(db.Integer)  # 층수
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
    code_info = db.Column(db.String(10), db.ForeignKey('address_codes.code'), nullable=False)

    def __repr__(self):
        return 'serial_no = %s, trade_price = %s, ep_area =%s, updated_at = %s' % (
            self.serial_no, self.trade_price, self.ep_area, self.updated_at)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'serial_no': self.serial_no,
            'trade_price': self.trade_price,
            'date': self.year + '-' + self.month + '-' + self.day,
            'road_name': self.road_name,
            'ep_area': self.ep_area,
            'floor': self.floor,

        }
