import json


# пока не использую эту штуку, так как решил отказаться от автоотправки чеков в налоговую, потом посмотрим
async def form_provider_data(price: int) -> str:
    provider_data = {
        "receipt": {
            "items": [
                {
                    "description": f"Пополнение баланса на {price}₽",
                    "quantity": "1.00",
                    "amount": {
                        "value": f"{price}",
                        "currency": 'RUB'
                    },
                    "vat_code": 1
                }
            ]
        }
    }

    return json.dumps(provider_data)