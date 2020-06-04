import numpy as np

def counting_cost(mapping):
    ver_cost = 0
    hor_cost = 0
    for i in range(mapping.shape[0] - 1):
        for j in range(mapping.shape[0] - 1):
            ver_cost += abs(mapping[i][j] - mapping[i][j + 1])
            hor_cost += abs(mapping[i][j] - mapping[i + 1][j])
    print("ver_cost : " + str(ver_cost))
    print("ver_cost : " + str(hor_cost))
    return ver_cost + hor_cost

mapping1 = [
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ]

mapping2 = [
        [1 ,2 , 3, 4, 5, 6, 7, 8],
        [9 ,10,11,12,13,14,15,16],
        [17,18,19,20,21,22,23,24],
        [25,26,27,28,29,30,31,32],
        [33,34,35,36,37,38,39,40],
        [41,42,43,44,45,46,47,48],
        [49,50,51,52,53,54,55,56],
        [57,58,59,60,61,62,63,64],
    ]

mapping3 = [
        [1 ,2 , 3, 4, 5, 6, 7, 8],
        list(reversed([9 ,10,11,12,13,14,15,16])),
        [17,18,19,20,21,22,23,24],
        list(reversed([25,26,27,28,29,30,31,32])),
        [33,34,35,36,37,38,39,40],
        list(reversed([41,42,43,44,45,46,47,48])),
        [49,50,51,52,53,54,55,56],
        list(reversed([57,58,59,60,61,62,63,64])),
    ]

mapping1 = np.array(mapping1)
mapping2 = np.array(mapping2)
mapping3 = np.array(mapping3)

mapping1_cost = counting_cost(mapping1)
mapping2_cost = counting_cost(mapping2)
mapping3_cost = counting_cost(mapping3)

print("mapping1_cost is : " + str(mapping1_cost))
print("mapping2_cost is : " + str(mapping2_cost))
print("mapping3_cost is : " + str(mapping3_cost))