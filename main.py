import csv
import logging
from datetime import datetime
from typing import Any, Dict, List, TypedDict

from requests import get
from requests.exceptions import JSONDecodeError

CSV_HEADERS = [
    "Название",
    "Цена",
    "Размер скидки",
    "Мера веса/объема/цена за указанную меру",
    "Старая цена",
    "Ссылка на картинку",
]


class Product(TypedDict):
    name: str
    price: float
    discount: float
    unit: str
    old_price: float
    image_link: str


logging.basicConfig(level=logging.INFO)


def write_to_csv(
    name: str, data: List[Product], header: List[str] = CSV_HEADERS
) -> None:
    with open(f"{name}-{datetime.now()}.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        for row in data:
            writer.writerow(
                [
                    row["name"],
                    row["price"],
                    row["discount"],
                    f'1 {row["unit"]}',
                    row["old_price"],
                    row["image_link"],
                ]
            )


def process_products(products: List[Dict[Any, Any]]) -> List[Product]:
    result = []
    for product in products:
        prices = product["prices"]
        discount = prices["discount"]
        # price_discount
        prod = Product(
            name=product["name"],
            price=prices["price_discount"]
            if discount
            else prices["price_regular"],
            discount=discount if discount else 0.0,
            unit=product["uom"],
            old_price=prices["price_regular"],
            image_link=product["image_small"],
        )
        result.append(prod)
    return result


def get_categories(store: str = "324G") -> List[Dict[Any, Any]] | None:
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
            return None
    return None


def get_category_products(
    category_id: int, offset: int = 0, store: str = "324G"
) -> List[Dict[Any, Any]] | None:
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
            products = resp.json()
            return products.get("products")
        except JSONDecodeError:
            return None
    return None


def main():
    data = get_categories()
    if not data:
        logging.error("Error while parsing categories")
        return

    for category in data:
        items = category.get("products_count")
        if not items:
            continue
        logging.info(f" Category: {category.get('name')}, items: {items}")

        products = []
        for offset in range(0, items, 100):
            tmp_products = get_category_products(category["id"], offset)
            if not tmp_products:
                logging.error("Error while parsing products")
                continue
            products.extend(tmp_products)

        products = process_products(products)
        write_to_csv(category["name"], products)


if __name__ == "__main__":
    main()
