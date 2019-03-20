import asyncio
import pytest

from unv.utils.tasks import (
    TasksManager, TasksBase, register, TaskSubprocessError
)


class SimpleTasks(TasksBase):
    async def multiply(self, param):
        await asyncio.sleep(0.1)
        return param * 2

    @register
    async def example(self, number):
        result = await self.multiply(int(number))
        result += 2
        return result

    @register
    async def run(self):
        return await self.subprocess('echo "test"')

    @register
    async def will_raise(self):
        return await self.subprocess('asdf1_123_342f')


def test_tasks_register_and_run():
    manager = TasksManager()
    manager.register(SimpleTasks)

    assert 'simple' in manager.tasks

    result = manager.run('simple.example 2')
    assert result == 6

    result = manager.run('simple.run')
    assert result == 'test\n'

    with pytest.raises(TaskSubprocessError):
        manager.run('simple.will_raise')
