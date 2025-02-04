from fastapi import APIRouter, Depends, Request
from core.schemas import UserActionOut
from .dao import EmailVerifyDAO
from .schemas import SendEmailIn, VerifyCodeOut, VerifyCodeIn
from .errors import EmailVerifyException

router = APIRouter(
                    prefix = '/code',
                    tags = ['Checking the mail code'],
                    responses = EmailVerifyException.get_responses_schemas()
                )



@router.post(path = '/send', summary = 'Sending code')
async def send_mail(request : Request, form : SendEmailIn) -> UserActionOut:
    await EmailVerifyDAO.block_send_mails(email = form.email)
    await EmailVerifyDAO.send_mail(email = form.email)
    return UserActionOut()


@router.post(path = '/verify', summary = 'Verify code')
async def verify_code(request : Request, form : VerifyCodeIn) -> VerifyCodeOut:
    return await EmailVerifyDAO.verify_code(form = form)