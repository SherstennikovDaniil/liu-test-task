from json import dump

from requests import get


def write_to_json_file(data):
    with open("test.json", "w") as f:
        dump(data, f, indent=4, ensure_ascii=False)


def get_category_info(category_id: int, offset: int = 0) -> dict | None:
    url = "https://5d.5ka.ru/api/cita/v4/categories/preview/"

    headers = {
        "Host": "5d.5ka.ru",
        "Accept": "application/json",
        "X-USER-STORE": "324G",
        "Accept-Language": "en-RU;q=1.0, ru-RU;q=0.9",
        "X-PACKAGE-NAME": "com.antimarket.pyaterochkadelivery",
        "User-Agent": "delivery_release/4.3.6 (com.antimarket.pyaterochkadelivery; build:1; iOS 16.0.0) Alamofire/5.6.1",
        "X-DEVICE-ID": "7406AAA7-D1B6-4326-8DD2-BFC75CE5CD2D",
        "X-APP-VERSION": "4.3.6",
        "X-PLATFORM": "ios",
        "X-CAN-RECEIVE-PUSH": "false",
    }
    params = {
        "category": f"{category_id}",
        "is_new": "0",
        "is_promo": "0",
        "offset": f"{offset}",
        "rating_order": "average_rating_desc",
    }

    resp = get(
        url,
        params=params,
        # cookies=cookies,
        headers=headers,
    )
    print(resp.text)
    print(resp.status_code)

    if resp.ok:
        return resp.json()
    else:
        return None


if __name__ == "__main__":
    data = get_category_info(716)
    write_to_json_file(data)
