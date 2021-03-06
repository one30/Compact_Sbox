'''
Descripttion : cal compact aes or sm4 sbox
Version      : source from https://mp.weixin.qq.com/s/TsnPvdPOcgKguFZbhMDWQw
Autor        : one30
Date         : 2021-03-05 11:33:26
LastEditTime : 2021-03-06 11:21:55
FilePath     : /cal_X.py
'''
from pyfinite import ffield

gen = 0b100011011
# gen = 0b111110101
F = ffield.FField(8, gen, useLUT=0)

def field_pow2(x,F): # 计算在F域上的平方
    return F.Multiply(x, x)

def field_pow3(x,F): # 计算在F域上的三次方
    return F.Multiply(x, field_pow2(x, F))

def field_pow4(x,F): # 计算在F域上的四次方
    return field_pow2(field_pow2(x, F), F)

for i in range(256): # 搜索w^2+w+1=0的根 正规基:{W^2,W}
    if field_pow2(i, F)^i^1 == 0:
        print(hex(i))
# 得到W = 0xbd, W^2 = 0xbc

# print(field_pow2(0xbc, F) ^ 0xbc ^ 1)
# print(field_pow2(0xbd, F) ^ 0xbd ^ 1)

 # 搜索z^2+z+0xbc=0的根 正规基:{Z^4,Z} s(z) = z^2+z+N, N=w^2=0xbc
for i in range(256):
    if field_pow2(i, F)^i^0xbc == 0:
        print(hex(i))
# 得到Z = 0x5c, Z^16 = 0x5d

# print(hex(field_pow2(0x5c, F) ^ 0x5c ^ 0xbc))
# print(hex(field_pow2(0x5d, F) ^ 0x5d ^ 0xbc))

 # 搜索GF(2^8)/GF(2^4)的正规基:{Y^16,Y} r(y) = y^2+y+v, v=N^2Z
v = F.Multiply(field_pow2(0xbc, F), 0x5c) #v = 0xec
# print(hex(v))
for i in range(256):
    if field_pow2(i, F) ^ i ^ v == 0:
        print(hex(i))
# we got Y = 0xff, Y^16 = 0xfe

print('result:')
w = 0xbd
w_2 = 0xbc
z = 0x5c
z_4 = 0x5d
y = 0xff
y_16 = 0xfe
w_2_z_4_y_16 = F.Multiply(F.Multiply(w_2, z_4), y_16)
w_z_4_y_16 = F.Multiply(F.Multiply(w, z_4), y_16)
w_2_z_y_16 = F.Multiply(F.Multiply(w_2,z), y_16)
w_z_y_16 = F.Multiply(F.Multiply(w, z), y_16)
w_2_z_4_y = F.Multiply(F.Multiply(w_2, z_4), y)
w_z_4_y = F.Multiply(F.Multiply(w, z_4), y)
w_2_z_y = F.Multiply(F.Multiply(w_2, z), y)
w_z_y = F.Multiply(F.Multiply(w, z), y)
print('w_2_z_4_y_16\t', hex(w_2_z_4_y_16))
print('w_z_4_y_16\t', hex(w_z_4_y_16))
print('w_2_z_y_16\t', hex(w_2_z_y_16))
print('w_z_y_16\t', hex(w_z_y_16))
print('w_2_z_4_y\t', hex(w_2_z_4_y))
print('w_z_4_y\t\t', hex(w_z_4_y))
print('w_2_z_y\t\t', hex(w_2_z_y))
print('w_z_y\t\t', hex(w_z_y))

# result:
# w_2_z_4_y_16     0x64
# w_z_4_y_16       0x78
# w_2_z_y_16       0x6e
# w_z_y_16         0x8c
# w_2_z_4_y        0x68
# w_z_4_y          0x29
# w_2_z_y          0xde
# w_z_y            0x60

