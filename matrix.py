import numpy as np
import random
import json
import copy

# ################################################
# Description:      Class that is used to help in  
#                   serialization of numpy arrays.
# ################################################
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# ################################################
# Description:      This is a class that abstracts
#                   away a lot of matrix functionality.
#                   Has a number of basic operations as 
#                   wells as some serialization options.
# ################################################
class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.zeros((rows, cols))

    # ################################################
    # Description:      Deepcopy the matrix and return  
    # ################################################
    def copy(self):
        matrix = copy.deepcopy(self)
        return matrix

    
    # ################################################
    # Description:      Converts the numpy matrix internal
    #                   object to an array. 
    # ################################################
    def toArray(self):
        lst = list(self.matrix)
        for count in range(0, len(lst)):
            lst[count] = list(lst[count])
        return lst

    # ################################################
    # Description:      Add two matricies together.
    #                   If input is an int add item
    #                   to all elements. 
    # ################################################
    def add(self, a):
        if isinstance(a, int) or isinstance(a, float):
            mObj = self.copy()
            for y in range(0, self.rows):
                for x in range(0, self.cols):
                    mObj.matrix[y][x] += a
        else:
            matrix = np.add(self.matrix, a.matrix)
            mObj = Matrix(self.rows, self.cols)
            mObj.matrix = matrix
        return mObj

    # ################################################
    # Description:      Randomize the matrix items.
    # ################################################
    def randomize(self):
        for y in range(0, self.rows):
            for x in range(0, self.cols):
                self.matrix[y][x] = (random.random() * 2) - 1

    # ################################################
    # Description:      Serialize the matrix into a 
    #                   string object.
    # ################################################
    def serialize(self):
        j = {'rows': self.rows, "cols": self.cols, "matrix": self.matrix}
        return json.dumps(j, cls = NumpyEncoder)

    # ################################################
    # Description:      Easy print for matrix.
    # ################################################
    def printMatrix(self):
        print(self.matrix)

    # ################################################
    # Description:      Multiplies self by another 
    #                   matrix.
    # ################################################
    def multiplySelf(self, nM):   
        if isinstance(nM, float) or isinstance(nM, int):
            matrix = np.multiply(nM, self.matrix)
        else:
            try:
                matrix = np.multiply(self.matrix, nM.matrix)
            except:
                matrix = self.matrix @ nM.matrix
        shape = matrix.shape
        rows = shape[0]
        try:
            cols = shape[1]
        except IndexError:
            cols = 1
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj
        
        pass

    # ################################################
    # Description:      This is a function to apply a
    #                   function operation to each
    #                   element in the array.
    # ################################################
    def map(self, func):
        matrix = self.copy()
        for y in range(0, self.rows):
            for x in range(0, self.cols):
                val = matrix.matrix[y][x]
                matrix.matrix[y][x] = func(val)

        return matrix

    # ################################################
    # Description:      Create a matrix from a number
    #                   array/list.
    # ################################################
    @staticmethod
    def fromArray(data):
        rows = len(data)
        try:
            cols = len(data[0])
        except TypeError:
            cols = 1
            lst = []
            for i in data:
                lst.append([i])
            data = lst
        mObj = Matrix(rows, cols)
        mObj.matrix = np.array(data)
        return mObj

    # ################################################
    # Description:      Given a serialized string
    #                   will create a matrix object.
    # ################################################
    @staticmethod
    def deserialize(data):
        loaded = json.loads(data)
        rows = loaded['rows']
        cols = loaded['cols']
        matrix = np.asarray(loaded['matrix'])
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj

    # ################################################
    # Description:      Multiply two matrices together
    # ################################################
    @staticmethod
    def multiply(nO, nM):
        matrix = np.dot(nO.matrix, nM.matrix)
        shape = matrix.shape
        rows = shape[0]
        try:
            cols = shape[1]
        except IndexError:
            cols = 1
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj

    # ################################################
    # Description:      Maps a function to each item
    #                   in a particular matrix.
    # ################################################
    @staticmethod
    def mapMF(matrix, func):
        return matrix.map(func)

    # ################################################
    # Description:      Subtract two matrices and return
    # ################################################
    @staticmethod
    def subtractMatrices(a, b):
        matrix = np.subtract(a.matrix, b.matrix)
        rows = np.size(matrix)
        cols = np.size(matrix, 1)
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj

    # ################################################
    # Description:      Add two matrices and return
    # ################################################
    @staticmethod
    def addMatrices(a, b):
        matrix = np.add(a.matrix, b.matrix)
        rows = np.size(matrix)
        cols = np.size(matrix, 1)
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj

    # ################################################
    # Description:      Transposes the given matrix
    #                   and returns a new one.
    # ################################################
    @staticmethod
    def transposeMatrix(n):
        matrix = np.transpose(n.matrix)
        rows = n.cols
        cols = n.rows
        mObj = Matrix(rows, cols)
        mObj.matrix = matrix
        return mObj



    
if __name__ == "__main__":

    m = Matrix(3, 3)
    m.matrix[0] = [1, 2, 3]
    m.matrix[1] = [4, 5, 6]
    m.matrix[2] = [7, 8, 9]

    m = m.add(1)
    print(m.matrix)

    print()
    m =  Matrix(2, 2)
    m.matrix[0] = [1, 2]
    m.matrix[1] = [3, 4]
    n = Matrix(2, 2)
    n.matrix[0] = [10, 11]
    n.matrix[1] = [12, 13]
    print(n.add(m).matrix)


    print()
    m = Matrix(3, 2)
    m.matrix[0] = [1, 2]
    m.matrix[1] = [3, 4]
    m.matrix[2] = [5, 6]
    n1 = Matrix(3, 2)
    n1.matrix[0] = [7, 8]
    n1.matrix[1] = [9, 10]
    n1.matrix[2] = [11, 12]
    print(n1.matrix)
    print(m.matrix)
    print(m.multiplySelf(n1).matrix)
    print(Matrix.multiply(m, n1).matrix)


    
    m = Matrix(2, 3)
    m.matrix[0] = [1, 2, 3]
    m.matrix[1] = [4, 5, 6]
    n = Matrix(3, 2)
    n.matrix[0] = [7, 8]
    n.matrix[1] = [9, 10]
    n.matrix[2] = [11, 12]
    print(m.multiplySelf(n).matrix)
    print(Matrix.multiply(m, n).matrix)