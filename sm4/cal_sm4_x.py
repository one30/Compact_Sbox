'''
Descripttion : 
Version      : 
Autor        : one30: one30@m.scnu.edu.cn(email)
Date         : 2021-03-06 17:41:27
LastEditTime : 2021-03-06 17:45:25
FilePath     : /sm4/cal_sm4_x.py
'''
from pyfinite import ffield

gen = 0b111110101
F = ffield.FField(8, gen, useLUT=0) # 这里一定要写useLUT=0，不然会出问题。。。

def field_pow2(x,F): # 计算在F域上的平方
    return F.Multiply(x, x)

def field_pow3(x,F): # 计算在F域上的三次方
    return F.Multiply(x, field_pow2(x, F))

def field_pow4(x,F): # 计算在F域上的四次方
    return field_pow2(field_pow2(x, F), F)

# 
for i in range(256):
    if field_pow2(i, F)^i^1 == 0: # 搜索 w^2+w+1 = 0的根
        print(hex(i))

for i in range(256):
    if field_pow2(i, F)^i^0x5c == 0: # 搜索 z^2+z+0x5c = 0的根
        print(hex(i))

u = F.Multiply(field_pow2(0x5c, F), 0x0c)
for i in range(256):
    if field_pow2(i, F)^i^0x76 == 0: # 搜索 z^2+z+0x76 = 0的根
        print(hex(i))

w = 0x5d
w_2 = 0x5c
z = 0x0c
z_4 = 0x0d
y = 0xef
y_16 = 0xee
w_2_z_4_y_16 = F.Multiply(F.Multiply(w_2, z_4), y_16)
w_z_4_y_16 = F.Multiply(F.Multiply(w, z_4), y_16)
w_2_z_y_16 = F.Multiply(F.Multiply(w_2, z), y_16)
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