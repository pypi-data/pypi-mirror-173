from loading_display import spinner
import time

a = spinner(icons=[
    '💻📨               🌑',
    '💻 📨              🌒',
    '💻  📨             🌓',
    '💻   📨            🌔',
    '💻    📨           🌕',
    '💻     📨          🌖',
    '💻      📨         🌗',
    '💻       📨        🌘',
    '💻        📨       🌑',
    '💻         📨      🌒',
    '💻          📨     🌓',
    '💻           📨    🌔',
    '💻            📨   🌕',
    '💻             📨  🌖',
    '💻              📨 🌗',
    '💻               📨🌘'])

while 1:
    next(a)
    time.sleep(0.1)
