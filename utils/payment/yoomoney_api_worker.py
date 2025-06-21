from data.config import PAYMENTS_YOOMONEY_TOKEN, PAYMENTS_YOOMONEY_RECEIVER
from yoomoney import Client, Quickpay


async def get_payment_link(label: str, price: int, message: str) -> str:
    quickpay = Quickpay(
        receiver=PAYMENTS_YOOMONEY_RECEIVER,
        quickpay_form="shop",
        targets=message,
        paymentType="SB",
        sum=float(price),
        label=label
    )
    return quickpay.redirected_url


async def check_payment(label: str) -> bool:
    client = Client(PAYMENTS_YOOMONEY_TOKEN)
    history = client.operation_history(label=label)
    if history.operations:
        return True
    else:
        return False
