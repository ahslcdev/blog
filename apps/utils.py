from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse

class CustomExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        errors = error_response.errors
        return {
            "errors":{
                "detalhes":[
                    {
                        "type": error_response.type,
                        "code": error.code,
                        "message": error.detail,
                        "field_name": error.attr
                    }
                    for error in errors
                ]
            }
        }