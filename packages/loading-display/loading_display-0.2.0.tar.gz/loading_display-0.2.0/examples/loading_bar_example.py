from loading_display import loading_bars
import time
from random import randint

max = 10
bar_count = 4
for i in range(0, max):
    bars_progress = [(i + randint(0, 2), max, f'Lorem {n}') for n in range(bar_count)]
    loading_bars(bars_progress,
                 bar_length=20,
                 show_percentage=True,
                 clear_when_done=False)
    time.sleep(0.2)
