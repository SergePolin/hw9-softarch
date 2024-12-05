from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

@dataclass
class Message:
    content: str
    created_at: datetime

class Filter(Process, ABC):
    def __init__(self, outputs: list[Queue]):
        super().__init__()
        self.input = Queue()
        self.outputs = outputs

    @abstractmethod
    def _process(self, content: str) -> str:
        raise NotImplementedError

    def run(self) -> None:
        while True:
            data = self.input.get()
            lag = (datetime.now() - data.created_at).total_seconds() * 1000
            print(self.__class__.__name__, f'{lag}ms')
            
            processed_content = self._process(data.content)
            
            for output in self.outputs:
                output.put(Message(
                    content=processed_content,
                    created_at=data.created_at
                )) 