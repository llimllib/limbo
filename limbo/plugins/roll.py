"""!roll <n> - rolls a die of n sides"""
import random
import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!roll( .*)?", text)
    if not match:
        return
    num_sides = (match[0])
    try:
        num_sides = int(num_sides)
    except ValueError as e:
        num_sides = int(float(num_sides))
    if num_sides <= 1:
        return "impossible dice!"
    return str(random.choice([x for x in range(1, num_sides + 1)]))
