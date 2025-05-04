from typing import TypeAlias, Annotated, Self, Any
import annotated_types
from pydantic import AfterValidator, model_validator, BeforeValidator
import re
from datetime import datetime
from .BaseModel import BaseModel
import logging




def xss_injection_validate(field : str) -> str:
    xss_patterns = [
        r'<\s*script.*?>.*?<\s*/\s*script\s*>',
        r'<\s*(iframe|img|svg|meta|body|input|link|style|div|a|form|button)\W.*?>',
        r'<[^>]*\s(on\w+)\s*=\s*["\']?[^"\'<>]*["\']?[^>]*>',
        r'javascript:\s*\S+',
        r'data:\s*(text/html|text/javascript|application/x-shockwave-flash)',
        r'eval\s*\('
    ]
    
    for pattern in xss_patterns:
        if re.search(pattern, field, re.IGNORECASE):
            raise ValueError('XSS threat detected in the entered data')
    return field


def string_whitespace_valid(field : Any) -> str:
    if not isinstance(field, str):
        raise ValueError('incorrect type')
    
    field = field.strip()
    if len(field) == 0:
        raise ValueError('incorrect field lenght')
    return field
    


def correct_time(time : datetime) -> datetime:
    time = time.replace(minute = 0, second = 0, microsecond = 0, tzinfo=None)
    if time < datetime.now():
        raise ValueError('Time has passed')
    return time




     
CorrectDateTimeType : TypeAlias = Annotated[datetime, AfterValidator(correct_time)]

MeetingID : TypeAlias = Annotated[int, annotated_types.Ge(1), annotated_types.Lt(2**32)]
TagID : TypeAlias = Annotated[int, annotated_types.Ge(1), annotated_types.Lt(2**32)]
UserID : TypeAlias = Annotated[int, annotated_types.Ge(1), annotated_types.Lt(2**32)]
Str : TypeAlias = Annotated[str, BeforeValidator(string_whitespace_valid)]
StrXSS : TypeAlias = Annotated[Str, AfterValidator(xss_injection_validate)]


class DateTimeIntervalOut(BaseModel):
    start : datetime
    end : datetime
    

class DateTimeIntervalIn(BaseModel):
    start : CorrectDateTimeType
    end : CorrectDateTimeType
    
    @model_validator(mode = 'after')
    def correct_time_interval(self) -> Self:
        if self.start >= self.end:
            raise ValueError('The end time cannot be more starting')
        return self
    
    
    
    
    
    