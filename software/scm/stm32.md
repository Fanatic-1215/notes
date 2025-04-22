### 一.开发方式选择

#### 1.寄存器+hal库+keil+vscode

~~~c
// 1.检查复位原因
void checkResetReason(void) {
  // 读取RCC_CSR寄存器的值
  uint32_t resetFlags = RCC->CSR;
  printf("main:");
  // 判断重启原因
  if ((resetFlags & RCC_CSR_SFTRSTF) != 0) {
    // 软件复位
    printf("Software Reset\n");
  } else if ((resetFlags & RCC_CSR_PORRSTF) != 0) {
    // 上电复位
    HAL_Delay(3000);
    printf("Power-On Reset\n");
  } else if ((resetFlags & RCC_CSR_PINRSTF) != 0) {
    // 外部引脚复位
    printf("Pin Reset\n");
  } else if ((resetFlags & RCC_CSR_IWDGRSTF) != 0) {
    // 独立看门狗复位
    printf("Independent Watchdog Reset\n");
  } else if ((resetFlags & RCC_CSR_WWDGRSTF) != 0) {
    // 窗口看门狗复位
    printf("Window Watchdog Reset\n");
  } else if ((resetFlags & RCC_CSR_LPWRRSTF) != 0) {
    // 低功耗复位
    printf("Low-Power Reset\n");
  } else if ((resetFlags & RCC_CSR_BORRSTF) != 0) {
    // 电源复位
    printf("Brown-Out Reset\n");
  }
  // 清除复位标志
  RCC->CSR |= RCC_CSR_RMVF;
}
~~~



#### 1.标准库+keil+vscode

#### 2.cubeMX（hal库）+keil+vocode

~~~c
// 1.printf重定向
int fputc(int ch, FILE *f)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
	return ch;
}
// 1.printf重定向
#include <stdio.h>
#include "usbd_cdc_if.h"
int fputc(int ch, FILE *f)
{
		uint8_t chr = ch;
		USBD_StatusTypeDef res;
	
		do {
				res = CDC_Transmit_FS(&chr, 1);
		} while(res != USBD_OK);

    return ch;
}

// 1.printf重定向
#include <stdio.h>
#include "usbd_cdc_if.h" // 在usbd_cdc_if.c这个文件
#include <stdarg.h>
void usb_printf(const char *format, ...)
{
    va_list args;
    uint32_t length;
 
    va_start(args, format);
    length = vsnprintf((char *)UserTxBufferFS, APP_TX_DATA_SIZE, (char *)format, args);
    va_end(args);
    CDC_Transmit_FS(UserTxBufferFS, length);
}
static int8_t CDC_Receive_FS(uint8_t* Buf, uint32_t *Len) // usb接收
{
  /* USER CODE BEGIN 6 */
  // 解析AT指令
  static float AP = 0.2;
  static float AI = 0.0;
  static float AD = 0.1;
  static float SP = 0.09;
  static float SI = 0.002;
  static float SD = 0.0;
  int fanFOC_mode = 0;
  char cmd[20] = {0};  // 增加缓冲区大小
  char param[20] = {0}; // 增加缓冲区大小
  if (sscanf(Buf, "AT+%19[^=]=%19[^\r\n]", cmd, param) == 2) { // 确保读取两个参数
    usb_printf("OK\r\n");
    if (strcmp(cmd, "MODE") == 0) {
      fanFOC_mode = atoi(param);
      fanFOC_set_mode(fanFOC_mode);
    } else if (strcmp(cmd, "AP") == 0) {
      AP = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    }else if (strcmp(cmd, "AI") == 0) {
      AI = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    } else if (strcmp(cmd, "AD") == 0) {
      AD = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    } else if (strcmp(cmd, "SP") == 0) {
      SP = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    } else if (strcmp(cmd, "SI") == 0) {
      SI = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    } else if (strcmp(cmd, "SD") == 0) {
      SD = atof(param);
      fanFOC_set_PID(AP,AI,AD,\
        SP,SI,SD,\
        0,0,0);
    } else if(strcmp(cmd, "ANGLE") == 0) {
      set_angle = atoi(param);
    } else if (strcmp(cmd, "SPEED") == 0) {
      set_speed = atoi(param);
    }else {
      usb_printf("Invalid AT command: %s\n", cmd);
    }
  } else {
      usb_printf("Invalid AT command format: %s\n", Buf);
  }
  memset(cmd, 0, sizeof(cmd));
  memset(param, 0, sizeof(param));


  USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);
  USBD_CDC_ReceivePacket(&hUsbDeviceFS);

  return (USBD_OK);
  /* USER CODE END 6 */
}

// 2.短按加长按下开机功能

xTaskCreate(key_task_enter, "KEY_TASK", 128, NULL, 15, NULL);
int start_flag = 0;
void key_task_enter(void const * argument) {
    while(1) {
      if (start_flag == 0)
      {  
        if (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) { // 按键被按下
            display(30); // 短按时点亮4个LED

            // 等待按键释放
            while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) {
                vTaskDelay(10); // 任务延迟，避免占用CPU
            }        
            
            display(8); // 短按时点亮所有LED    
            while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_SET) {
                vTaskDelay(10); // 任务延迟，避免占用CPU
            }
            for (int i = 0; i < 4; i++) {
                // 检查按键是否仍然被按下
                while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) { 
                    display(i+21);                 
                    if (i == 3)
                    {
                        start_flag = 1;
                        break; // 退出内层循环，继续点亮下一个 LED
                    }
                    vTaskDelay(200); // 等待 100ms

                    
                    break; // 退出内层循环，继续点亮下一个 LED
                }
                // 如果按键被松开，熄灭所有 LED
                if (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_SET) {
                    HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1);
                    display(8);
                }
            }
        }
        vTaskDelay(300); // 防止任务过于频繁运行
      } else {
        if (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) { // 按键被按下
            display(8); // 短按时点亮4个LED

            // 等待按键释放
            while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) {
                vTaskDelay(10); // 任务延迟，避免占用CPU
            }        
            display(30); // 短按时点亮所有LED    
            while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_SET) {
                vTaskDelay(10); // 任务延迟，避免占用CPU
            }
            for (int i = 4; i >= 0; i--) {
                // 检查按键是否仍然被按下
                while (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) {
                    display(i+20);
                    if (i == 0)
                    {
                        start_flag = 0;
                        break; // 退出内层循环，继续点亮下一个 LED
                    }
                    vTaskDelay(200); // 等待 100ms
                    
                    break; // 退出内层循环，继续点亮下一个 LED
                }
                // 如果按键被松开，熄灭所有 LED
                if (HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_SET) {
                    display(8);
                }
            }
        }
        vTaskDelay(300); // 防止任务过于频繁运行
      }
  }
      
}
~~~



#### 3.cubeIDE

~~~c
// 1.printf重定向
int __io_putchar(int ch) {
	HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 1000);
}
~~~

### 二.知识点（基于cubeIDE）

### 1.看门狗

~~~c
// 独立看门狗IWDG
HAL_IWDG_Refresh(); // 喂狗
// 窗口看门狗WWDG
// 判断复位原因
if(__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST) == SET) {
  printf("reset_IWDG\r\n");
  __HAL_RCC_CLEAR_RESET_FLAGS();
}else {
  printf("reset_other\r\n");
}
~~~



