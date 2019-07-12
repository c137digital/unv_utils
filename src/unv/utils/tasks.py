import asyncio

from .os import run_in_shell, RunInShellError


def register(method):
    method.__task__ = True
    return method


class TaskRunError(Exception):
    pass


class Tasks:
    NAMESPACE = ''

    def __init__(self, manager):
        self._manager = manager

    @classmethod
    def get_namespace(cls):
        namespace = cls.NAMESPACE
        if not namespace:
            raise ValueError('Please define NAMESPACE for {}'.format(cls))
        return namespace

    @staticmethod
    async def _local(command, interactive=False):
        try:
            return await run_in_shell(command, interactive)
        except RunInShellError as err:
            raise TaskRunError(err)


class TasksManager:
    def __init__(self):
        self.tasks = {}

    def register(self, task_class):
        self.tasks[task_class.get_namespace()] = task_class

    def run_task(self, task_class, name, args):
        task = getattr(task_class(self), name)
        return asyncio.run(task(*args))

    def run(self, commands):
        commands = commands.split()
        for index, command in enumerate(commands, start=1):
            namespace, name = command.split('.')

            task_class = self.tasks[namespace]
            args = []
            if ':' in name:
                name, task_args = name.split(':')
                args = task_args.split(',')

            method = getattr(task_class, name)
            if getattr(method, '__task__', None) and name == method.__name__:
                result = self.run_task(task_class, name, args)
                if index == len(commands):
                    return result
