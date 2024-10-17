import requests
import xml.etree.ElementTree as ET

def fetch_heat_wave_data(year, sido=None):
    base_url = "http://apis.data.go.kr/1741000/HeatWaveCasualtiesRegion/getHeatWaveCasualtiesRegionList"
    service_key = "xcNU53U9YdUn5pLf5lNivK23JZffteYY62BPnk7Dyp2moHUdkthuXkZdb8sXXM8Xj6PFGUDGG3f/85QoiBBJCg=="

    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "20",
        "type": "xml",
        "bas_yy": str(year)
    }
    if sido:
        params["sidoNm"] = sido

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        root = ET.fromstring(response.content)
        
        # 결과 코드 확인
        result = root.find(".//RESULT")
        if result is not None:
            result_code = result.find('resultCode').text
            result_msg = result.find('resultMsg').text
            if result_code != "INFO-0":
                print(f"API 오류: {result_msg}")
                return []

        # 데이터 개수 확인
        total_count = int(root.find(".//totalCount").text)
        if total_count == 0:
            print(f"{year}년 데이터가 없습니다.")
            return []

        data = []
        for item in root.findall(".//row"):
            data.append({
                "year": item.find('bas_yy').text,
                "region": item.find('regi').text,
                "total": item.find('tot').text,
                "outdoor": {
                    "total": item.find('otdoor_subtot').text,
                    "workplace": item.find('otdoor_otdoor_wrkpl').text,
                    "field": item.find('otdoor_field').text,
                    "farmland": item.find('otdoor_farmland').text,
                    "mountain": item.find('otdoor_mountain').text,
                    "river": item.find('otdoor_river').text,
                    "road": item.find('otdoor_road').text,
                    "residential": item.find('otdoor_resarea_arund').text,
                    "other": item.find('otdoor_etc').text
                },
                "indoor": {
                    "total": item.find('indoor_subtot').text,
                    "house": item.find('indoor_house').text,
                    "building": item.find('indoor_bildg').text,
                    "workplace": item.find('indoor_wrkpl').text,
                    "greenhouse": item.find('indoor_greenhouse').text,
                    "other": item.find('indoor_etc').text
                }
            })
        
        # 요청한 연도와 반환된 데이터의 연도 일치 여부 확인
        if data and data[0]['year'] != str(year):
            print(f"요청한 연도({year})와 반환된 데이터의 연도({data[0]['year']})가 일치하지 않습니다.")
            return []
        
        print(f"Fetched data: {data}")  # 디버깅을 위한 출력
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        return []
    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
        return []
    except Exception as e:
        print(f"데이터 가져오기 오류: {e}")
        return []