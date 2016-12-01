import logging
from backends.xmpp import BaseBot

# if msg["mucnick"] != self.nick and self.commandprefix in msg["body"][
#                0]:
#            if msg["body"][0] == self.commandprefix:
#                #command, param = msg["body"].split(" ")
#                splitlist = msg["body"].split(" ")
#                command, param = splitlist[0], splitlist[1:]
#                print command, param

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname) -8s %(message)s")

    xmpp = BaseBot("crubot@livecoding.tv", "streampassword",
                   "cruor99@chat.livecoding.tv", "crubot", ["xep_0045"])
    xmpp.connect()
    xmpp.process(block=True)
