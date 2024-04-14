matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]

def maximalRectangle(matrix):
    if not matrix:
        return 0
    # return 0 if matrix is empty
    n = len(matrix[0]) 
    # n is the number of columns
    height = [0] * (n + 1)
    # height is a list of n+1 zeros, we need n+1 because we need to calculate the area of the last column, so we need to add a zero to the end of the list to calculate the area of the last column

    # still not sure why we need to add a zero to the end of the list
    res = 0
    # res is the maximum area of the rectangle
    for row in matrix:
        for i in range(n): # for each column
            height[i] = height[i] + 1 if row[i] == '1' else 0 # if the element in the row is 1, increment the height of the column by 1, otherwise set the height of the column to 0
        stack = [-1] # stack is a list with -1 as the only element, we need to add -1 to the stack because we need to calculate the area of the first column, so we need to add -1 to the stack to calculate the area of the first column
        for i in range(n + 1):
            while height[i] < height[stack[-1]]:
                h = height[stack.pop()]
                w = i - 1 - stack[-1]
                res = max(res, h * w)
            stack.append(i)
    return res

print(maximalRectangle(matrix))



def find_maximal_rectangle(matrix: list[list[str]]) -> int:
    n = len(matrix[0])
    heights = [0] * (n + 1)
    best = 0
    for row in matrix:
        for col in range(n):
            heights[col] = heights[col] + 1 if row[col] == '1' else 0
        stack = [-1]
        for col in range(n + 1):
            while heights[col] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = col - stack[-1] - 1
                best = max(best, h * w)
            stack.append(col)
    return best

print(find_maximal_rectangle(matrix))