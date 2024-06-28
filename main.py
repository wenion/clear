from redis_om import Migrator, get_redis_connection
from redis_om import Field, JsonModel, EmbeddedJsonModel
from pydantic import NonNegativeInt
from typing import Optional
import csv
from datetime import datetime
import argparse
import re
import os


class Result(JsonModel):
    class Meta:
        global_key_prefix = 'h'
        model_key_prefix = 'Result'
    title: str = Field(index=True)
    url: str = Field(index=True)
    summary: Optional[str] #= Field(index=True, full_text_search=True, default="")
    highlights: Optional[str] #= Field(index=True, full_text_search=True, default="")



class UserRole(EmbeddedJsonModel):
    class Meta:
        global_key_prefix = 'h'
        model_key_prefix = 'UserRole'
    userid: str = Field(index=True)
    faculty: str = Field(index=True)
    teaching_role: str = Field(index=True)
    teaching_unit: str = Field(index=True)
    campus: Optional[str] = Field(full_text_search=True, sortable=True)
    joined_year: NonNegativeInt = Field(index=True)
    years_of_experience: NonNegativeInt = Field(index=True)
    expert: NonNegativeInt = Field(index=True)


class UserEvent(JsonModel):
    class Meta:
        global_key_prefix = 'h'
        model_key_prefix = 'UserEvent'
    event_type: str = Field(index=True, full_text_search=True)
    timestamp: int = Field(index=True)
    tag_name: str = Field(index=True)
    text_content: str = Field(index=True)
    base_url: str = Field(index=True)
    userid: str = Field(index=True)
    ip_address: Optional[str] = Field(full_text_search=True, sortable=True)
    interaction_context: Optional[str] = Field(full_text_search=True, sortable=True)
    event_source: Optional[str] = Field(full_text_search=True, sortable=True)
    system_time: Optional[datetime]
    x_path: Optional[str] = Field(full_text_search=True, sortable=True)
    offset_x: Optional[float] = Field(full_text_search=True, sortable=True)
    offset_y: Optional[float] = Field(full_text_search=True, sortable=True)
    doc_id: Optional[str] = Field(full_text_search=True, sortable=True)
    region: Optional[str] = Field(index=True, default="Australia/Sydney")
    session_id: Optional[str] = Field(full_text_search=True, sortable=True)
    task_name: Optional[str] = Field(full_text_search=True, sortable=True)
    width: Optional[int] = Field(full_text_search=True, sortable=True)
    height: Optional[int] = Field(full_text_search=True, sortable=True)
    image: Optional[str]
    title: Optional[str] = Field(full_text_search=True, sortable=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clear')
    parser.add_argument('name', type=str, help='User id', nargs='?', const='')

    args = parser.parse_args()

    print(args.name)

    Migrator().run()

    users = UserRole.find().all()
    for u in users:
        print(u)

    if args.name:
        events = UserEvent.find(UserEvent.userid == args.name).all()
        count = UserEvent.find(UserEvent.userid == args.name).count()
        # for e in events:
        #     UserEvent.delete(e.pk)

        print('all count', count)
    