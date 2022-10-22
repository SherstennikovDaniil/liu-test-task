# Парсинг приложения `Пятёрочка Доставка`

### Этапы выполнения:
* Отсиффать запросы
* Спарсить :)

## Сниффинг

Чтобы записать запросы мобильного приложения я предпочитаю `Charles Proxy` и уcтановленное приложение на iPhone.

После установки приложения и включения проксирования, я запустил приложение и открыл пару категорий.

По итогу было найдено 2 endpoint'a, предоставляющих информацию в формате JSON:

* https://5d.5ka.ru/api/cita/v5/categories/
   
   Данный endpoint предоставляет список доступных категорий формата:
   ```
    [
        {
            "id": id объекта,
            "name": название объекта,
            "type": тип объекта,
            "description": описание,
            "subtitle": подзаголовок,
            ...
            *различные метаданные*
            ...
            "products_count": количество товаров в категории,
            "subcategories": [список подкатегорий]
        },
        ...
    ]
   ```
* https://5d.5ka.ru/api/cita/v1/products/
  
  Данный endpoint предоставляет информацию о доступных в категории товарах в формате:
  ```
    [
        "filters": [список доступных фильтров],
        "products": [
        {
            "plu": id товара,
            "name": название товара,
            "image_small": ссылка на изображение,
            "prices": {
                "price_regular": обычная цена,
                "price_discount": цена по скидке,
                "discount": размер скидки
            },
            "promo": {
                данные об акции
            },
            "is_new": новый ли товар,
            "uom": мера измерения,
            "step": шаг,
            "average_rating": средняя оценка,
            "rates_count_in_period": количество оценок за период,
        },
        ...
        ]
    ]
  ```
## Написание парсера
Сначала я сконвертировал запросы из `Charles Proxy` из `CURL` в `Python` с помощью [curl2python](https://curlconverter.com).

После было реализовано 2 функции:
* [`get_categories`](https://github.com/SherstennikovDaniil/liu-test-task/blob/main/main.py#LC70) - возвращает список категорий
* [`get_products`](https://github.com/SherstennikovDaniil/liu-test-task/blob/main/main.py#LC96) - возвращает список товаров в категории