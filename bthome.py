# Adapted from:
# https://github.com/Bluetooth-Devices/bthome-ble/blob/main/src/bthome_ble/bthome_v2_encryption.py
"""Example showing encoding and decoding of BTHome v2 advertisement"""

import binascii
from bluetooth import BLE
import mbedtls


def parse_value(data: bytes) -> dict[str, float]:
    """Parse decrypted payload to readable BTHome data"""
    vlength = len(data)
    if vlength >= 3:
        temp = round(int.from_bytes(data[1:3], "little", False) * 0.01, 2)
        humi = round(int.from_bytes(data[4:6], "little", False) * 0.01, 2)
        print("Temperature:", temp, "Humidity:", humi)
        return {"temperature": temp, "humidity": humi}
    print("MsgLength:", vlength, "HexValue:", data.hex())
    return {}


def encrypt_payload(
    data: bytes,
    mac: bytes,
    uuid16: bytes,
    sw_version: bytes,
    count_id: bytes,
    key: bytes,
) -> bytes:
    """Encrypt payload."""
    nonce = b"".join([mac, uuid16, sw_version, count_id])  # 6+2+1+4 = 13 bytes
    print(len(nonce))
    print(len(key))
    result = mbedtls.aes_encrypt("AES-128-CCM", key, nonce, data, 4, b"")
    ciphertext = result[:-4]
    mic = result[-4:]
    print("MAC:", mac.hex())
    print("Binkey:", key.hex())
    print("Data:", data.hex())
    print("Nonce:", nonce.hex())
    print("Ciphertext:", ciphertext.hex())
    print("MIC:", mic.hex())
    return b"".join([uuid16, sw_version, ciphertext, count_id, mic])


# =============================
# main()
# =============================
def main() -> None:
    """Example to encrypt and decrypt BTHome payload."""
    print()
    print("====== Test encode -----------------------------------------")
    data = bytes(bytearray.fromhex("02CA0903BF13"))  # BTHome data (not encrypted)
    parse_value(data)  # Print temperature and humidity

    ble = BLE()
    ble.active(True)
    
    print()
    print("Preparing data for encryption")
    count_id = bytes(bytearray.fromhex("00112233"))  # count id (change every message)
    mac = ble.config('mac')[1]
    uuid16 = b"\xD2\xFC"
    sw_version = b"\x41"
    bindkey = binascii.unhexlify("231d39c1d7cc1ab1aee224cd096db932")

    payload = encrypt_payload(
        data=data,
        mac=mac,
        uuid16=uuid16,
        sw_version=sw_version,
        count_id=count_id,
        key=bindkey,
    )
    print()
    print("Encrypted data:", payload.hex())
    print("payload length: ", len(payload))
    adv_data = bytes([0x02, 0x01, 0x06, len(payload)+1, 0x16])+payload
    print("adv data: ", adv_data)
    
    ble.gap_advertise(200, adv_data=adv_data, connectable=False)
    while True:
        pass
    

if __name__ == "__main__":
    main()