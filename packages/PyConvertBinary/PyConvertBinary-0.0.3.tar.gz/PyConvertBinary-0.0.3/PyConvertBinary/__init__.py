Hexadecimal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
def DecToBin(num):
    List = []
    try:
        if isinstance(num, float):
            return 'Error'
        num = int(num)
        while num > 0:
            if num % 2 != 0:
                List.append('1')
            else:
                List.append('0')
            num = num // 2
        return ''.join(reversed(List))
    except ValueError:
        return 'Error'

def BinToDec(num):
    answer = 0
    if isinstance(num, float):
        return 'Error'
    num = ''.join(reversed(str(num)))
    for _ in range(len(num)):
        if num[_] == '1':
            answer += 2 ** _
        elif num[_] == '0':
            pass
        else:
            return 'Error'
    return answer

def DecToHex(num):
    remainder = []
    answer = []
    if isinstance(num, int):
        while num > 0:
            remainder.append(num % 16)
            num = num // 16
        for _ in remainder:
            answer.append(Hexadecimal[_])
        return ''.join(reversed(answer))
    else:
        return 'Error'

def HexToDec(num):
    num = ''.join(reversed(str(num)))
    count = 0
    answer = 0
    if isinstance(num, str):
        for _ in num:
            if _ in Hexadecimal:
                answer += (Hexadecimal.index(_)*16**count)
                count += 1
            else:
                return 'Error'
    else:
        return 'Error'
    return answer