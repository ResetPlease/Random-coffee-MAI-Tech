from fastapi import APIRouter, Depends, Request
from .dao import VerifyingUserDAO
from .schemas import SendEmailIn, VerifyCodeOut, VerifyCodeIn, SendEmailOut
from .errors import EmailVerifyException
from .dependencies import get_email_verify_dao, get_email_verify_utils, get_code_send_limit, get_auth_verify_utils
from .utils import EmailVerifyUtils, AuthVerifyUtils
from core.dependencies.limiter import PersonalLimiter
import asyncio



router = APIRouter(
                    prefix = '/code',
                    tags = ['Checking the mail code'],
                    responses = EmailVerifyException.get_responses_schemas()
                )




@router.post(
                path = '/send',
                summary = 'Sending code',
                dependencies = [Depends(get_code_send_limit)]
            )
async def send_email(
                    form : SendEmailIn,
                    dao : VerifyingUserDAO = Depends(get_email_verify_dao),
                    utils : EmailVerifyUtils = Depends(get_email_verify_utils),
                    limiter : PersonalLimiter = Depends(get_code_send_limit)
                ) -> SendEmailOut:
    code, op_id = utils.generate_code(), utils.generate_operation_id()
    await asyncio.gather(
                            dao.save_code(email = form.email, code = code, operation_id = op_id),
                            utils.send_email_with_code(code, form.email)
                        )
    return SendEmailOut(operation_id = op_id, block_seconds = await limiter.get_next_block_time())



@router.post(path = '/verify', summary = 'Verify code')
async def verify_code(
                    form : VerifyCodeIn,
                    dao : VerifyingUserDAO = Depends(get_email_verify_dao),
                    auth_utils : AuthVerifyUtils = Depends(get_auth_verify_utils)
                ) -> VerifyCodeOut:
    is_correct_code = await dao.is_correct_code(form.email, form.code, form.operation_id)
    
    if is_correct_code:
        await asyncio.gather(
                            dao.delete_code(form.email),
                            auth_utils.notify_about_user(form.operation_id, form.email)
                        )
        
    return VerifyCodeOut(is_correct_code = is_correct_code)