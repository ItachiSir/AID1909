# # 矩阵转置
# list = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12]
# ]
# list02=[]
# for c in range(len(list[0])):
#     line=[]
#     for r in range(len(list)):
#         line.append(list[r][c])
#     list02.append(line)
# print(list02)

# Z字形变换

# 行数为3                  行数为4
# L * C * I * R           L * * D * * R
# E T O E S I I G         E * O E * I I
# E * D * H * N           E C * I H * N
#                         T * * S * * G

def convert(s, numRows):
    if numRows == 1:
        return s
    rows = [''] * min(numRows, len(s))
    cur_row = 0
    going_down = False
    for c in s:
        for index in range(len(rows)):
            if index==cur_row:
                rows[index] += c
            elif index!=cur_row:
                rows[index]+=' '

        if cur_row == 0 or cur_row == numRows - 1:
            going_down = not going_down
        cur_row += 1 if going_down else -1
    for item in rows:
        print(item.strip())
    res = ''.join(rows)
    return res
s="LEETCODEISHIRING"
numRows = 4
# print(convert(s,numRows))
convert(s,numRows)