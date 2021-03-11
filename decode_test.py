def huffman_decode(dictionary, text):
    res = ""
    while text:
        for k in dictionary:

            if text.startswith(k):
                res += dictionary[k]
                text = text[len(k):]
    return res

print(huffman_decode({ '0':'a' ,'100': 'd','101' :'c' ,  '11': 'p'}, '0101011000000111111111111101100'),'_-_-_-_-')
