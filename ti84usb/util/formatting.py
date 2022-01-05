def format_bytes(bytes, n=4):
    hex = bytes.hex().upper()
    return " ".join([hex[i:i + n] for i in range(0, len(hex), n)])