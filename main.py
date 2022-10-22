from json import dump
from typing import List
import logging

from requests import get
from requests.exceptions import JSONDecodeError

logging.basicConfig(level=logging.INFO)


def write_to_json_file(data):
    with open("test.json", "w") as f:
        dump(data, f, indent=4, ensure_ascii=False)


def get_categories(store: str = "324G"):
    headers = {
        "Host": "5d.5ka.ru",
        "Accept": "application/json",
        "X-USER-STORE": store,
        "Accept-Language": "en-RU;q=1.0, ru-RU;q=0.9",
        "X-PACKAGE-NAME": "com.antimarket.pyaterochkadelivery",
        "User-Agent": "delivery_release/4.3.6 (com.antimarket.pyaterochkadelivery; build:1; iOS 16.0.0) Alamofire/5.6.1",
        "X-DEVICE-ID": "7406AAA7-D1B6-4326-8DD2-BFC75CE5CD2D",
        "X-APP-VERSION": "4.3.6",
        "X-PLATFORM": "ios",
        "X-CAN-RECEIVE-PUSH": "false",
    }

    resp = get(
        "https://5d.5ka.ru/api/cita/v5/categories/",
        headers=headers,
    )
    if resp.ok:
        try:
            return resp.json()
        except JSONDecodeError:
            return []


def get_category_products(
    category_id: int, offset: int = 0, store: str = "324G"
) -> List[dict]:
    headers = {
        "Host": "5d.5ka.ru",
        "Accept": "application/json",
        "X-USER-STORE": store,
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
        "limit": "100",
        "offset": f"{offset}",
    }

    resp = get(
        "https://5d.5ka.ru/api/cita/v1/products/",
        params=params,
        headers=headers,
    )
    if resp.ok:
        try:
            return resp.json()
        except JSONDecodeError:
            return []


def main():
    data = get_categories()
    for category in data:
        products = get_category_products(category["id"])
        write_to_json_file(products)
        input()


if __name__ == "__main__":
    main()
