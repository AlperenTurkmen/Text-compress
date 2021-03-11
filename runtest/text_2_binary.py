def to_bytes(data):
    b = bytearray()
    for i in range(0, len(data), 8):
        b.append(int(data[i:i+8], 2))
    return bytes(b)
file = open('binfile.txt', 'r')
string = file.read()
file.close()
f=open("binfile.bin","bw")
f.write(to_bytes(string))
f.close()
print(to_bytes(string))