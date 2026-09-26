class ZeroLength(BaseException):
    text = "{} has zero length"


class FromNone(BaseException):
    text = "Specify --from value"


class ToNone(BaseException):
    text = "Specify --to value"


class DifferentConverterCategory(BaseException):
    text = "Different converter category"
