matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]

def maximalRectangle(matrix):
    if not matrix:
        return 0
    columns = len(matrix[0])
    print(columns," columns")
    height = [0] * (columns + 1)
    print(height," height table initally")
    print(" ")
    
    res = 0
    for row_index, row in enumerate(matrix):
        for i in range(columns):
            height[i] = height[i] + 1 if row[i] == '1' else 0
        print(height," height table for row" ,row_index)
        stack = [-1]
        for i in range(columns + 1):
            while height[i] < height[stack[-1]]:
                h = height[stack.pop()]
                w = i - 1 - stack[-1]
                res = max(res, h * w)
            stack.append(i)
    print(" ")

    print("this way we get the height of the columns for the current row \n")
    print("ignore the last column in the height table for now,just focus on the first 5 columns \n")
        
    return res

for i in matrix:
    print(i)
print(maximalRectangle(matrix)," Ans")

# steps
# 1. create a list of zeros with n+1 elements, n is the number of columns
# 2. for each row in the matrix
# 3. for each column in the row
# 4. if the element in the row is 1, increment the height of the column by 1
# 5. if the element in the row is 0, set the height of the column to 0
# 6. create a stack with -1 as the only element