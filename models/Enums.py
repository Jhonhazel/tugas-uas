import enum
from sqlalchemy import Enum as SQLAlchemyEnum

class PaymentStatusEnum(enum.Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    REFUNDED= 'refunded'
    CANCELLED = 'cancelled'

DbPaymentStatusEnum = SQLAlchemyEnum(PaymentStatusEnum, name="payment_status_enum")
DbPaymentInfoStatusEnum = SQLAlchemyEnum(PaymentStatusEnum, name="payment_info_status_enum")