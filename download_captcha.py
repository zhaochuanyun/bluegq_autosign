import recognize


def download():
    for index in range(200):
        print('%d.gif' % (index))
        (loginhash, formhash, seccodehash) = recognize.get_code_info()
        recognize.get_verifycode(recognize.get_code_info(), seccodehash, '%d.png' % (index))


if __name__ == '__main__':
    download()
