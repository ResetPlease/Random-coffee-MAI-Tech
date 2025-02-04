from core.dao.redis import RedisDAO
from redis.asyncio.client import Pipeline
from pydantic import PositiveInt
from .schemas import VerifyCodeOut, VerifyCodeIn
from .config import settings
from .errors import EmailBlockedError, MaxAttemptsError, UnknownEmailError
from worker.app.email import send_simple_email
import random



class EmailVerifyDAO(RedisDAO):
    
    _block_time : dict[int | None, int] = {
                                            None : settings.FIRST_BLOCK_TIME,
                                            b'1' : settings.SECOND_BLOCK_TIME,
                                            b'2' : settings.THIRD_BLOCK_TIME
                                        }
    
    @staticmethod
    def _is_blocked_now(ttl : int) -> bool:
        if ttl < 0:
            return False
        return (ttl - settings.KEY_AFTER_UNBLOCK_LIFETIME) >= 0
    
    
    def _generate_code() -> PositiveInt:
        min_value = 10 ** (settings.CODE_LENGTH - 1)
        max_value = (10 ** settings.CODE_LENGTH) - 1

        return random.randint(min_value, max_value)
    
    
    @classmethod
    @RedisDAO.get_pipeline()
    async def _delete_code(cls, pipeline : Pipeline, *, email : str) -> None:
        pipeline.multi()
        pipeline.delete(f'{email}:code', f'{email}:attempt_count')
        await pipeline.execute()
    
    
    @classmethod
    @RedisDAO.get_pipeline()
    async def block_send_mails(cls, pipeline : Pipeline, *, email : str) -> None:
        pipeline.multi()
        pipeline.get(f'{email}:block')
        pipeline.ttl(f'{email}:block')
        email_block_count, email_block_time = await pipeline.execute()
        
        if cls._is_blocked_now(email_block_time):
            raise EmailBlockedError
        
        pipeline.multi()
        new_block_time = cls._block_time.get(email_block_count, settings.THIRD_BLOCK_TIME)
        new_expire_time = new_block_time + settings.KEY_AFTER_UNBLOCK_LIFETIME
        pipeline.incrby(f'{email}:block')
        pipeline.expire(f'{email}:block', new_expire_time)
        await pipeline.execute()
        
        
    @classmethod
    @RedisDAO.get_pipeline()
    async def send_mail(cls, pipeline : Pipeline, *, email : str) -> None:
        pipeline.multi()
        code : PositiveInt = cls._generate_code()
        pipeline.set(f'{email}:code', code, settings.CODE_LIFETIME)
        pipeline.set(f'{email}:attempt_count', 0, settings.CODE_LIFETIME)
        await pipeline.execute()

        send_simple_email.delay(
                            smtp_server = settings.SMTP_SERVER,
                            smtp_port = settings.SMTP_PORT,
                            receiver_email = email,
                            login = settings.VERIFY_EMAIL_LOGIN,
                            password = settings.VERIFY_EMAIL_PASSWORD,
                            subject = f'{code} is your verification code',
                            html_body_file = open('./app/templates/email_verify.html', mode = 'r').read(),
                            html_boby_kwargs = {'code' : code, 'seconds' : settings.CODE_LIFETIME}
            
                        )
        
        
        
    @classmethod
    @RedisDAO.get_pipeline()
    async def verify_code(cls, pipeline : Pipeline, *, form : VerifyCodeIn) -> VerifyCodeOut:
        pipeline.multi()
        pipeline.get(f'{form.email}:code')
        pipeline.get(f'{form.email}:attempt_count')
        code, attempt_count = await pipeline.execute()
        
        if code is None or attempt_count is None:
            raise UnknownEmailError
        
        if int(attempt_count) >= settings.CODE_MAX_FAIL_ATTEMPT_COUNT:
            raise MaxAttemptsError
        
        if int(code) == form.code:
            return VerifyCodeOut(is_correct_code = True)
        
        pipeline.multi()
        pipeline.incrby(f'{form.email}:attempt_count')
        await pipeline.execute()
        return VerifyCodeOut(is_correct_code = False)
        
        
        
        
        
        
        
        
        
        
        
        