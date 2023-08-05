import math
import sys


def bars(progress: list,
         bar_length=10,
         show_percentage=False,
         icon='\u2588',
         clear_when_done=False):
    '''
    Prints out multiple loading bars (len(current_progress)).
    `progress` is a list of
    `(current_progress: int, total: int, label: string)` for each loading bar.
    The with of the loading bar
    in characters is based on `bar_length`.
    If `show_percentage` is `True`, the percentage with be added
    at the end of the loading bar.
    '''
    for cp in progress:
        bar(cp[0],
            total=cp[1],
            bar_length=bar_length,
            show_percentage=show_percentage,
            label=cp[2] if len(cp) > 2 else '',
            icon=icon)
        sys.stdout.write('\n')
        sys.stdout.flush()
    bars_done = [cp[0] >= cp[1] for cp in progress]
    all_done = len(list(set(bars_done))) == 1 and bars_done[0]
    if all_done and not clear_when_done:
        return
    for cp in progress:
        sys.stdout.write('\x1b[1A')
        if all_done and clear_when_done:
            print('\033[2K', end='')
        sys.stdout.flush()


def bar(current_progress: int,
        total=100,
        bar_length=10,
        show_percentage=False,
        label='',
        icon='\u2588'):
    '''
    Prints out a loading bar with the given loading progression
    based on `current_progress` and `total`. The with of the loading bar
    in characters is based on `bar_length`.
    If `show_percentage` is `True`, the percentage with be added
    at the end of the loading bar.
    '''
    percentage = current_progress / (total / 100)
    q = math.floor(percentage / (100 / bar_length))
    remaining = bar_length - q
    bar = f'{icon * min(q, bar_length)}{" "*remaining}'
    if show_percentage:
        bar += f' {round(percentage, 1)} %'
    print(f'\r{label} {bar}', end='')


def spinner(icons=["\u25DC ", " \u25DD", " \u25DE", "\u25DF "]):
    '''
    Returns a spinner Generator. 
    Pass the instance of this to next() to print the next frame of the spinner.
    '''
    current_index = 0
    while 1:
        if current_index >= len(icons) - 1:
            current_index = 0
        else:
            current_index += 1
        yield print(f'\r{icons[current_index]}', end='')
