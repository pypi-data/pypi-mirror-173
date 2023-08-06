import inspect

from rich import print as rprint

results = {'passing': 0, 'failed': 0}
data = {}


def test(comment: str = '', args: dict = {}) -> None:
    def wrapper(func):
        data[func.__name__] = {
            'comment': comment,
            'func': func,
            'args': args
        }

    return wrapper


def run():
    for name, keys in data.items():
        comment = keys['comment'] if len(keys['comment']) > 0 else name + '()'
        function = keys['func']
        line = inspect.getsourcelines(function)[1]

        try:
            function(**keys['args'])

            results['passing'] += 1
            status = 'PASS'
            color = 'green'

        except AssertionError:
            results['failed'] += 1
            status = 'FAIL'
            color = 'red'

        rprint(f'[on {color}] {status} [/] {name}:{line} -> {comment}.')

    print('\nFailing: ' + str(results['failed']))
    print('Passed: ' + str(results['passing']))
