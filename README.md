# bthome_v2_pico_w
An example of how to send bthome v2 advertising encrypted data with raspberry pi pico W

This example has been possible with the great help of [Carglglz](https://github.com/Carglglz/mpy-mbedtls) .

This example runs on a custom version of micropython - MicroPython v1.20.0-328-g01c758e26-dirty on 2023-08-02; Raspberry Pi Pico W with RP2040
In order to compile this version please follow the instructions in this repo [mpy-mbedtls](https://github.com/Carglglz/mpy-mbedtls).

Note: By using the full mbedtls configuration (mbedtls_config.h), bluetooth is not being able to start, possible because of not enough memory.
We had to disable these defines:
`
#define MBEDTLS_PEM_PARSE_C
#define MBEDTLS_PEM_WRITE_C
#define MBEDTLS_BASE64_C
`
and also comment out these functions:
mod_mbedtls.c: mbedtls_pk_write_key_pem
x509/mod_x509.c: mbedtls_x509write_csr_pem

For a more detailed view visit this issue: https://github.com/Carglglz/mpy-mbedtls/issues/2