from django.core.exceptions import ValidationError


# def range_value_validator(value):
#     if not 0 <= value <= 10:
#         raise ValidationError("The rating must be between 0.0 and 10.0")


class RangeValueValidator:
    def __init__(self, min_value, max_value, message=None):
        self.min_value = min_value
        self.max_value = max_value

        if not message:
            self.message = f"The rating must be between {self.min_value:.1f} and {self.max_value:.1f}"
        else:
            self.message = message

    def __call__(self, value):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            "main_app.validators.RangeValueValidator",
            [self.min_value, self.max_value],
            {'message': self.message}
        )