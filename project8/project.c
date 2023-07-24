#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <oqs/common.h>
#include <arm_neon.h>

#define PQC_AES128_STATESIZE 88
typedef struct {
	uint64_t sk_exp[PQC_AES128_STATESIZE];
} aes128ctx;

static inline void aes128_armv8_encrypt(const unsigned char* rkeys, const unsigned char* n, unsigned char* out) {
	uint8x16_t temp = vld1q_u8(n);

	temp = vaeseq_u8(temp, vld1q_u8(rkeys));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 16));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 32));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 48));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 64));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 80));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 96));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 112));
	temp = vaesmcq_u8(temp);
	temp = vaeseq_u8(temp, vld1q_u8(rkeys + 128));
	temp = vaesmcq_u8(temp);

	temp = vaeseq_u8(temp, vld1q_u8((rkeys + 144)));
	temp = veorq_u8(temp, vld1q_u8((rkeys + 160)));

	vst1q_u8(out, temp);
}

void oqs_aes128_enc_sch_block_armv8(const uint8_t* plaintext, const void* _schedule, uint8_t* ciphertext) {
	const unsigned char* schedule = (const unsigned char*)_schedule;
	aes128_armv8_encrypt(schedule, plaintext, ciphertext);
}

void oqs_aes128_ecb_enc_sch_armv8(const uint8_t* plaintext, const size_t plaintext_len, const void* schedule, uint8_t* ciphertext) {
	assert(plaintext_len % 16 == 0);
	const aes128ctx* ctx = (const aes128ctx*)schedule;

	for (size_t block = 0; block < plaintext_len / 16; block++) {
		oqs_aes128_enc_sch_block_armv8(plaintext + (16 * block), (const void*)ctx->sk_exp, ciphertext + (16 * block));
	}
}

int main() {
	const uint8_t plaintext[] = {
		0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
		0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF
	};
	const size_t plaintext_len = sizeof(plaintext);

	const uint8_t key[PQC_AES128_STATESIZE] = {
		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
	};

	uint8_t ciphertext[plaintext_len];
	aes128ctx ctx;
	memcpy(ctx.sk_exp, key, sizeof(key));

	oqs_aes128_ecb_enc_sch_armv8(plaintext, plaintext_len, &ctx, ciphertext);

	printf("Plaintext: ");
	for (size_t i = 0; i < plaintext_len; i++) {
		printf("%02X ", plaintext[i]);
	}
	printf("\n");

	printf("Ciphertext: ");
	for (size_t i = 0; i < plaintext_len; i++) {
		printf("%02X ", ciphertext[i]);
	}
	printf("\n");

	return 0;
}
