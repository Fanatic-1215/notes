### 1.C语言

#### 		1.1变量

![image-20240430163014424](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240430163014424.png)

#### 	1.2 结构体和指针在数据结构中的运用（构造节点）

##### 		1.2.1 链表

```c
// 单向链表
// 结构体
typedef struct Node{
    int data;
    struct Node *next;
}Node;

// 结构体变量
LNNode node1；
```



##### 		1.2.2 二叉树

```c
#include <malloc.h> // 导入malloc.h

// 结构体
typedef struct BTNode{
    int data;
    struct BTNode *lchild; // 指向左子数
    struct BTNode *rchild; // 指向右子数
}BTNode;
// 结构体变量
int main() {
    // 方式一
    BTNode node1;
    
    // 方式二：常用
    BTNode *node1;
	node1 = (BTNode1 *)malloc(sizeof(BTNode)); // 使用需要导入malloc.h
    free(node1); // 回收内存
}
```

#### 	1.3 共用体

~~~c 
typedef struct Person {
    char name[20];
    int gender; 
    union {
        float score;
        char coures[];
    }sc;
} Per;

int main() {
    int i;
    Per per[num];
    for (i = 0; i < num; i++) {
        per[i].name = "lisa"
        per[i].gender = 1;
        if(per[i].name == "lisa") {
            per[i].sc.scores = 100.1; // 共用体一般在结构体嵌套使用
        }
    }
}
~~~

#### 	1.4 typedef的5种使用场景

~~~c
// 场景一：给基本数据类型起别名
typedef int integer;
int i;
integer i;

// 场景二：给结构体和共用体
struct Student {
    char name[10];
    int age;
};
typedef struct Student Stu;
Stu stu1;

// 场景三：给指针起别名
typedef int * int_pointer_typdef
int num;
int *pointe1 = &num;	
int_pointer_typdef pointer2 = &num;

// 场景四：给数组起别名
typedef int arr[5];

// 场景五：给函数起别名
typedef int (*func)(int,int);
func func1 = &min;
(*func1)(1,1);

// 一二常用
~~~

#### 	1.5 内存分配函数

![image-20240501113143553](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240501113143553.png)

~~~c
#include <stdlib.h>

malloc(10) // 在堆空间分配10个地址的空间
int * i;
i = (int *)malloc(10 * sizeof(int));
~~~

#### 1.6 文件io

~~~c
#define _CRT_SECURE_NO_WARNINGS // 禁用安全警告
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>



void testWrite() {
    const char *filepath = "C:/Users/fan/Desktop/hello.txt";
    FILE* file_p = fopen(filepath,"a");
    fputs("mello\n", file_p);
    fclose(file_p);
}
void testRead() {
    char bufferdata[100];
    const char* filepath = "C:/Users/fan/Desktop/hello.txt";
    FILE* file_p = fopen(filepath, "r");
    while (fgets(bufferdata, 100, file_p) != NULL)
    {
        printf("%s", bufferdata);
    }
    fclose(file_p);
}
int main()
{
    testWrite();
    return 0;
}
 
~~~



### 2. C语言之数据结构与算法

概念：时间复杂度（算法的基本操作执行的次数）与空间复杂度(变量的个数)

数据结构：线性表（顺序表数组，链表，栈，队列，字符串），树（二叉树，搜索二叉树，平衡搜索二叉树，AVLTree RBTree），哈希

算法：二分查找O(log2N)缺点要先排序，哈希表，B树系列，递归（斐波拉且递归O（a1(qn-1)/q-1））,

#### 顺序表（数组）

~~~c
// 顺序表数组
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
typedef int SLDataType;


// 动态顺序表
typedef struct SeqList
{
    SLDataType* array;
    int size;     // 数组存了多少数据
    int capacity; // 实际能存的数据的大小
} SL;

