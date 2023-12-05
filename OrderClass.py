import datetime
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class Order:
    time: datetime.date
    direction: str
    ticker: str
    strike: Decimal
    option_exp: datetime.date
    option_price: Decimal
    option_type: str
    timeframe: str
    comment: str
