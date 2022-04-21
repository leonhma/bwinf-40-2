from re import findall, sub


def is_unique(challenge: str, /, progressbar=False, print_nonunique=True) -> bool:
    try:
        int(challenge[1])
    except ValueError:
        challenge = f'+{challenge}'

    previous = None
    body, res = sub(r'[*/+-]', '◦', challenge).split('=')

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
    
    while True:
        a = step()
        if not a: break
        # test if ops combination matches res and no non-int results
        combination = ''.join(nums[i//2] if i%2==0 else ops[(i-1)//2] for i in range(length*2+1))
        print(f'checking {combination}, {int(eval(combination))=}, {int(res)=}')
        if int(eval(combination)) == int(res):
            print('matching res')
            # body matches the result, now check for non-int results
            summands = findall(r'[+-].*?(?=[+-]|$)', challenge)
            for summand in summands:
                s, *dm = [summand[i]+summand[i+1] for i in range(0, len(summand)-1, 2)]
                while dm:
                    s = eval(f'{s}{dm.pop(0)}')
                    if not s%1:
                        if not previous:
                            previous = combination
                        else:
                            print(f'NOT UNIQUE: {challenge}! {previous}, {combination}')
                            return False
    return True

print(is_unique('3*4+3=15', progressbar=True))



    
