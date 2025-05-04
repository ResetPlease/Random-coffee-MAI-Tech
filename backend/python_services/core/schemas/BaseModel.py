from pydantic import BaseModel as __BaseModel, ConfigDict
from typing import Any



class BaseModel(__BaseModel):
    
    model_config = ConfigDict(frozen = True, from_attributes = True, extra = 'ignore')
    
    
    def model_dump(self, **kwargs) -> dict[str, Any]:
        return super().model_dump(**kwargs, by_alias = True)
    
    
    