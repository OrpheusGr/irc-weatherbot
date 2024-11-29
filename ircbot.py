import irc.client
import weathermodule
import time
import json
loopin = 0
weather = weathermodule
f = open("settings.json", encoding="utf-8")
settings = json.loads(f.read())
f.close()
irc_settings = settings["irc"]


def on_connect(connection, event):
    print("Connected successfully")
    for i in irc_settings["channels"]:
        connection.join(i)

def on_pubmsg(connection, event):
    sender = event.source.nick
    msg = event.arguments[0].split()
    isweather = weather.caller(msg, [sender, event.source.host])
    if isweather[0] == "error":
        wreply = "Error: " + isweather[1].replace("[bold]", "\x02")
        connection.privmsg(event.target, wreply)
    elif isweather[0] == "success":
        connection.privmsg(event.target, isweather[1].replace("[bold]", "\x02"))


def startirct():
    global loopin
    react = irc.client.Reactor()
    c = react.server().connect(irc_settings["server"], irc_settings["port"], irc_settings["nickname"], None, "weather", "I do them weather stuff")
    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("pubmsg", on_pubmsg)
    loopin = 1
    while loopin:
        try:
            time.sleep(0.2)
            react.process_once(0.2)
        except Exception as err:
            print("An error has occured. %s" % str(err))
            pass

startirct()
