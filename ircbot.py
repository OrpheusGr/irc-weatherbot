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

def save_settings(settings):
    file = "settings.json"
    with open(file, 'w') as json_file:
        json.dump(settings, json_file)

def on_join(connection, event):
    global settings
    if event.target not in settings["irc"]["channels"]:
        settings["irc"]["channels"].append(event.target)
        save_settings(settings)
        f = open("settings.json", encoding="utf-8")
        settings = json.loads(f.read())
        f.close()
        irc_settings = settings["irc"]
        print(irc_settings)

def on_connect(connection, event):
    global irc_settings
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
        checkf = isweather[1].split("||")
        if checkf == False:
            connection.privmsg(event.target, isweather[1].replace("[bold]", "\x02"))
        else:
            for line in checkf:
                connection.privmsg(event.target, line.replace("[bold]", "\x02"))

def startirct():
    global loopin
    react = irc.client.Reactor()
    c = react.server().connect(irc_settings["server"], irc_settings["port"], irc_settings["nickname"], None, "weather", "I do them weather stuff")
    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("pubmsg", on_pubmsg)
    c.add_global_handler("join", on_join)
    loopin = 1
    while loopin:
        #try:
        time.sleep(0.2)
        react.process_once(0.2)
        #except Exception as err:
           # print("An error has occured. %s" % str(err))
            #pass

startirct()
