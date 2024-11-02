### 一.开发方式选择

#### 1.标准库+keil+vscode

#### 2.cubeMX（hal库）+keil+vocode

~~~c
// 1.printf重定向
int fputc(int ch, FILE *f)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
	return ch;
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



