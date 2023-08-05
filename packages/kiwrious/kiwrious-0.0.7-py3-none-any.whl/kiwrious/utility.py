import struct


def to_int16(hex_value):
    value = int(hex_value[0:2], 16) | int(hex_value[2:4], 16) << 8

    if value & (1 << 15):
        value -= 1 << 16
    return round(value, 2)


def to_int16_r(hex_value):
    value = int(hex_value[0:2], 16) | int(hex_value[2:4], 16) << 8

    if value & (1 << 15):
        value -= 1 << 16
    return value


def to_unsigned_int16(hex_value):
    return round(int(hex_value[0:2], 16) | int(hex_value[2:4], 16) << 8, 2)


def to_float32(hex_value):
    hex_value = ''.join([hex_value[x:x + 2] for x in range(6, -2, -2)])
    return round(struct.unpack('!f', bytes.fromhex(hex_value))[0], 2)


def ir_calc(sensor_packet):
    xxx = to_unsigned_int16(sensor_packet[0:4])

    a = struct.unpack('!f', bytes.fromhex(''.join([sensor_packet[x:x + 2] for x in range(10, 2, -2)])))[0]
    b = struct.unpack('!f', bytes.fromhex(''.join([sensor_packet[x:x + 2] for x in range(18, 10, -2)])))[0]
    c = struct.unpack('!f', bytes.fromhex(''.join([sensor_packet[x:x + 2] for x in range(26, 18, -2)])))[0]

    return round(((a * (xxx ** 2)) / (10 ** 5)) + (b * xxx) + c, 2)


def unsigned32(sensor_packet):
    value = string_to_int16(sensor_packet[0]) + string_to_int16(sensor_packet[0]) * 2 ** 8 + string_to_int16(
        sensor_packet[2]) * 2 ** 16 + string_to_int16(sensor_packet[3]) * 2 ** 24
    return value


def string_to_int16(number):
    if number == "a":
        return 10
    elif number == "b":
        return 11
    elif number == "c":
        return 12
    elif number == "d":
        return 13
    elif number == "e":
        return 14
    elif number == "f":
        return 15
    else:
        return int(number)