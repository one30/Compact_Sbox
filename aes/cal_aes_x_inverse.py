'''
Descripttion : cal x^-1 at GF(2^8)
Version      : from https://mp.weixin.qq.com/s/TsnPvdPOcgKguFZbhMDWQw
Autor        : one30: one30@m.scnu.edu.cn
Date         : 2021-03-06 11:22:31
LastEditTime : 2021-03-06 14:31:35
FilePath     : /cal_aes_x_inverse.py
'''
from pyfinite import genericmatrix

XOR = lambda x,y: x^y
AND = lambda x,y: x&y
DIV = lambda x,y: x
m = genericmatrix.GenericMatrix(size=(8, 8), zeroElement=0, identityElement=1, add=XOR, mul=AND, sub=XOR, div=DIV)

m.SetRow(0, [0, 0, 0, 1, 0, 0, 1, 0])
m.SetRow(1, [1, 1, 1, 0, 1, 0, 1, 1])
m.SetRow(2, [1, 1, 1, 0, 1, 1, 0, 1])
m.SetRow(3, [0, 1, 0, 0, 0, 0, 1, 0])
m.SetRow(4, [0, 1, 1, 1, 1, 1, 1, 0])
m.SetRow(5, [1, 0, 1, 1, 0, 0, 1, 0])
m.SetRow(6, [0, 0, 1, 0, 0, 0, 1, 0])
m.SetRow(7, [0, 0, 0, 0, 0, 1, 0, 0])
print(m)

print(m.Inverse())