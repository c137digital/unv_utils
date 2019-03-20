import asyncio

from unv.utils.tasks import TasksManager, TasksBase, register


class SimpleTasks(TasksBase):
    async def multiply(self, param):
        await asyncio.sleep(0.1)
        return param * 2

    @register
    async def example(self, number):
        result = await self.multiply(int(number))
        result += 2
        return result


def test_tasks_register_and_run():
    manager = TasksManager()
    manager.register(SimpleTasks)

    assert 'simple' in manager.tasks

    result = manager.run('simple.example 2')
    assert result == 6
