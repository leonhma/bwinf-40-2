from re import findall, search, sub

from alive_progress import alive_bar

# from program import get_challenge


def is_unique(challenge: str, /, progressbar=False, print_nonunique=True) -> bool:
    try:
        int(challenge[1])
    except ValueError:
        challenge = f'+{challenge}'

    previous = None
    body, res = challenge.split('=')

    nums = [x for x in body if x in '123456789']
    length = len(nums)-1

    ops = [''] * length
    
    def step(i=0):
        if not ops[0]:
            for j in range(len(ops)):
                ops[j] = '+'
        elif ops[i] == '+':
            ops[i] = '-'
        elif ops[i] == '-':
            ops[i] = '*'
        elif ops[i] == '*':
            ops[i] = '/'
        elif ops[i] == '/':
            ops[i] = '+'
            if i+1<len(ops):
                res = step(i+1)
                if not res:  # propagate upwards
                    return False
            else:
                return False
        return True
    
    while step():
        # test if ops combination matches res and no non-int results
        combination = '+'+''.join(nums[i//2] if i%2==0 else ops[(i-1)//2] for i in range(length*2+1))
        if search(r'[/*]1', combination):
            continue
        if int(eval(combination)) == int(res):
            next_flag = False
            # body matches the result, now check for non-int results
            summands = findall(r'[+-].*?(?=[+-]|$)', combination)
            print(f'{summands=}')
            for summand in summands:
                s, *dm = [summand[i]+summand[i+1] for i in range(0, len(summand)-1, 2)]
                print(f'{s=} {dm=}')
                while dm:
                    s = float(eval(f'{s}{dm.pop(0)}'))
                    print(s)
                    if s%1:
                        print('not divisible by 1')
                        next_flag = True
                        break
                if next_flag: break
            if next_flag: continue
            if not previous:
                previous = combination
            else:
                print(f'NOT UNIQUE: {challenge}! {previous}, {combination}')
                return False
    return not not previous  # cast to bool

if __name__ == '__main__':
    with alive_bar(10000) as bar:
        for i in range(10000):
            challenge = get_challenge()
            if is_unique(challenge):
                bar() 
                bar.text = f'{(1-0.5**i)*100}%'
            else: break
