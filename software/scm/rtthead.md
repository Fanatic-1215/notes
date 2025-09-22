#### 1.驱动开发（模板）

~~~c
// 看底部
#include <rtconfig.h>
#include <board.h>
#include <rtthread.h>
#include <rtdevice.h>

#define LED_PIN    GET_PIN(D, 10)

rt_device_t led_app_dev;

void led_board_init(void) {
    rt_pin_mode(LED_PIN, PIN_MODE_OUTPUT);
    rt_pin_write(LED_PIN, PIN_LOW);
}

int led(int argc, char **argv)
{
    if(argc == 2)
    {
        if(strcmp(argv[1], "on") == 0)
        {
            rt_pin_write(LED_PIN, PIN_HIGH);
        }
        else if(strcmp(argv[1], "off") == 0)
        {
            rt_pin_write(LED_PIN, PIN_LOW);
        }
        else if (strcmp(argv[1], "on_posix") == 0) {
            int fd = open("/dev/led", RT_DEVICE_FLAG_RDWR);
            if (fd == -1) {
                goto _err;
            }
            write(fd, "on", 2);
            close(fd);

        }
        else if (strcmp(argv[1], "off_posix") == 0) {
            int fd = open("/dev/led", RT_DEVICE_FLAG_RDWR);
            if (fd == -1) {
                goto _err;
            }
            write(fd, "off", 3);
            close(fd);
        }
        else if (strcmp(argv[1], "on_rtt") == 0) {
            led_app_dev = rt_device_find("led");
            if (led_app_dev == RT_NULL) {
                goto _err;
            }
            rt_device_open(led_app_dev, RT_DEVICE_FLAG_RDWR);
            rt_device_write(led_app_dev, NULL, "on", NULL);
            rt_device_close(led_app_dev);
        }
        else if (strcmp(argv[1], "off_rtt") == 0) {
            led_app_dev = rt_device_find("led");
            if (led_app_dev == RT_NULL) {
                goto _err;
            }
            rt_device_open(led_app_dev, RT_DEVICE_FLAG_RDWR);
            rt_device_write(led_app_dev, NULL, "off", NULL);
            rt_device_close(led_app_dev);
        }

        else
        {
            goto _usage;
        }
        return 0;
    }
_usage:
    rt_kprintf("Usage(led on/off)\n");
    return 0;
_err:
    rt_kprintf("err\n");
    return 0;
}


rt_err_t  led_open  (rt_device_t dev, rt_uint16_t oflag) {
    rt_kprintf("led_open\n");
    return 0;
}
rt_err_t  led_close (rt_device_t dev) {
    rt_kprintf("led_close\n");
    return 0;
}

rt_size_t led_write (rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size){
    rt_kprintf("led_write ");
    if (strcmp(buffer, "on") == 0) {
        rt_kprintf("on \n");
        rt_pin_write(LED_PIN, PIN_HIGH);
    } else if (strcmp(buffer, "off") == 0) {
        rt_kprintf("off \n");
        rt_pin_write(LED_PIN, PIN_LOW);
    } else {
        rt_kprintf("not on/off \n");
    }
    return 0;
}


void led_device_init(void) {
    rt_device_t led_dev = NULL;
    led_dev = rt_device_create(RT_Device_Class_Char, 32);
    if (led_dev == RT_NULL) {
        rt_kprintf("led_device_init err\n");
        return ERROR;
    }

    led_dev->open = led_open;
    led_dev->write = led_write;
    led_dev->close = led_close;

    rt_device_register(led_dev, "led", RT_DEVICE_FLAG_RDWR);
}

INIT_BOARD_EXPORT(led_board_init); // 配置led工作模式
INIT_DEVICE_EXPORT(led_device_init); // 驱动初始化
MSH_CMD_EXPORT(led,  "led on/off");
// 使用：
// 1.开灯：
// 		命令行“cd /dev” - > “echo "on" led”
// 		命令行“led on”			// 类似于裸机方式，直接操控
// 		命令行“led on_posix” 	// 使用posix标准，如open();
// 		命令行“led on_rtt”		// 使用rtt的函数，如rt_device_open();
// 2.关灯
// 		将上面on替换成off就是关灯命令
~~~

#### 2.应用开发

~~~c
// 上面int led(int argc, char **argv)函数编写了应用demo
~~~

