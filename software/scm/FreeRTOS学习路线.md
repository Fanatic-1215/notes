### 1. 基础知识
- **了解STM32**：熟悉STM32的基本架构和功能，包括其内核、外设等。
- **学习C语言**：确保你对C语言有足够的理解，因为这是开发STM32和使用FreeRTOS的基础。

### 2. 使用STM32CubeMX
- **安装STM32CubeMX**：从ST官网下载并安装STM32CubeMX。
- **创建项目**：学习如何创建一个新项目，并选择相应的STM32微控制器型号。
- **配置外设**：使用STM32CubeMX配置GPIO、中断、时钟等基础外设。
- **生成代码**：了解如何生成初始化代码，这些代码为后续的软件开发提供了基础。

### 3. 引入FreeRTOS
- **了解FreeRTOS基本概念**：学习任务、调度器、队列、信号量等基本概念。
  - **任务**：在FreeRTOS中，任务是一个独立的程序执行流。每个任务都有自己的堆栈和任务状态。
  - **调度器**：调度器负责管理任务的执行，决定哪个任务应该在何时运行。
  - **队列**：队列用于在任务之间传递数据，是一种线程安全的数据结构。
  - **信号量**：信号量主要用于同步任务或者保护共享资源。
  - **互斥量**：互斥量是一种特殊的信号量，用于确保对共享资源的独占访问。

- **集成FreeRTOS**：在STM32CubeMX中启用FreeRTOS，并配置任务和堆栈。
  - 在FreeRTOS中，你可以通过定义一个`TaskFunction`和使用`xTaskCreate`函数来创建任务，同时指定任务的堆栈大小和优先级。

- **生成FreeRTOS代码**：生成包含FreeRTOS的初始化代码。

### 4. 开发和调试
- **编写任务代码**：实践编写不同的任务，例如LED闪烁、读取传感器数据等。
- **使用同步机制**：实现任务间的同步，如使用队列、信号量和互斥量。
  - **队列**：通过`xQueueSend`和`xQueueReceive`函数来发送和接收数据。
  - **信号量**：使用`xSemaphoreGive`和`xSemaphoreTake`来释放和获取信号量。
  - **互斥量**：与信号量类似，但确保了资源的独占访问。

- **调试**：学习如何使用调试工具来调试和优化FreeRTOS应用。

### 5. 进阶学习
- **中断管理**：了解如何在FreeRTOS中安全地使用中断。
  - 在FreeRTOS中，中断安全主要涉及使用`FromISR`后缀的API函数，如`xSemaphoreGiveFromISR`，这些函数专为从中断服务例程调用而设计。

- **内存管理**：探索FreeRTOS的内存管理机制，包括静态和动态内存分配。
- **实时性分析**：学习如何分析和优化系统的实时性能。

### 6. 实际应用
- **项目实践**：尝试完成一个小型的嵌入式项目，如温度监控系统、小型机器人等。
- **学习案例分析**：分析和学习其他人的FreeRTOS项目，理解不同的应用场景和解决方案。

### 7. 持续学习
- **参加社区和论坛**：加入STM32和FreeRTOS的社区，参与讨论，解决问题。
- **阅读文档和书籍**：定期阅读STM32和FreeRTOS的最新文档和相关书籍，不断更新知识。

### 8. 常用API（重点）

![img](https://img-blog.csdnimg.cn/20200814215344482.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDc5MzQ5MQ==,size_16,color_FFFFFF,t_70#pic_center)

~~~~c
// 1. 任务:创建和删除，调度，状态查询，时间统计
xTaskCreate(); // 动态创建
xTaskCreateStatic(); // 静态创建
vTaskDelete(); // 删除任务
~~~~

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240505145844064.png" alt="image-20240505145844064" style="zoom: 67%;" />

~~~~C
// 2. 队列：创建和删除，读写
xQueueCreate(); // 动态创建
xQueueSend(); // 写
xQueueSendToBack(); // 从队列的尾部写
xQueueSendToFront(); // 从队列的头部写
xQueueOverWrite(); // 覆盖写
xQueueRecive(); // 读并删除队列头
xQueuePeek(); // 只读

// 问题：xQueueRecive();函数阻塞了
~~~~



~~~~c
// 3. 二值信号量（本质是队列）：创建和删除，释放和获取
xSemaphoreCreateBinary(); // 动态创建
xSemaphoreCreateBinarystatic(); // 静态创建
xSemaphoreGive(); // 释放
xSemaphoreTake(); // 获取

~~~~



~~~~c
// 4. 基数型信号量
~~~~



~~~~c
// 5. 互斥量
~~~~



~~~~c
// 6.事件标志组
~~~~



~~~~c
// 7. 任务通知
~~~~



~~~~c
// 8. 延迟函数
~~~~



~~~~c
// 9. 定时器
~~~~



~~~~c
// 10. 中断管理
~~~~

## 二.rtthread+shell

~~~c
// board.c
#include "main.h"
extern UART_HandleTypeDef huart1;
extern void MX_USART1_UART_Init(void);

	MX_USART1_UART_Init();// 初始化调用

void rt_hw_console_output(const char *str)
{
        rt_size_t i = 0, size = 0;
        char a = '\r';
        
        __HAL_UNLOCK(&huart1);
        
        size = rt_strlen(str);
        for (i = 0; i < size; i++)
        {
        if (*(str + i) == '\n')
        {
                HAL_UART_Transmit(&huart1, (uint8_t *)&a, 1, 1);
        }
                HAL_UART_Transmit(&huart1, (uint8_t *)(str + i), 1, 1);
        }
}

char rt_hw_console_getchar(void)
{
        int ch = -1;
        if (__HAL_UART_GET_FLAG(&huart1, UART_FLAG_RXNE) != RESET)
        {
                ch = huart1.Instance->RDR & 0xff;
        }
        else
        {
                if(__HAL_UART_GET_FLAG(&huart1, UART_FLAG_ORE) != RESET)
                {
                        __HAL_UART_CLEAR_OREFLAG(&huart1);
                }
                rt_thread_mdelay(1);
        }
        return ch;
}

~~~

