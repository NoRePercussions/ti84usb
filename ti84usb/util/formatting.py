def format_bytes(bytes, n=4):
    if type(bytes) is int:
        bytes = bytes.to_bytes(2, 'big')
    hex = bytes.hex().upper()
    return " ".join([hex[i:i + n] for i in range(0, len(hex), n)])