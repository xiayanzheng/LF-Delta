from common.data_hub import Salt
from lfcomlib.Jessica import Security


class Encrypt(Security.Core):

    def main(self):
        while True:
            user_input = input("Pls input encrypt text or input 'qt' to exit.> ")
            if user_input == 'qt':
                exit()
            split_text = input("Split Text> ")
            if split_text == "":
                user_input_split = [user_input]
            else:
                user_input_split = user_input.split(split_text)
            print("Encrypted Message")
            for msg in user_input_split:
                encrypted = self.encrypt(Salt.sec, msg)
                print("{} ====> {}".format(msg, encrypted.decode()))
