from dataclasses import dataclass
from json import dumps

class Base:
    @staticmethod
    def default(obj: "Base"):
        return {
            **{
                attr: (getattr(obj, attr))
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            },
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Base.default, ensure_ascii=False)

@dataclass
class new_emailResult(Base):
    email: str

    @staticmethod
    def parse(email: str) -> "new_emailResult":
        return new_emailResult(
            email=email
        )
    



@dataclass
class inboxResult(Base):
    sender: str
    html: str
    subject: str
    message: str
    time: str

    @staticmethod
    def parse(data: dict) -> "inboxResult":
        return inboxResult(
            sender=data['sender'],
            html=data['html'],
            subject=data['subject'],
            message=data['message'],
            time=data['time']
        )
