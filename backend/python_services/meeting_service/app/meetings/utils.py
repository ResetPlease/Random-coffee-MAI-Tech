from core.utils import BaseServiceUtils
from core.dao.http import HTTPRequest, HTTPMethod
from core.schemas import UserID, DateTimeIntervalIn
from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from .schemas import PublicUserInfoOut, MeetingOut, DateTimeIntervalOut
from core.models.postgres import MeetingDB, MeetingMemberDB







class MeetingUtils(BaseServiceUtils):
    
    __slots__ = ('match_endpoint', 'match_endpoint_method')
    
    
    def __init__(
                self, 
                requester : HTTPRequest,
                service_name : str, 
                service_port : int,
                match_endpoint : str,
                match_endpoint_method : HTTPMethod
            ) -> None:
        self.match_endpoint = match_endpoint
        self.match_endpoint_method = match_endpoint_method
        super().__init__(requester, service_name, service_port)
        

    async def can_two_users_start_meeting(
                                            self,
                                            creater_user_id : UserID, 
                                            user_id : UserID,
                                            meeting_interval : DateTimeIntervalIn
                                        ) -> BaseHTTPException | None:
        response = await self.requester.request(
                                    method = self.match_endpoint_method,
                                    server = self.service_name, 
                                    port = self.service_port, 
                                    endpoint = self.match_endpoint,
                                    body = {
                                        'meeting_datetime' : meeting_interval.model_dump(mode = 'json'),
                                        'searcher_user_id' : creater_user_id,
                                        'active_user_id' : user_id
                                    }
                                )
        
        if response.status != 200:
            response_json = await response.json()
            return BaseHTTPException(
                                        status_code = response.status,
                                        detail = BaseHTTPExceptionModel.model_validate(response_json['detail']),
                                        headers = response.headers,
                                        need_registrate = False
                                )
        
    @staticmethod
    def cast_meetings_to_response(
                                user_meetings : list[MeetingDB]
                            ) -> list[MeetingOut]:
        meetings = [
                        MeetingOut(
                                    meeting_id = meeting.id,
                                    status = meeting.status,
                                    meeting_datetime = DateTimeIntervalOut(
                                                                            start = meeting.meeting_datetime_start,
                                                                            end = meeting.meeting_datetime_end
                                                                        ),
                                    created_at = meeting.created_at, 
                                    users = [PublicUserInfoOut.model_validate(member.user) for member in meeting.members]
                                ) 
                        for meeting in user_meetings
                ]
        
        return meetings