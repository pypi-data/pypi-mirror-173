__all__ = ['Job']


import typing as t

from ....base.type import Row

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from .command import Command


class Job:
    '''LSF job'''

    def __init__(self, item: Row[str]) -> None:
        self._item = item
        self._command = None

    def __repr__(self) -> str:
        return f'<Job #{self.id} named "{self.name}" {self.stat}@{self.queue} by {self.user}>'

    @classmethod
    def from_bjob(cls, item: Row[str]) -> 'Self':
        return cls(item)

    @classmethod
    def from_bjobs_with_command(cls, command: 'Command', *items: Row[str]) -> t.List['Self']:
        return [cls.from_bjob(item).set_command(command) for item in items]

    @property
    def command(self) -> 'Command':
        assert self._command is not None, 'Please call Job::set_command first'

        return self._command

    @property
    def id(self) -> str:
        return self._item['JOBID']

    @property
    def is_run(self) -> bool:
        return self.stat == 'RUN'

    @property
    def is_stop(self) -> bool:
        return self.stat == 'USUSP'

    @property
    def name(self) -> str:
        return self._item['JOB_NAME']

    @property
    def queue(self) -> str:
        return self._item['QUEUE']

    @property
    def stat(self) -> str:
        return self._item['STAT']

    @property
    def user(self) -> str:
        return self._item['USER']

    def set_command(self, command: 'Command') -> 'Self':
        self._command = command
        return self

    def kill(self, *args: str) -> str:
        return self.command.bkill(self.id, *args)

    def resume(self, *args: str) -> str:
        return self.command.bresume(self.id, *args)

    def stop(self, *args: str) -> str:
        return self.command.bstop(self.id, *args)
