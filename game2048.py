"""
2048核心算法
"""

list_merge = [2, 0, 0, 2]


# 1.定义函数,将list_merge中的0元素移到末尾
# 2 0 2 0 -->2 2 0 0
# 0 0 2 0 -->2 0 0 0
# 4 0 2 4 -->4 2 4 0


def zero_to_end(L):
    for r in range(len(L) - 1):
        for c in range(r + 1, len(L)):
            if L[r] == 0:
                L[r], L[c] = L[c], L[r]


# zero_to_end(list_merge)
# print(list_merge)

def merge(L):
    zero_to_end(L)
    for r in range(len(L) - 1):
        if L[r] == L[r + 1]:
            L[r] += L[r + 1]
            del L[r + 1]
            L.append(0)


# merge(list_merge)
# print(list_merge)

# 定义函数，将二维列表中的数据进行左移操作
map = [
    [2, 0, 2, 0],
    [4, 4, 2, 0],
    [0, 4, 0, 4],
    [2, 2, 0, 4]
]


def left_merge(vic):
    for list in vic:
        merge(list)


# left_merge(map)
# print(map)
# 定义函数，将二维列表中的数据进行右移操作
def right_merge(vic):
    for list in vic:
        L = list[::-1]
        merge(L)
        list[::-1] = L


# right_merge(map)
# print(map)


# 方阵转置
def square_matrix_transpose(sqr_matrix):
    for c in range(len(sqr_matrix) - 1):  # 0,1,2
        for r in range(c + 1, len(sqr_matrix)):
            sqr_matrix[r][c], sqr_matrix[c][r] = sqr_matrix[c][r], sqr_matrix[r][c]


# 定义函数，将二维列表中的数据进行上移操作
def move_up(vic):
    square_matrix_transpose(vic)
    left_merge(vic)
    square_matrix_transpose(vic)


# 定义函数，将二维列表中的数据进行下移操作
def move_down(vic):
    square_matrix_transpose(vic)
    right_merge(vic)
    square_matrix_transpose(vic)


move_down(map)
print(map)
