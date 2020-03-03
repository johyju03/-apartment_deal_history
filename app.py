from flask import Flask, render_template, jsonify, request
from xml.etree import ElementTree as ET
import requests

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config

app.config.from_object(config.DevelopmentConfig())
db = SQLAlchemy(app)

from models.code import AddressCodes
from models.trade_info import TradeInfo

db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/address/<address>')
def get_address(address):
    res = {}
    keyword = "%{}%".format(address)
    addr = AddressCodes.query.filter(AddressCodes.address_name.like(keyword)).all()

    res['codes'] = [t.serialize for t in addr]
    res['trade'] = []

    return jsonify(res)


@app.route('/trade')
def get_trades():
    # 법정동코드별 실거래 가격 조회
    if request.method == 'GET':

        year = request.args.get('year', None)
        month = request.args.get('month', None)
        address_cd = request.args.get('address_code', None)
        amount = request.args.get('amount', 10)
        page = request.args.get('page', 1)

        if year and month and address_cd:
            if amount != 'all':
                res = TradeInfo.query.filter(TradeInfo.year == year, TradeInfo.month == month.rjust(2, '0'),
                                             TradeInfo.code_info == address_cd).order_by(TradeInfo.day.desc()).paginate(
                    page=int(page), error_out=False, max_per_page=int(amount))

                return jsonify(
                    {
                        'has_next': res.has_next,
                        'has_prev': res.has_prev,
                        'next_num': res.next_num,
                        'prev_num': res.prev_num,
                        'items': [t.serialize for t in res.items]
                    })
            else:
                res = TradeInfo.query.filter(TradeInfo.year == year, TradeInfo.month == month.rjust(2, '0'),
                                             TradeInfo.code_info == address_cd).order_by(TradeInfo.day.desc()).all()

                return jsonify(
                    {
                        'has_next': None,
                        'has_prev': None,
                        'next_num': None,
                        'prev_num': None,
                        'items': [t.serialize for t in res]
                    })

    return jsonify({})


@app.route('/trade/update')
def update_trade_info():
    # 특정 년/월에 거래된 전체 실거래 내역 업데이트 (1회
    year = request.args.get('year', None)
    month = request.args.get('month', None)
    if year and month:
        codes = db.session.query(AddressCodes.parent_code).group_by(AddressCodes.parent_code).all()
        parent_codes = [code.parent_code for code in codes]
        request_url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
        for pc in parent_codes:
            params = {
                'ServiceKey': config.Config.DATA_SECRET_KEY,
                'LAWD_CD': pc,
                'pageNo': 1,
                'numOfRows': 9999,
                'DEAL_YMD': year + month.strip().rjust(2, '0')
            }

            res = requests.get(request_url, params=params)
            print(res.text)
            root = ET.fromstring(res.text)

            for item in root.iter('item'):
                try:
                    trade = TradeInfo()
                    trade.name = ("" if item.find('아파트') is None else item.find('아파트').text.strip())
                    trade.serial_no = ("" if item.find('일련번호') is None else item.find('일련번호').text.strip())
                    trade.trade_price = item.find('거래금액').text.strip()
                    trade.year = item.find('년').text.strip()
                    trade.month = item.find('월').text.strip().rjust(2, '0')
                    trade.day = item.find('일').text.strip().rjust(2, '0')
                    trade.road_name = ("" if item.find('도로명') is None else item.find('도로명').text.strip())
                    trade.si_gun_code = item.find('법정동시군구코드').text.strip()
                    trade.dong_code = item.find('법정동읍면동코드').text.strip()
                    trade.ep_area = ("" if item.find('전용면적') is None else item.find('전용면적').text.strip())
                    trade.floor = ("" if item.find('층') is None else item.find('층').text.strip())
                    trade.code_info = trade.si_gun_code + trade.dong_code
                except Exception as e:
                    print(e)
                    continue

                db.session.add(trade)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"errors": "commit 실패"})

        return jsonify(parent_codes)

    return jsonify({"errors": "parameter required (year, month)"})


if __name__ == '__main__':
    app.run()
