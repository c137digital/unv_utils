import asyncio
import pytest

from unv.utils.tasks import TasksManager, Tasks, register, TaskRunError


class SimpleTasks(Tasks):
    NAMESPACE = 'simple'

    async def multiply_by_2(self, param):
        await asyncio.sleep(0.1)
        return param * 2

    @register
    async def example(self, *numbers):
        result = 0
        for number in numbers:
            result += await self.multiply_by_2(int(number))
        result += 2
        return result

    @register
    async def run(self):
        return await self._local('echo "test"')

    @register
    async def will_raise(self):
        return await self._local('asdf1_123_342f')


def test_tasks_register_and_run():
    manager = TasksManager()
    manager.register(SimpleTasks)

    assert 'simple' in manager.tasks

    result = manager.run('simple.example:2')
    assert result == 6

    result = manager.run('simple.example:20 simple.example')
    assert result == 2

    result = manager.run('simple.example')
    assert result == 2

    result = manager.run('simple.example:2,4')
    assert result == 14

    result = manager.run('simple.run')
    assert result == 'test\n'

    with pytest.raises(TaskRunError):
        manager.run('simple.will_raise')
