from cryptography.fernet import Fernet


def encrypt(my_string):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(my_string.encode("utf-8"))

    with open("encrypted.txt", "w+") as f:
        f.writelines([key.decode("utf-8"), "\n", cipher_text.decode("utf-8")])

    print("Key is:\t{}".format(key.decode("utf-8")))
    print("Encrypted text:\t{}".format(cipher_text.decode("utf-8")))


def decrypt(key, cipher_text):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(cipher_text)


if __name__ == "__main__":
    encrypt("Hello")
