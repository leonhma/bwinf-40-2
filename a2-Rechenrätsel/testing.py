from tqdm import tqdm
from program2 import generate_challenge
import re

test = 100
length = 5
failed = 0

for i, char in enumerate(pbar := tqdm(range(test))):
    challenge = generate_challenge(length)
    challenge = re.sub(r'[*+-/]', '◦', challenge[1:])
    pbar.write(f'testing on chalenge {challenge}')
    pbar.set_description("Processing %s" % char)
