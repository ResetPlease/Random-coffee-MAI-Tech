from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta



class VerificationSettings(BaseSettings):
    
    LIFETIME : timedelta
    
    model_config = SettingsConfigDict(
        env_prefix = 'VERIVICATE_',
        extra = 'ignore',
        frozen = True
    )
    
verification_settings = VerificationSettings()
