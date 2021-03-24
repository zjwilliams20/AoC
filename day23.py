#########################
# day 23
#########################


# initial_cups = [int(c) for c in '389125467'] # test
initial_cups = [int(c) for c in '643719258'] # real


def cupGame(cups, nMoves):

    def move(circBuff, current, last):
    
        # pick up three cups
        three = [circBuff[current], 
                circBuff[circBuff[current]], 
                circBuff[circBuff[circBuff[current]]]
                ]

        # remove three cups
        circBuff[current] = circBuff[three[-1]]

        # find the destination
        dest, i = current, 1
        while True:
            dest -= 1
            if dest == 0:
                dest = last
            if dest not in three:
                break

        # insert cups after destination
        circBuff[three[-1]] = circBuff[dest]
        circBuff[dest] = three[0]

        return circBuff[current]

    def linkList(cups):
        '''create a linked list from a list of cups, where the next number
           is the value at the current index
        '''

        circBuff = [0] * (max(cups)+1)
        for i, n in enumerate(cups[:-1]):
            circBuff[n] = cups[i+1]
        circBuff[cups[-1]] = cups[0]
        return circBuff
    
    circBuff = linkList(cups)
    current = cups[0]
    last = max(cups)

    for _ in range(nMoves):
        current = move(circBuff, current, last)
    
    cup = circBuff[1]
    while cup != 1:
        yield cup
        cup = circBuff[cup]


def unwrap(circBuff):

    num = 1
    ans = ''
    for _ in range(len(circBuff)-2):
        num = circBuff[num]
        ans = ''.join([ans, str(num)])
    return ans


# part 1
cupGen = cupGame(initial_cups, 100)
print(f"Part 1: {''.join([str(c) for c in cupGen])}")


# part 2
extended_cups = initial_cups.copy()
extended_cups.extend(range(max(extended_cups)+1, int(1_000_000)+1))
cupGen = cupGame(extended_cups, 10_000_000)
print(f'Part 2: {next(cupGen) * next(cupGen)}')
