spis=[ (9, -5), (12, -1), (3, 0), (-9, 2), (1, -6), (11, 12), (-11, 12), (-5, 9), (5, 7), (7, 5)]
for i in range(len(spis)):
    a=spis[i]
    s=a[0]
    t=a[1]
    if s>5 or t>7:
        print('YES')
    else:
        print('NO')
