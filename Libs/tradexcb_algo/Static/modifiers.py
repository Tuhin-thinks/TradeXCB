
def fix_values(value, tick_size):
    return round(int(value / tick_size) * tick_size, len(str(tick_size)))