// 接口函数
void SeqListInit(SL *ps) {
    ps->array = NULL;
    ps->size = 0;
    ps->capacity = 0;
}
void SeqListPushBack(SL *ps, SLDataType x) {
    // 如果没有空间或者空间不足就扩容
    if (ps->size == ps->capacity)
    {
        int newcapacity = ps->capacity == 0? 4:ps->capacity *2;
        SLDataType* tep = (SLDataType *)realloc(ps->array, newcapacity*(sizeof(SLDataType)));
        if (tep == NULL)
        {
            printf("realloc fail\n");
            exit(-1);
        }
        ps->array = tep;
        ps->capacity = newcapacity;
    }
    ps->array[ps->size] = x;
    ps->size++;
    // 
}
void SeqListPrint(SL* ps) {
    for (int i = 0; i < ps->size; i++) {
        printf("%d\n", ps->array[i]);
    }
}
void SeqListDestory(SL* ps) {
    ps->array = NULL;
    ps->capacity = ps->size = 0;
}
void SeqListPopBack(SL* ps) {
    if (ps->size > 0)
    {
        ps->size--;
    }
}

void TestSeqList() {
    SL sl;
    SeqListInit(&sl);
    SeqListPushBack(&sl, 1);
    SeqListPushBack(&sl, 2);
    SeqListPushBack(&sl, 3);
    SeqListPushBack(&sl, 4);
    SeqListPushBack(&sl, 5);
    SeqListPrint(&sl);
    SeqListPopBack(&sl);
    SeqListPopBack(&sl);
    SeqListPopBack(&sl);
    SeqListPopBack(&sl);
    SeqListPopBack(&sl);
    SeqListPopBack(&sl);
    SeqListPushBack(&sl, 1);
    SeqListPushBack(&sl, 2);
    SeqListPushBack(&sl, 3);
    SeqListPushBack(&sl, 4);
    SeqListPushBack(&sl, 5);
    SeqListPrint(&sl);
    SeqListDestory(&sl);
}
int main()
{
    TestSeqList();
    return 0;
}


int main()
{
    int* p1 = (int *)malloc(sizeof(int) * 10);
    printf("%p\n", p1);
    int* p2 = (int *)realloc(p1, sizeof(int) * 20);
    printf("%p\n", p2);
    return 0;
} // 这是realloc的缺陷，如果没有连续的空间可以开辟，会在更大的空间开辟，把原来的删除，所以要用链表
~~~

#### 链表

~~~c
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
typedef int SLTDataType;

typedef struct SLT
{
    SLTDataType data;
    SLT * next;
} SLTNode;

void SListPushBack(SLTNode** pphead,SLTDataType x) {
    // 链接新节点
    SLTNode* newnode = (SLTNode*)malloc(sizeof(SLTNode));
    newnode->data = x;
    newnode->next = NULL;
    if (*pphead == NULL)
    {
        *pphead = newnode;
    }
    else
    {
        // 找到尾节点
        SLTNode* tail = *pphead; 
        while (tail->next != NULL)
        {
            tail = tail->next;
            
        }
        tail->next = newnode;
    }
    
}
void SListPrint(SLTNode * phead) {
    SLTNode* cur = phead;
    while (cur != NULL)
    {
        printf("%d->", cur->data);
        cur = cur->next;
    }
}

void TestSList() {
    SLTNode* plist = NULL;
    SListPushBack(&plist, 1);
    SListPushBack(&plist, 2);
    SListPushBack(&plist, 3);
    SListPrint(plist);
}
int main()
{
    TestSList();
    return 0;
}

~~~

#### 栈

有数组栈（更有优势）和链式栈（节省空间）

~~~c
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef int STDataType;

typedef struct Stack
{
    STDataType* a;
    int top;
    int capacity;
}ST;

void StackInit(ST* ps) {
    if (ps == NULL)
    {

    }
    ps->a = NULL;
    ps->top = 0;
    ps->capacity = 0;
}

void StackDesroy(ST * ps) {
    free(ps->a);
    ps->a = NULL;
    ps->capacity = ps->top = 0;
}

