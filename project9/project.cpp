#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <thread>
#include <windows.h>
#define th_num 16
#define m_bits 10000000


static void dump_buf_32(uint32_t* buf, uint32_t len)
{
	uint32_t i;
	printf("buf:");

	for (i = 0; i < len; i++) {
		printf("%s%02x%s", i % 16 == 0 ? "\r\n\t" : " ",
			buf[i],
			i == len - 1 ? "\r\n" : "");
	}
}

static void dump_buf_8(uint8_t* buf, uint32_t len)
{
	uint32_t i;
	printf("buf:");

	for (i = 0; i < len; i++) {
		printf("%s%02x%s", i % 16 == 0 ? "\r\n\t" : " ",
			buf[i],
			i == len - 1 ? "\r\n" : "");
	}
}


const uint32_t fk[4] = {
	0xa3b1bac6,
	0x56aa3350,
	0x677d9197,
	0xb27022dc
};

const uint32_t ck[32] = {
	0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
	0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
	0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
	0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
	0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
	0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
	0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
	0x10171e25,0x2c333a41,0x484f565d,0x646b7279
};

const uint8_t s_box[256] = {

	0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
	0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
	0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
	0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
	0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
	0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
	0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
	0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
	0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
	0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
	0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
	0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
	0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
	0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
	0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
	0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48
};


uint32_t move(uint32_t data, int length)
{
	uint32_t result = 0;
	result = (data << length) ^ (data >> (32 - length));
	return result;
}


uint32_t t(uint32_t input)
{
	uint8_t b[4] = { input >> 24,input >> 16,input >> 8,input };
	for (int i = 0; i < 4; i++)
	{
		b[i] = s_box[(int)b[i]];
	}
	uint32_t c = (b[0] << 24) ^ (b[1] << 16) ^ (b[2] << 8) ^ b[3];
	c = c ^ move(c, 2) ^ move(c, 10) ^ move(c, 18) ^ move(c, 24);
	return c;
}

void t_1(uint32_t* input, uint32_t* rk)
{
	uint32_t k[50];
	for (int i = 0; i < 4; i++)
	{
		k[i] = input[i] ^ fk[i];
	}

	for (int i = 0; i < 32; i++)
	{
		uint32_t t = k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ ck[i];
		uint8_t b[4] = { t >> 24,t >> 16,t >> 8,t };
		for (int i = 0; i < 4; i++)
		{
			b[i] = s_box[(int)b[i]];
		}
		t = (b[0] << 24) ^ (b[1] << 16) ^ (b[2] << 8) ^ b[3];
		t = t ^ move(t, 13) ^ move(t, 23);
		rk[i] = k[i] ^ t;
		k[i + 4] = rk[i];
		//printf("%u\n", k[i]);
	}
}

void f(uint32_t* input, uint32_t rk, uint32_t* output)
{
	output[0] = input[1];
	output[1] = input[2];
	output[2] = input[3];
	output[3] = input[0] ^ t(input[1] ^ input[2] ^ input[3] ^ rk);
}


uint32_t key[4] = {
   0x01234567,0x89abcdef,
   0xfedcba98,0x76543210
};

void SM4_multhread(uint32_t* rk, uint32_t* plain, int size, int times) {
	uint32_t output[4];
	uint32_t temp[4];
	for (int i = times; i < size; i += 4 * th_num) {
		f(plain + i, rk[0], output);
		for (int i = 1; i < 32; i++)
		{
			for (int i = 0; i < 4; i++)
			{
				temp[i] = output[i];
			}
			f(temp, rk[i], output);
		}
		uint32_t temp1, temp2;
		temp1 = output[0];
		temp2 = output[1];
		output[0] = output[3];
		output[1] = output[2];
		output[2] = temp2;
		output[3] = temp1;
	}
}

void SM4_unrolling(uint32_t* rk, uint32_t* plain, int size) {
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&BegainTime);
	uint32_t output[8];
	uint32_t temp[4];
	uint32_t tempp[4];
	for (int i = 0; i < size; i += 8) {
		f(plain + i, rk[0], output);
		f(plain + i + 4, rk[0], output + 4);
		for (int i = 1; i < 32; i++)
		{
			for (int i = 0; i < 4; i++)
			{
				temp[i] = output[i];
				tempp[i] = output[i + 4];
			}
			f(temp, rk[i], output);
			f(tempp, rk[i], output + 4);
		}
		uint32_t temp1, temp2;
		temp1 = output[0];
		temp2 = output[1];
		output[0] = output[3];
		output[1] = output[2];
		output[2] = temp2;
		output[3] = temp1;
		temp1 = output[4];
		temp2 = output[5];
		output[4] = output[7];
		output[5] = output[6];
		output[6] = temp2;
		output[7] = temp1;
	}
	QueryPerformanceCounter(&EndTime);
	double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
	printf("SM4+两次循环展开用时： %f seconds\n", time);
}

void SM4(uint32_t* rk, uint32_t* plain, int size) {
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&BegainTime);
	uint32_t output[4];
	uint32_t temp[4];
	for (int i = 0; i < size; i += 4) {
		f(plain + i, rk[0], output);
		for (int i = 1; i < 32; i++)
		{
			for (int i = 0; i < 4; i++)
			{
				temp[i] = output[i];
			}
			f(temp, rk[i], output);
		}
		uint32_t temp1, temp2;
		temp1 = output[0];
		temp2 = output[1];
		output[0] = output[3];
		output[1] = output[2];
		output[2] = temp2;
		output[3] = temp1;
	}
	QueryPerformanceCounter(&EndTime);
	double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
	printf("原始SM4用时： %f seconds\n", time);
}



int main()
{
	uint32_t* plain = (uint32_t*)malloc(sizeof(int) * m_bits);
	if (plain == NULL) {
		printf("内存分配不成功！\n");
	}
	else {
		for (int i = 0; i < m_bits; ++i)
		{
			plain[i] = rand();
		}
	}
	uint32_t rk[32];
	t_1(key, rk);


	SM4(rk, plain, m_bits);

	SM4_unrolling(rk, plain, m_bits);

	std::thread th[th_num];
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&BegainTime);
	for (int j = 0; j < th_num; j++)
	{
		th[j] = std::thread(SM4_multhread, rk, plain, m_bits, 4 * j);
	}
	for (int i = 0; i < th_num; i++)
	{
		th[i].join();
	}
	QueryPerformanceCounter(&EndTime);
	double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
	printf("pthread创建线程用时： %f seconds\n", time);
}

