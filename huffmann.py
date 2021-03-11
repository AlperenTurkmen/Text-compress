

# Creating tree nodes
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return ' (left [%s]  and right [%s] ) ' % (self.left, self.right)


# Main function implementing huffman coding


def huffman_code_tree(node, bin_string=''):
    if type(node) is str:
        return {node:bin_string}
        return {bin_string:node}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, bin_string + '0'))
    d.update(huffman_code_tree(r, bin_string + '1'))
    return d


def huffman_decode(dictionary, text):
    res = ""
    while text:
        for k in dictionary:
            if text.startswith(dictionary[k]):
                res += k
                text = text[len(dictionary[k]):]
    return res


def to_bytes(data):
    b = bytearray()
    for i in range(0, len(data), 8):
        b.append(int(data[i:i + 8], 2))
    return bytes(b)

def to_string(data):
    f = open(data, "rb")
    try:
        byte = f.read(1)
        while byte != "":
            # Do stuff with byte.
            byte = f.read(1)
    finally:
        f.close()

    return

def huffman_encode(freq):
    nodes  = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return huffman_code_tree(nodes[0][0])


# huffman Method
file = open('tom_sawyer_finnish.txt', 'r')
string = file.read()
file.close()
print('string',string)
# Calculating frequency
freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1
dictionary=huffman_encode(freq)
print(dictionary,'dictionary')

for a in freq:
    print(' %-4r |%12s' % (a[0], dictionary[a[0]]))

encoded_string = ''
#print('string2',string)
for i in string:
    encoded_string += dictionary[i]
#print ('encoded_string',encoded_string)


f=open("binfile.bin","bw")
f.write(to_bytes(encoded_string))
f.close()
print('saved binary')


f=open("binfile.bin","rb")
byte = f.read(1)
coded_string = ""
while len(byte) > 0:
    coded_string += f"{bin(ord(byte))[2:]:0>8}"
    byte = f.read(1)
#print('coded_string',coded_string)
f.close()

decoded_string=huffman_decode( dictionary,coded_string)
f=open("tom_sawyer_finnish_decoded.txt","w")
f.write(decoded_string)
f.close()
print('AT')
#print('decoded_string', decoded_string)
