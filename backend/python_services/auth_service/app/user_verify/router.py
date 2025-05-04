from core.models.rabbitmq.auth import auth_verify_subscriber, AuthNotifyForm
from core.models.rabbitmq import rabbitmq_router
from fastapi import Depends
from .dependencies import get_user_verifying_dao, UserVerifyingDAO
from uuid import UUID






@auth_verify_subscriber
async def accept_user_email_verification(
                                        form : AuthNotifyForm,
                                        dao : UserVerifyingDAO = Depends(get_user_verifying_dao)
                                    ) -> None:
    await dao.save_user_verification(form.email, form.operation_id)

