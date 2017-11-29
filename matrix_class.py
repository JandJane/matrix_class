from sys import stdin


class MatrixError(BaseException):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class Matrix:
    def __init__(self, array):
        self.array = []
        for i in range(len(array)):
            self.array.append([None] * len(array[0]))
            for j in range(len(array[0])):
                self.array[i][j] = array[i][j]

    def __str__(self):
        ans = ''
        for i in range(self.size()[0]):
            for j in range(self.size()[1]):
                if j != self.size()[1] - 1:
                    ans += str(self.array[i][j]) + '\t'
                else:
                    ans += str(self.array[i][j])
            if i != self.size()[0] - 1:
                ans += '\n'
        return ans

    def size(self):
        return ((len(self.array), len(self.array[0])))

    def __add__(self, other):
        if self.size() == other.size():
            ans = []
            for i in range(self.size()[0]):
                ans.append([None] * self.size()[1])
                for j in range(self.size()[1]):
                    ans[i][j] = self.array[i][j] + other.array[i][j]
            return Matrix(ans)
        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if isinstance(self, int) or isinstance(self, float):
            ans = []
            for i in range(other.size()[0]):
                ans.append([None] * other.size()[1])
                for j in range(other.size()[1]):
                    ans[i][j] = other.array[i][j] * self
            return Matrix(ans)
        elif isinstance(other, int) or isinstance(other, float):
            ans = []
            for i in range(self.size()[0]):
                ans.append([None] * self.size()[1])
                for j in range(self.size()[1]):
                    ans[i][j] = self.array[i][j] * other
            return Matrix(ans)
        else:
            if self.size()[1] != other.size()[0]:
                raise MatrixError(self, other)
            else:
                ans = []
                for i in range(self.size()[0]):
                    ans.append([None] * other.size()[1])
                    for j in range(other.size()[1]):
                        element = 0
                        for k in range(self.size()[1]):
                            element += self.array[i][k] * other.array[k][j]
                        ans[i][j] = element
                return(Matrix(ans))

    __rmul__ = __mul__

    def solve(self, b):
        if self.size()[0] < self.size()[1]:
            raise Exceprion()
        k = 0
        for i in range(len(b)):
            if self.array[i][i] == 0:
                j = i + 1
                while j < len(b) and self.array[j][i] == 0:
                    j += 1
                if j == len(b):
                    raise Exceprion()
                else:
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    b[i] = b[j]
            alpha = 1 / self.array[i][i]
            for j in range(self.size()[1]):
                self.array[i][j] *= alpha
            b[i] *= alpha
            for j in range(i + 1, self.size()[0]):
                alpha = self.array[j][i]
                for k in range(i, self.size()[1]):
                    self.array[j][k] -= self.array[i][k] * alpha
                b[j] -= b[i] * alpha
        for i in range(self.size()[1] + 1, self.size()[0]):
            if b[i] != 0:
                raise Exceprion()
        ans = b
        for i in range(len(b) - 1, -1, -1):
            for j in range(i + 1, len(b)):
                ans[i] -= b[j] * self.array[i][j]
        return ans

    def transpose(self):
        newArray = []
        for i in range(self.size()[1]):
            newArray.append([None] * self.size()[0])
            for j in range(self.size()[0]):
                newArray[i][j] = self.array[j][i]
        self.array = newArray
        return Matrix(newArray)

    @staticmethod
    def transposed(m):
        newArray = []
        for i in range(m.size()[1]):
            newArray.append([None] * m.size()[0])
            for j in range(m.size()[0]):
                newArray[i][j] = m.array[j][i]
        return Matrix(newArray)


class SquareMatrix(Matrix):
    def __pow__(self, n):
        if n == 0:
            E = [[0] * self.size()[0] for i in range(self.size()[0])]
            for i in range(self.size()[0]):
                E[i][i] = 1
            return SquareMatrix(E)
        elif n == 1:
            return self
        elif n % 2 == 0:
            temp = (self ** (n//2))
            return temp * temp
        else:
            return self * (self ** (n - 1))