void StackPush(ST * ps,STDataType x) {
    if (ps->top == ps->capacity)
    {
        int newcapacity = ps->capacity == 0 ? 4 : ps->capacity * 2;
        STDataType* tmp = (STDataType*)realloc(ps->a,sizeof(STDataType) * newcapacity );
        if (tmp == NULL)
        {
            printf("realloc fail\n");
            exit(-1);
        }
        ps->a = tmp;
        ps->capacity = newcapacity;
    }
    ps->a[ps->top] = x;
    ps->top++;
}

void StackPop(ST* ps) {
    ps->top--;
    if (ps->top == 0)
    {
        ps->top = 0;
    }
}

STDataType StackTop(ST* ps) {

    return 0;
}

int StackSize(ST* ps) {
    return 0;
}

bool StackEmpty(ST* ps) {
    return 0;
}
void printmy(ST *ps) {
    for (int i = 0; i < ps->top; i++)
    {
        printf("%d\n", ps->a[i]);
    }
}

void testStack() {
    ST st;
    StackInit(&st);
    StackPush(&st, 1);
    StackPush(&st, 2);
    StackPush(&st, 3);
    StackPush(&st, 4);
    StackPush(&st, 5);
    printmy(&st);
    StackPop(&st);
    printmy(&st);
    StackDesroy(&st);
    printmy(&st);
}

int main()
{
    testStack();
    return 0;
}

~~~

#### 队列

有数组队列和链式队列（常用）

#### 快排

#### 二分查找

### 3. c语言之预处理

~~~c
// 1.预定义符号
__FILE__ // 进行编译的源文件
__LINE__
__DATE__
__TIME__
__STDC__
printf("%s,%d",__FILE__,__LINE__);
    
// 2.#define定义标识符1. 在编译时预处理的会被全部替换,而不是计算 2.\是续行符
#define Printx printf("hjk	\
	dhfk	\
    uehla	\
    ke")
// 定义宏
#define SQUARE(x) ((x)*(x)) // 
printf("%d", SQUARE(2));
// 替换规则
宏不能递归，就是不能自己调用自己
// #和##
    
// 3.#undef移除定义
// 4.命令行定义，和根据机器的内存大小编译出不同版本
    ls -a
    ls -l
    gcc test.c -D DATA=10 // 在代码行没有定义，在命令行-D定义
    
// 5.条件编译
// 5.1
#define __DEBUG__
#if __DEBUG__ // 如何条件为true，则编译
    printf("");
#endif // __DEBUG__

// 5.2多分支条件编译
#if 常量表达式
	// ...
#elif 常量表达式
	// ...
#else 常量表达式
	// ...
#endif

// 5.3判断是否被定义
#define max 100
#ifndef(max)
	printf();
#endif

// 5.4 嵌套指令


// 6.文件包含#include防止头文件重复定义
#ifndef __TEXT_H__
#defef __TEXT_H__
#endif
// 也可以用
#pragma once  // 有些编译器不支持

// 7.// 计算结构体成员的偏移量
#include <stddef.h>
typdef struct {
    char c1;
    int c2;
    char c3;
}ST;
printf("%d",offsetof(ST,c1)); // 0
printf("%d",offsetof(ST,c2)); // 4
printf("%d",offsetof(ST,c3)); // 8

// 方法二
#define getNum(type,m_name)	(int)&(((type*)0)->m_name)
typdef struct {
    char c1;
    int c2;
    char c3;
}ST;
~~~

### 4.  计算机组成原理

![image-20240520113608848](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240520113608848.png)

#### 1.计算机系统概述

​	硬件：冯诺依曼

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240520114912992.png" alt="image-20240520114912992" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240520115551602.png" alt="image-20240520115551602" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240520120714628.png" alt="image-20240520120714628" style="zoom:50%;" />

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240520121545308.png" alt="image-20240520121545308" style="zoom:50%;" />

​	软件：系统软件（freeRTOS等系统也是系统软件），应用软件。机器语言->汇编语言->高级语言



#### 5.C++

