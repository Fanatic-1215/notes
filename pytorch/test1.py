import torch

# 一.认识pyrch:1.元素操作 ----------------------------------------------------------------------------------------------

# x = torch.empty(5,3)
# print(x)

# x = torch.rand(5,3)
# print(x)

# x = torch.zeros(5,3,dtype=torch.long)
# print(x)

# x = torch.tensor([5.5,3])
# print(x)

# x =  torch.ones(5,3,dtype=torch.long)
# y = torch.rand_like(x,dtype=torch.float)
# print(x)
# print(y)
# m,n = x.size()
# print('m = ',m)
# print('n = ',n)


# 一.认识pyrch:2.运算操作 ----------------------------------------------------------------------------------------------
# buffer = torch.empty(5,3)
# x = torch.tensor([[1.1,1.2,1.3],[2.1,2.2,2.3],[3.1,3.2,3.3],[4.1,4.2,4.3],[5.1,5.2,5.3]])
# y = torch.rand(5,3)
# print(x)
# print(y)
# print(torch.add(x,y))
# print(x + y)
# buffer = torch.add(x,y)
# print(buffer)
# print(x[:,:2])

# 一.认识pyrch:3.类型转换 ----------------------------------------------------------------------------------------------
# tensor与numpy之间的转换
# cpu与gpu

# 二.pytorch中的autograde-------------------------------------自动求导--------------------------------------------------
x = torch.ones(3,3,requires_grad=True)
print(x)
y = x + 2
print(y)
print(x.grad_fn)
print(y.grad_fn)
print(y.mean())
print(x.eq(y).all())
