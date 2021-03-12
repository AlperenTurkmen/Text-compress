#ECM1414 Continuous Assessment 2021
#Author - Alperen Turkmen
import sys
from datetime import datetime
import json
# This class is a node tree class.
class NodeTree(object):
    '''
    This class has attributes of:
    children: a node can have 2 children, left and right.
    nodes: a node can have 2 children nodes, left and right.
    '''
    def __init__(self, left=None, right=None): #
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return ' (left [%s]  and right [%s] ) ' % (self.left, self.right)

# This is the function that does the huffman coding

def huffman_code_tree(node, bin_string=''):
    '''

    :param node: is the node whose tree we're going to create.
    :param bin_string: is the initial bin_string.
    :return: this function returns a dictionary of d. It contains all the unique binary codes.

    This recursive function creates a huffman code tree,
     it tries to give nodes a binary code until the bottommost node (characters) are reached.
    '''
    if type(node) is str:
        return {node:bin_string}
        return {bin_string:node}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, bin_string + '0')) #update the left child
    d.update(huffman_code_tree(r, bin_string + '1')) #update the right child
    return d

def remove_padding(padded_encoded_text):
    '''

    :param padded_encoded_text: this is the text which we're gonna get rid of its pads.
    :return: returns the raw text, without paddings.
    Normally, My function added zeros to the last byte of my binary file.
    To avoid this situation: I found this solution. It removes paddings carefully.
    '''
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text

def huffman_decode(dictionary, text):
    '''

    :param dictionary: is the dictionary with unique binary codes of characters.
    :param text: is the text that's being decoded.
    :return: returns a decoded version of the code.
    '''
    res = ""
    while len(text)>=1:
        for k in dictionary: #Iterates over all dictionary for each character.
            if text.startswith(dictionary[k]):
                print(len(text),' Bits remaining...')
                res += k
                text = text[len(dictionary[k]):]
    return res


def to_bytes(data):
    '''

    :param data: is the string we need in binary.
    :return: returns a binary file.
    '''
    b = bytearray()
    print('creating binary')
    for i in range(0, len(data), 8):
        b.append(int(data[i:i + 8], 2))
    return bytes(b)


def pad_encoded_text(encoded_text):
    '''

    :param encoded_text: is the encoded text that we're gonna pad.
    :return: returns a padded version of the encoded text.
    '''
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def huffman_encode(freq):
    '''
    This function here creates a huffman tree according to frequencies of characters.
    :param freq: is the dictionary that contains the frequency of each character.
    :return: returns a tree without binary numbers.
    '''
    nodes  = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return huffman_code_tree(nodes[0][0])

start=datetime.now() #Start the timer
# huffman Method
file = open(str(sys.argv[1]), 'r',encoding='UTF-8')
#You can give any file in format UTF-8 as an argument with this py code.
string = file.read()
file.close()
# Calculating frequency
print(datetime.now()-start,'File read time') #The runtime of the fileread.
start=datetime.now() #Start the timer again.
freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1
dictionary=huffman_encode(freq)
#####
json_file = json.dumps(dictionary) #This part saves the dictionary as a json file.
f = open('dictionary.json','w')
f.write(json_file)
f.close()
#####
print(dictionary,'dictionary')
print(datetime.now()-start,'Frequencies are calculated.')
for a in freq:
    print(' %-4r |%12s' % (a[0], dictionary[a[0]]))

encoded_string = ''
for i in string:
    encoded_string += dictionary[i]
encoded_string = pad_encoded_text(encoded_string)

target_file = str(sys.argv[2])
binfile=open(target_file,"bw")
binfile.write(to_bytes(encoded_string))
binfile.close()
print('saved binary')


read_binfile=open(target_file,"rb") #Reads from binary file to start decompressing.
byte = read_binfile.read(1)
coded_string = ""

start=datetime.now() #Start the timer again to calculate decoding time.
while len(byte) > 0:
    coded_string += f"{bin(ord(byte))[2:]:0>8}"
    byte = read_binfile.read(1)
coded_string = remove_padding(coded_string)
print('new coded_string: ', coded_string)
print('While loop for encoding took:',datetime.now()-start)

read_binfile.close()
with open('dictionary.json') as f:
    dictionary_from_json = json.load(f)
start=datetime.now() #Start the timer again to calculate decoding time.
decoded_string=huffman_decode( dictionary_from_json,coded_string) #Uses the dictionary from a json file.
print('string decoded in:',datetime.now()-start)
decoded_txtfile = 'decoded_'+ str(sys.argv[1])
decoded_binfile=open(decoded_txtfile,"w")
decoded_binfile.write(decoded_string)
decoded_binfile.close()

json = json.dumps(dictionary) #Saves the dictionary as a json file.
f = open('dictionary.json','w')
f.write(json)
f.close()
