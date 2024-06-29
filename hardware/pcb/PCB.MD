## 1. PCB设计布线常用操作（规则）

### 	1.1 孔径

​		过孔直径=2*过孔孔径+/-2mil

​		一般：r = 12mil，R = 22mil(考虑成本最低)

### 	1.2 线宽

​		1.width of power:30mil

​		2.width of single:8mil

​		3....

### 	1.3 间距

### 	1.4 短路

### 	1.5 开路

### 	1.6 铜皮

​		1.正片

​		2.负片：6mil

### 	1.7 阻焊

​		2.5mil

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503190939763.png" alt="image-20240503190939763" style="zoom:50%;" />

​		油墨桥大于等于4mil

## 2.PCB设计布线常用操作（命令）

### 	2.2 U + M联合布线(TAB切换走线间距)

### 	2.3 CTRL + G修改步进

### 	2.4 U + F + O扇孔

### 	2.5 合理分类

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503210134359.png" alt="image-20240503210134359" style="zoom:100%;" />

### 3. PCB布线的基本原则

### 	3.1 先处理信号线，再处理电源线

### 	3.2 从最密的地方开始走线

### 	3.3 晶振包地走线，内差分走线，下方不走线

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503194252264.png" alt="image-20240503194252264" style="zoom:50%;" />

### 	3.4 孔的处理：错位打孔；GND孔就近打孔

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503195747107.png" alt="image-20240503195747107" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503204123455.png" alt="image-20240503204123455" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503204450675.png" alt="image-20240503204450675" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503204539698.png" alt="image-20240503204539698" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503205158763.png" alt="image-20240503205158763" style="zoom:70%;" />

![image-20240503205254886](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240503205254886.png)

## 4. 电源的处理（按照顺序，上面是信号线的处理，接下来是电源的处理）

### 	4.1 电源（大电源铺铜，小电源可以走信号线）(平面分割)

### 5. DRC电气性能检查（design rule check）

​	
