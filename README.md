# 월별 아파트 실거래가 조회

**공공데이터 오픈 API** 를 이용한 월별 아파트 실거래가 조회 사이트 구축 사이트입니다.

# 사용 스펙
- 사용 언어
> Python3.6
- DB
> MySQL 5.7

# 요구사항

1. DB에 업데이트할 **전체 법정동코드(지번주소) 파일**
 => 기본소스안에 포함되어져 있으나, 년 단위로 업데이트가 필요할 수 있습니다. ([https://www.code.go.kr/index.do](https://www.code.go.kr/index.do) 에서 다운가능)

2. 공공데이터 사이트(https://www.data.go.kr/)에서 해당 API 에 대한 **서비스 키** 발급
> 서비스명 : 아파트매매 실거래 상세 자료

## 구축순서
1. **DB 생성** 
> **'real_estate_trade_price'** 라는 이름으로 로컬에 DB 생성
2. **config.json 파일 생성** (첨부된 config_sample.json 양식 참조)

3.  app.py 파일을 실행하여, DB 내에 두 개의 테이블 생성
> 1) address_codes (주소조회 테이블), 
> 2) trade_info (실거래가 테이블)

4. **주소조회 테이블내에 데이터 삽입** (resource/주소데이터_업데이트쿼리.sql)

5.  **월별 실거래가 업데이트**
> app.py 실행 후에 
> (ex. [http://127.0.0.1:5000/trade/update?year=2020&month=3](http://127.0.0.1:5000/trade/update?year=2020&month=3)) 를 호출하여, 
> 해당 달에 대한 **지역별 아파트 실거래가** 업데이트

6. **사이트에서 조회**
