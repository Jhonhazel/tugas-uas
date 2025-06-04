import enum
from sqlalchemy import Enum

class PaymentStatus(enum.Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    REFUNDED= 'refunded'
    CANCELLED = 'cancelled'