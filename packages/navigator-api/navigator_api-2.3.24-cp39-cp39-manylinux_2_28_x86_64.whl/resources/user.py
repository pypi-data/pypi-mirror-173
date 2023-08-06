from typing import Union
from datetime import datetime
from asyncdb.models import Model, Column
from navigator.conf import default_dsn, USERS_TABLE


class User(Model):
    """Basic User notation."""

    user_id: int = Column(required=False, primary_key=True)
    first_name: str
    last_name: str
    title: str
    email: str = Column(required=False, max=254)
    alternateemail: str
    password: str = Column(required=False, max=128)
    last_login: datetime = Column(required=False)
    username: str = Column(required=False)
    is_superuser: bool = Column(required=True, default=False)
    is_active: bool = Column(required=True, default=True)
    is_new: bool = Column(required=True, default=True)
    is_staff: bool = Column(required=True, default=False)
    title: str = Column(equired=False, max=90)
    registration_key: str = Column(equired=False, max=512)
    reset_pwd_key: str = Column(equired=False, max=512)
    date_joined: datetime = Column(required=False)
    birth_date: Union[datetime, str] = Column(required=False)
    avatar: str = Column(max=512)
    associate_id: str = Column(required=False)
    associateoid: str = Column(required=False)
    company: str
    department: str
    position_id: str
    group_id: list
    groups: list
    programs: list = Column(required=False)

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        driver = "pg"
        dsn: str = default_dsn
        name = USERS_TABLE
        schema = "public"
        strict = True
        frozen = False
        connection = None
