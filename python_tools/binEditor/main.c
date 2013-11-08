#include <stdio.h>

/***************驱动代码区结构***************
  0~ 7字节: 驱动区头部标识				
	 8字节: 驱动内容起始位
     9字节: 驱动数据段长度
	10字节: 寄存器地址位数
	11字节: 每次写寄存器的数据位数
 12~15字节: 预留给用户自定义
  16~ 字节: 驱动数据段                   
	 ****驱动数据格式*************
	 操作方式 + 操作参数
	 操作方式:	0x1写数据  0x2延时
	 操作参数:
		写数据: m位地址 n位数据
		延时:	延时毫秒数
	 *****************************
 最后8字节: 驱动区结束标识                
********************************************/
const unsigned char driver_array[] = {
	'x','l','s','-','l','c','d',':',
	0x10,0x24,0x8, 0x8,'-','-','-','-',
	0x1, 0x1, 0x1, 0x0,
	0x1, 0x2, 0x2, 0x0,
	0x1, 0x3, 0x3, 0x0,
	0x1, 0x4, 0x4, 0x0,
	0x2, 0xA, 0x0, 0x0,
	0x1, 0x5, 0x5, 0x0,
	0x1, 0x6, 0x6 ,0x0,
	0x1, 0x7, 0x7, 0x0,
	0x1, 0x8, 0x8, 0x0,
	'd','r','v','-','e','n','d',';'
};
#define DRIVER_OFFSET	  8
#define DRIVER_LEN		  9
#define DRIVER_A_SIZE    10
#define DRIVER_W_SIZE    11
#define DRIVER_WRITE	0x1
#define DRIVER_SLEEP	0x2

int main(int argc, char * argv[])
{
	unsigned int i;
	for (i = driver_array[DRIVER_OFFSET]; i < driver_array[DRIVER_OFFSET] + driver_array[DRIVER_LEN]; ) {
		unsigned char operator = driver_array[i];
		unsigned char address;
		unsigned int value;
		if (DRIVER_WRITE == operator) {
			if (0x8 == driver_array[DRIVER_A_SIZE]) {
				address = driver_array[++i];
			}
			if (0x8 == driver_array[DRIVER_W_SIZE]) {
				value = driver_array[++i];
			}
			else if (0x16 == driver_array[DRIVER_W_SIZE]) {
				value = driver_array[++i] * 16 + driver_array[++i];
			}
			else {
				printf("invalid value size!");
				return 1;
			}
				printf("write data %x in %x\n", value, address);
		}
		else if (DRIVER_SLEEP == operator) {
			value = driver_array[++i];
			printf("sleep %d ms\n", value);
		}
		else {
			printf("invalid operator\n");
			return 2;
		}
		while(driver_array[i] != 0x0)
			i ++;
        while (driver_array[i] == 0x0)
            i ++;
	}
	return 0;
}
