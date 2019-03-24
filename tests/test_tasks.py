import asyncio
import pytest

from unv.utils.tasks import (
    TasksManager, TasksBase, register, TaskSubprocessError
)


class SimpleTasks(TasksBase):
    async def multiply_by_2(self, param):
        await asyncio.sleep(0.1)
        return param * 2

    @register
    async def example(self, *numbers):
        if 'value' in self.storage:
            return self.storage['value'] + 10

        result = 0
        for number in numbers:
            result += await self.multiply_by_2(int(number))
        result += 2
        return result

    @register
    async def run(self):
        return await self.subprocess('echo "test"')

    @register
    async def modify(self, value):
        self.storage['value'] = int(value)

    @register
    async def will_raise(self):
        return await self.subprocess('asdf1_123_342f')


def test_tasks_register_and_run():
    manager = TasksManager()
    manager.register(SimpleTasks)

    assert 'simple' in manager.tasks

    result = manager.run('simple.example:2')
    assert result == 6

    result = manager.run('simple.example:20 simple.example')
    assert result == 2

    result = manager.run('simple.modify:20 simple.example')
    assert result == 30

    result = manager.run('simple.example')
    assert result == 2

    result = manager.run('simple.example:2,4')
    assert result == 14

    result = manager.run('simple.run')
    assert result == 'test\n'

    with pytest.raises(TaskSubprocessError):
        manager.run('simple.will_raise')
