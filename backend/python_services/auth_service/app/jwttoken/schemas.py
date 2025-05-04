from pydantic import Field, ConfigDict
from core.schemas import BaseModel
  
  


class UpdateTokensIn(BaseModel):
    refresh_token : str 
    
    
    
    