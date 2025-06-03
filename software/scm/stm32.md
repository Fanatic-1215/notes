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
#include "main.h"
typedef struct {
  const char* cmd_str;
  void* var;
  int type; // 0 for int, 1 for float
} CommandMapping;
static CommandMapping command_map[] = {
  {"Value_Cur_Sta", &Value_Cur_Sta, 0},
  {"Value_THD", &Value_THD, 1},
  {"Value_FV", &Value_FV, 1},
  {"Value_FREQUENCE", &Value_FREQUENCE, 1},
  {"Value_JB1", &Value_JB1, 1},
  {"Value_JB2", &Value_JB2, 1},
};

#define COMMAND_MAP_SIZE (sizeof(command_map) / sizeof(command_map[0]))
static int8_t CDC_Receive_FS(uint8_t* Buf, uint32_t *Len)
{
  /* USER CODE BEGIN 6 */
  char cmd[20] = {0};  
  char param[20] = {0}; 
  if (sscanf((char*)Buf, "AT+%19[^=]=%19[^\r\n]", cmd, param) == 2) { 
      for (size_t i = 0; i < COMMAND_MAP_SIZE; i++) {
          if (strcmp(cmd, command_map[i].cmd_str) == 0) {
              if (command_map[i].type == 0) { // Integer
                  *((uint8_t*)command_map[i].var) = (uint8_t)(isdigit(param[0]) ? atoi(param) : 0);
              } else if (command_map[i].type == 1) { // Float
                  *((float*)command_map[i].var) = (isdigit(param[0]) ? (strchr(param, '.') ? atof(param) : (float)atoi(param)) : 0);
              }
              usb_printf("Set %s to: %s\r\n", cmd, param);
              break; // Exit loop once the command is found and processed
          }
      }
  }
  USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);
  USBD_CDC_ReceivePacket(&hUsbDeviceFS);
  return (USBD_OK);
  /* USER CODE END 6 */
}
~~~



#### 3.cubeIDE

~~~c
// 1.printf重定向
int __io_putchar(int ch) {
	HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 1000);
}
~~~

#### 4.Makefile

~~~makefile
# 第一步：GNU Tools Arm Embedded编译gcc和openocd下载工具
~~~

~~~makefile
# 第二步：配置Makefile
define GCC_PATH
"./tool/GNU Tools Arm Embedded/7 2018-q2-update/bin"
endef

define OPENOCD_PATH
"./tool/openocd"
endef

#######################################
# download stlink
#######################################
OPENOCD_INTERFACE = stlink-v2.cfg
OPENOCD_TARGET = stm32f1x.cfg
TARGET = make_demo1
OPENOCD_FLASH_START = 0x08000000
download:
	$(OPENOCD_PATH)/bin/openocd -f $(OPENOCD_PATH)/scripts/interface/$(OPENOCD_INTERFACE) -f $(OPENOCD_PATH)/scripts/target/$(OPENOCD_TARGET) -c init -c targets -c "reset halt" -c "flash write_image erase ./$(BUILD_DIR)/$(TARGET).bin 0x08000000" -c "verify_image ./$(BUILD_DIR)/$(TARGET).bin 0x08000000 bin" -c "reset run" -c shutdown

#######################################
# download daplink
#######################################
OPENOCD_INTERFACE = cmsis-dap.cfg
OPENOCD_TARGET = stm32f1x.cfg
TARGET = make_demo1
OPENOCD_FLASH_START = 0x08000000
download:
	$(OPENOCD_PATH)/bin/openocd \
		-f $(OPENOCD_PATH)/share/openocd/scripts/interface/$(OPENOCD_INTERFACE) \
		-c "transport select swd" \
		-c "adapter speed 1000" \
		-f $(OPENOCD_PATH)/share/openocd/scripts/target/$(OPENOCD_TARGET) \
		-c "init" \
		-c "reset halt" \
		-c "flash write_image erase ./$(BUILD_DIR)/$(TARGET).elf" \
		-c "reset run" \
		-c "shutdown"
~~~

#### 5.Cmake+makefile

~~~makefile
# 第一步：在build目录下
cmake .. -G "Unix Makefiles"
~~~

~~~makefile
# 第二步：在build目录下配置
#######################################
# download
#######################################
define OPENOCD_PATH
"C:/BearPi/developTools/openocd"
endef
OPENOCD_INTERFACE = stlink-v2.cfg
OPENOCD_TARGET = stm32f1x.cfg
TARGET = cmake_demo1
OPENOCD_FLASH_START = 0x08000000
download:
	$(OPENOCD_PATH)/bin/openocd -f $(OPENOCD_PATH)/scripts/interface/$(OPENOCD_INTERFACE) -f $(OPENOCD_PATH)/scripts/target/$(OPENOCD_TARGET) -c "program ./$(BUILD_DIR)/$(TARGET).elf" -c "reset run" -c shutdown
~~~

~~~makefile
# 第三步：编译下载
make && make download
~~~

#### 6.Cmake+ninja

~~~makefile
# 编译下载
cmake -B build -G "Ninja" 
ninja -C build
~~~

#### 7.makefile+task.json

~~~json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "OPENOCD_PATH": "E:/env/OpenOCD-20240916-0.12.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "make",
            "args": [
            ],
            "group": "build"
        },
        {
            "label": "connect",
            "type": "shell",
            "command": "usbip",
            "args": [
                "attach",
                "-r",
                "192.168.137.33",
                "-b",
                "1-1"
            ],
            "group": "build"
        },
        {
            "label": "clean",
            "type": "shell",
            "command": "make",
            "args": [
                "clean"
            ],
            "group": "build"
        },
        {
            "label": "download",
            "type": "shell",
            "command": "E:/env/OpenOCD-20240916-0.12.0/bin/openocd",
            "args": [
                "-f",
                "E:/env/OpenOCD-20240916-0.12.0/share/openocd/scripts/interface/cmsis-dap.cfg", 
                "-c", "adapter speed 500",  // 关键点：设置下载速度为 1000 kHz 
                "-f",
                "E:/env/OpenOCD-20240916-0.12.0/share/openocd/scripts/target/stm32f1x.cfg", 
                "-c", "init",
                "-c", "reset halt",          // 先复位并暂停目标 
                "-c", "flash write_image erase build/make_demo1.elf",   // 擦除后写入 
                "-c", "reset run",           // 复位并运行 
                "-c", "shutdown"
            ],
            "group": "build"
        },
        {
            "label": "build & download",
            "type": "shell",
            "dependsOn":["build","download"],
            "group": "build",
            "dependsOrder": "sequence",
            "problemMatcher": []
        }
    ]
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



