import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import datetime

def base_session_start_callback(context, roster, timestamp):
    logging.warning("Using a base callback, consider changing")
    logging.warning(context)
    logging.warning(roster)
    logging.warning(timestamp)

def base_muc_callback(context, sender, body, timestamp):
    logging.warning("Using a base callback, consider changing")
    logging.warning(context)
    logging.warning(sender)
    logging.warning(body)
    logging.warning(timestamp)

def base_muc_got_online_callback(context, nick, role, room, timestamp, basepresence):
    logging.warning("Using a base callback, consider changing")
    logging.warning(context)
    logging.warning(nick)
    logging.warning("Role: {}".format(role))
    logging.warning(room)
    logging.warning(timestamp)

def base_muc_got_offline_callback(context, nick, role, room, timestamp, basepresence):
    logging.warning("Using a base callback, consider changing")
    logging.warning("OFFLINE")
    logging.warning(context)
    logging.warning(nick)
    logging.warning("Role: {}".format(role))
    logging.warning(room)
    logging.warning(timestamp)
    context.send_message(mto=basepresence["from"].bare,
                         mbody="Goodbye {}".format(nick),
                         mtype="groupchat")


class BaseBot(ClientXMPP):

    session_start_callback = base_session_start_callback
    muc_callback = base_muc_callback
    muc_got_online_callback = base_muc_got_online_callback
    muc_got_offline_callback = base_muc_got_offline_callback


    def __init__(self, jid, password, room, nick, plugins=[]):
        ClientXMPP.__init__(self, jid, password)

        for plugin in plugins:
            self.register_plugin(plugin)

        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::{}::got_offline".format(self.room),
                               self.muc_offline)
        self.add_event_handler("muc::{}::got_online".format(self.room),
                               self.muc_online)

    def muc_online(self, presence):
        muc = presence["muc"]
        nick = muc["nick"]
        role = muc["role"]
        room = muc["room"]

        self.muc_got_online_callback(nick, role, room, datetime.datetime.now(), presence)

    def muc_offline(self, presence):
        muc = presence["muc"]
        nick = muc["nick"]
        role = muc["role"]
        room = muc["room"]

        self.muc_got_offline_callback(nick, role, room, datetime.datetime.now(), presence)

    def muc_message(self, msg):
        if msg["mucnick"] != self.nick:
            self.muc_callback(msg["mucnick"], msg["body"], datetime.datetime.now())

    def session_start(self, event):
        self.send_presence()
        self.plugin["xep_0045"].joinMUC(self.room, self.nick, wait=True)
        #roster = self.get_roster()
        #self.session_start_callback(roster)


    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            msg.reply("Thanks for sending\n{}".msg).send()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname) -8s %(message)s")

    xmpp = BaseBot("crubot@livecoding.tv", "streampassword")
    xmpp.register_plugin("xep_0045")
    xmpp.connect()
    xmpp.process(block=True)
