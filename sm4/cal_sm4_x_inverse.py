'''
Descripttion : 
Version      : 
Autor        : one30: one30@m.scnu.edu.cn(email)
Date         : 2021-03-06 17:47:34
LastEditTime : 2021-03-06 17:47:56
FilePath     : /sm4/cal_sm4_x_inverse.py
'''
from pyfinite import genericmatrix

XOR = lambda x,y: x^y
AND = lambda x,y: x&y
DIV = lambda x,y: x
m = genericmatrix.GenericMatrix(size=(8, 8),zeroElement=0,identityElement=1,add=XOR,mul=AND,sub=XOR,div=DIV)

m.SetRow(0, [1, 1, 0, 1, 1, 1, 0, 1])
m.SetRow(1, [1, 1, 1, 0, 1, 1, 0, 1])
m.SetRow(2, [1, 1, 0, 1, 0, 0, 1, 0])
m.SetRow(3, [1, 0, 1, 0, 1, 0, 0, 1])
m.SetRow(4, [0, 1, 0, 0, 0, 0, 1, 0])
m.SetRow(5, [1, 1, 1, 0, 0, 1, 1, 1])
m.SetRow(6, [0, 0, 0, 1, 1, 1, 1, 0])
m.SetRow(7, [0, 0, 0, 0, 0, 1, 0, 0])
print(m)
print(m.Inverse())