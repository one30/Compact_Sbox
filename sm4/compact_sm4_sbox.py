'''
Descripttion : 
Version      : 
Autor        : one30: one30@m.scnu.edu.cn(email)
Date         : 2021-03-06 17:49:04
LastEditTime : 2021-03-06 20:22:08
FilePath     : /sm4/compact_sm4_sbox.py
'''
# import sys

# sys.path.append('../aes/')

# import compact_aes_sbox

def G4_mul(x, y):
    # GF(2^2)的乘法运算，正规基{W^2, W}
    a = (x & 0x02)>>1
    b = x & 0x01
    c = (y & 0x02)>>1
    d = y & 0x01
    e = (a ^ b) & (c ^ d)
    return (((a & c) ^ e) << 1) | ((b & d) ^ e)

def G4_mul_N(x):
    # GF(2^2)上的乘N操作，N=W^2
    a = (x & 0x02)>>1
    b = x & 0x01
    p = b
    q = a ^ b
    return (p<<1)|q

def G4_mul_N2(x):
    # GF(2^2)上的乘N^2操作，N=W^2
    a = (x & 0x02)>>1
    b = x & 0x01
    return ((a ^ b)<<1) | a\

def G4_inv(x):
    # GF(2^2)的求逆操作，该操作和GF(2^2)的平方操作等价
    a = (x & 0x02)>>1
    b = x & 0x01
    return (b<<1)|a

def G16_mul(x, y):
    # GF(2^4)的乘法操作，正规基{Z^4, Z}
    a = (x & 0xc)>>2
    b = x & 0x03
    c = (y & 0xc)>>2
    d = y & 0x03
    e = G4_mul(a^b, c^d)
    e = G4_mul_N(e)
    p = G4_mul(a,c) ^ e
    q = G4_mul(b,d) ^ e
    return (p<<2) | q

def G16_sq_mul_u(x):
    # GF(2^4)的平方后乘u操作, u = N^2Z, N = W^2
    a = (x & 0xc)>>2
    b = x & 0x3
    p = G4_inv(a ^ b)
    q = G4_mul_N2(G4_inv(b))
    return (p<<2)|q

def G16_inv(x):
    # GF(2^4)的求逆操作
    a = (x & 0xc)>>2
    b = x & 0x03
    c = G4_mul_N(G4_inv(a^b))
    d = G4_mul(a, b)
    e = G4_inv(c ^ d)
    p = G4_mul(e, b)
    q = G4_mul(e, a)
    return (p<<2)|q

def G256_inv(x):
    # GF(2^8)的求逆操作
    a = (x & 0xf0)>>4
    b = x & 0x0f
    c = G16_sq_mul_u(a ^ b)
    d = G16_mul(a, b) 
    e = G16_inv(c ^ d)
    p = G16_mul(e, b)
    q = G16_mul(e, a)
    return (p<<4)|q

def G256_new_basis(x, b):
    # x在新基b下的表示
    y = 0
    for i in range(8):
        if x & (1<<(7-i)):
            y ^= b[i]
    return y

g2b = [0b00100001, 0b11010011, 0b10000001, 0b01001010, 0b10001010, 0b10111001, 0b10110000, 0b11111111]
b2g = [0xf4, 0xec, 0x54, 0xa2, 0xd2, 0xc7, 0x2e, 0xd4]

A = [0b11100101, 0b11110010, 0b01111001, 0b10111100, 0b01011110, 0b00101111, 0b10010111, 0b11001011]
def SM4_SBOX(x):
    t = G256_new_basis(x, A)
    t ^= 0xd3
    t = G256_new_basis(t, g2b)
    t = G256_inv(t)
    t = G256_new_basis(t, b2g)
    t = G256_new_basis(t, A) #仿射变换乘
    return t ^ 0xd3

sbox = []
for i in range(256):
    sbox.append(SM4_SBOX(i))  # 生成sbox

for i,s in enumerate(sbox):
    print(f'%02x'%s,', ', end='')
    if (i+1)%16==0:
        print()

