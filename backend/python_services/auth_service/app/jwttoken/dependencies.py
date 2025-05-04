from .utils import (
                    JWTTokenRandomFields,
                    JWTTokensConcatenateUtils,
                    AccessTokenUtils,
                    RefreshTokenUtils,
                    JWTTokenActionsUtils
                )
from .dao import JWTTokenDAO, JWTTokenStorageDAO
from fastapi import Depends
from functools import lru_cache




@lru_cache
def get_jwttoken_utils() -> JWTTokensConcatenateUtils:
    from .config import jwtsettings
    
    random_fields_utils = JWTTokenRandomFields()
    access_token_utils = AccessTokenUtils(jwtsettings.ACCESS_TOKEN_TTL, jwtsettings.SECRET, jwtsettings.ALGORITHM)
    refresh_token_utils = RefreshTokenUtils(jwtsettings.REFRESH_TOKEN_TTL, jwtsettings.SECRET, jwtsettings.ALGORITHM)
    tokens_concatinate_utils = JWTTokensConcatenateUtils(access_token_utils, refresh_token_utils, random_fields_utils)
    return tokens_concatinate_utils



@lru_cache
def get_jwt_token_storage_dao() -> JWTTokenStorageDAO:
    return JWTTokenStorageDAO()


@lru_cache
def get_jwttoken_dao(
                        jwt_token_storage_dao : JWTTokenStorageDAO = Depends(get_jwt_token_storage_dao),
                        jwttoken_utils : JWTTokensConcatenateUtils = Depends(get_jwttoken_utils)
                    ) -> JWTTokenDAO:
    return JWTTokenDAO(jwttoken_utils.refresh.get_lifetime(), jwt_token_storage_dao)



@lru_cache
def get_jwttoken_action_utils(
                                jwttoken_dao : JWTTokenDAO = Depends(get_jwttoken_dao),
                                jwttoken_utils : JWTTokensConcatenateUtils = Depends(get_jwttoken_utils)
                            ) -> JWTTokenActionsUtils:
    return JWTTokenActionsUtils(jwttoken_utils, jwttoken_dao)