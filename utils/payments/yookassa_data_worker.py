import json


async def form_provider_data(price: int) -> str:
    provider_data = {
        "receipt": {
            "items": [
                {
                    "description": "Подписка на месяц",
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