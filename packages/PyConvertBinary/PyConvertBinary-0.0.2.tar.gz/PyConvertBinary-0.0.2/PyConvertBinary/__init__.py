def DecToBin(num):
    List = []
    if isinstance(num, int):
        while num > 0:
            if num % 2 != 0:
                List.append('1')
            else:
                List.append('0')
            num = num // 2
        return ''.join(reversed(List))
    else:
        return 'Error'
def BinToDec(num):
    answer = 0
    if isinstance(num, int):
        num = ''.join(reversed(str(num)))
        for _ in range(len(num)):
            if num[_] == '1':
                answer += 2 ** _
            elif num[_] == '0':
                pass
        return answer
    else:
        return 'Error'

def DecToHex(num):
    Hexadecimal = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    remainder = []
    answer = []
    if isinstance(num, int):
        while num > 0:
            remainder.append(num % 16)
            num = num // 16
        for _ in remainder:
            answer.append(Hexadecimal[_-1])
        return ''.join(reversed(answer))
    else:
        return 'Error'