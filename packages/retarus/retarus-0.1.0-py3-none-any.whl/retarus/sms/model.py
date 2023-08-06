from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, validator
from ..base.utils import to_camel_case


class Options(BaseModel):
    src: Optional[str]
    encoding: Optional[str]
    billcode: Optional[str]
    status_requested: Optional[bool]
    flash: Optional[bool]
    customer_ref: Optional[str]
    validity_min: Optional[int]
    max_parts: Optional[int]
    invalid_characters: Optional[str]
    qos: Optional[str]
    job_period: Optional[str]
    duplicate_detection: Optional[bool]
    blackout_periods: Optional[List[str]]

    class Config:
        alias_generator = to_camel_case


class Recipient(BaseModel):
    dst: str
    customer_ref: Optional[str]
    blackout_periods: Optional[List[str]]

    class Config:
        alias_generator = to_camel_case


class Messages(BaseModel):
    text: str
    recipients: List[Recipient]

    @validator("text")
    def check_text_length(cls, v):
        if len(v) > 160:
            raise ValueError(f"Following message is to long, there is a limit 160 character per job: {v}")


class SmsJob(BaseModel):
    """
    Create an instance of a SmsJob, set all your needed properties and dispatch it to the Retarus server to send it.

    options: Set special properties how the sms should be processed.
    messages*: set your message that you want to send.
    """
    options: Optional[Options]
    messages: List[Messages]

    class Config:
        alias_generator = to_camel_case

    def exclude_optional_dict(model: BaseModel):
        return {**model.dict(exclude_unset=True), **model.dict(exclude_none=True)}


class JobReport(BaseModel):
    job_id: str
    src: str
    encoding: str
    billcode: str
    status_requested: bool
    flash: bool
    validity_min: int
    customer_ref: str
    qos: str
    receipt_ts: str
    finished_ts: str
    recipient_ids: List[str]

    class Config:
        alias_generator = to_camel_case


class Client(object):
    def send_sms(self, sms: SmsJob):
        pass

    def get_sms_jobs(self, job_id: str) -> dict:
        pass

    def filter_sms_jobs(self, *args, **kwargs):
        """
        Gets all fax reports that match the given criteria.

        Parameters:
        job_ids_only: bool
        from_ts: str (e.g. 2018-06-13T00:00+02:00) can only be max 30 days before to_ts
        to_ts: str (e.g. 2018-06-20T00:00+02:00)
        open: bool
        offset: int (default: 0)
        limit: int (default: 100)
        """
        pass

    def server_version(self):
        pass
