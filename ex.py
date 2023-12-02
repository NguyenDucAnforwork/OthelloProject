grid = [[1,-1], [1,-2]]
weight = [[1,2], [3,4]]
print(sum([int(grid[i][j])*int(weight[i][j]) for i in range(0,2) for j in range(0,2)]))