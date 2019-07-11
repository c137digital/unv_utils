import asyncio


def register(method):
    method.__task__ = True
    return method


class TaskRunError(Exception):
    pass


class SubprocessShellError(Exception):
    pass


async def run_subprocess_shell(command, interactive=False):
    stdout = stderr = asyncio.subprocess.PIPE
    if interactive:
        stdout = stderr = None
    proc = await asyncio.create_subprocess_shell(
        command, stdout=stdout, stderr=stderr
    )
    stdout, stderr = await proc.communicate()
    if stderr and proc.returncode != 0:
        raise SubprocessShellError(
            f'Command "{command}" finished with '
            f'error code [{proc.returncode}]:\n'
            f'{stderr.decode()} '
        )
    if stdout:
        return stdout.decode()


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
            return await run_subprocess_shell(command, interactive)
        except SubprocessShellError as err:
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
