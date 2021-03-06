'''
Descripttion : 
Version      : 
Autor        : one30
Date         : 2021-03-06 14:32:30
LastEditTime : 2021-03-06 17:32:33
FilePath     : /compact_aes_sbox.py
'''
g2b = [0b10011000, 0b11110011, 0b11110010, 0b01001000, 0b00001001, 0b10000001, 0b10101001, 0b11111111]
b2g = [0b01100100, 0b01111000, 0b01101110, 0b10001100, 0b01101000, 0b00101001, 0b11011110, 0b01100000]

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

A = [0b10001111, 0b11000111, 0b11100011, 0b11110001, 0b11111000, 0b01111100, 0b00111110, 0b00011111] #仿射变换矩阵乘

def AES_SBOX(x):
    t = G256_new_basis(x, g2b)
    t = G256_inv(t)
    t = G256_new_basis(t, b2g)
    t = G256_new_basis(t, A) #仿射变换乘
    return t ^ 0x63

sbox = []
for i in range(256):
    sbox.append(AES_SBOX(i)) #生成sbox

for i,s in enumerate(sbox):
    print(f'%02x'%s, ', ', end='')
    if (i+1)%16==0:
        print()

'''
python3 compact_aes_sbox.py 
63 , 7c , 77 , 7b , f2 , 6b , 6f , c5 , 30 , 01 , 67 , 2b , fe , d7 , ab , 76 , 
ca , 82 , c9 , 7d , fa , 59 , 47 , f0 , ad , d4 , a2 , af , 9c , a4 , 72 , c0 , 
b7 , fd , 93 , 26 , 36 , 3f , f7 , cc , 34 , a5 , e5 , f1 , 71 , d8 , 31 , 15 , 
04 , c7 , 23 , c3 , 18 , 96 , 05 , 9a , 07 , 12 , 80 , e2 , eb , 27 , b2 , 75 , 
09 , 83 , 2c , 1a , 1b , 6e , 5a , a0 , 52 , 3b , d6 , b3 , 29 , e3 , 2f , 84 , 
53 , d1 , 00 , ed , 20 , fc , b1 , 5b , 6a , cb , be , 39 , 4a , 4c , 58 , cf , 
d0 , ef , aa , fb , 43 , 4d , 33 , 85 , 45 , f9 , 02 , 7f , 50 , 3c , 9f , a8 , 
51 , a3 , 40 , 8f , 92 , 9d , 38 , f5 , bc , b6 , da , 21 , 10 , ff , f3 , d2 , 
cd , 0c , 13 , ec , 5f , 97 , 44 , 17 , c4 , a7 , 7e , 3d , 64 , 5d , 19 , 73 , 
60 , 81 , 4f , dc , 22 , 2a , 90 , 88 , 46 , ee , b8 , 14 , de , 5e , 0b , db , 
e0 , 32 , 3a , 0a , 49 , 06 , 24 , 5c , c2 , d3 , ac , 62 , 91 , 95 , e4 , 79 , 
e7 , c8 , 37 , 6d , 8d , d5 , 4e , a9 , 6c , 56 , f4 , ea , 65 , 7a , ae , 08 , 
ba , 78 , 25 , 2e , 1c , a6 , b4 , c6 , e8 , dd , 74 , 1f , 4b , bd , 8b , 8a , 
70 , 3e , b5 , 66 , 48 , 03 , f6 , 0e , 61 , 35 , 57 , b9 , 86 , c1 , 1d , 9e , 
e1 , f8 , 98 , 11 , 69 , d9 , 8e , 94 , 9b , 1e , 87 , e9 , ce , 55 , 28 , df , 
8c , a1 , 89 , 0d , bf , e6 , 42 , 68 , 41 , 99 , 2d , 0f , b0 , 54 , bb , 16 , 
'''
