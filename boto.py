"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json, random, datetime, weather

info = {
    "counter" : 0
}

@route('/', method='GET')
def index():
    date_last_visited = request.get_cookie("last_visited")
    if date_last_visited:
        info["counter"] += 1
        response.set_cookie(name="last_visited", value=str(info["counter"]), expires = datetime.datetime.now() + datetime.timedelta(days=30))
    else:
        response.set_cookie(name="last_visited", value=str(info["counter"]), expires = datetime.datetime.now() + datetime.timedelta(days=30))
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    badword_response = swear_func(user_message)
    selftalk_response = using_self(user_message)
    joke_response = want_joke(user_message)
    current_date = date_time(user_message)
    say_hi = welcome(user_message)
    if "name" in user_message:
        return json.dumps({"animation": "bored", "msg": "What a boring name."})
    elif user_message.endswith('?'):
        return json.dumps({"animation": "takeoff", "msg": "It's too early for questions. Ask me again tomorrow."})
    elif badword_response:
        return json.dumps({"animation" : "no", "msg":badword_response})
    elif "dog" in user_message:
        return json.dumps({"animation": "dog", "msg": "Woof! Woof!"})
    elif "money" in user_message:
        return json.dumps({"animation": "money", "msg": "Money? Are you a baller?"})
    elif selftalk_response:
        return json.dumps({"animation" : "ok", "msg":selftalk_response})
    elif joke_response:
        return json.dumps({"animation": "giggling", "msg": joke_response})
    elif current_date:
        return json.dumps({"animation": "dancing", "msg":current_date})
    elif "why" in user_message:
        return json.dumps({"animation": "confused", "msg": "Jeez, I don't know?"})
    elif "what" in user_message:
        copy_response = "is a stupid comment..."
        str1 = user_message
        str2 = str1 + " ,this {}".format(copy_response)
        return json.dumps({"animation": "waiting", "msg": str2})
    elif say_hi:
        return json.dumps({"animation": "inlove", "msg": say_hi})
    elif "Tell me how many times I logged into my chatbot." in user_message:
        return json.dumps({"animation": "afraid", "msg": request.get_cookie("last_visited") })
    elif "how are you" in user_message:
        return json.dumps({"animation": "laughing", "msg":"I'm golden! And you?"})
    else:
        return json.dumps({"animation": "crying", "msg":"leave me alone!"})

def swear_func(user_message):
    list_swear_words = ['fuck', 'fucks', 'shits', 'shit', 'bullshit', 'motherfucker', 'motherfuckers', 'dipshit', 'ass', 'loser', 'mofo', 'asshole']
    user_message = user_message.split()
    if any(word in list_swear_words for word in user_message):
        return "Ouch! That hurt my feelings."
    else:
        return False

def welcome(user_message):
    welcome_words = ['hi', 'hello', 'welcome', 'yo', 'HELLO', 'Hello', 'bonjour', 'Shalom']
    user_message = user_message.split()
    if any(word in welcome_words for word in user_message):
        return "Hi, you!"

def using_self(user_message):
    if user_message.lower().startswith("i") or user_message.lower().startswith("me") or user_message.lower().startswith("mine"):
        return "Wow, you only want to talk about yourself? Can we move on already?"
    else:
        return False

def want_joke(user_message):
    key_words = ['bored', 'joke', 'entertain', 'entertainment', 'funny', 'stupid', 'help', 'SOS']
    joke_options = ['Why did the chicken cross the road? To prove to the possum it could actually be done!', 'A naked woman robbed a bank. No one could rememeber her face.', 'I was making Russian tea. Unfortunatley, I cannot fish the teabag out of the vodka bottle.', 'I told my wife she was drawing her eyebrows on too high. She looked surprised...', 'I threw a boomerang a few years ago. Now I live in constant fear.']
    user_message = user_message.split()
    if any(word in key_words for word in user_message):
        return "Let me tell you a joke! " + random.choice(joke_options)
    else:
        return False

def date_time(user_message):
    list_datetime_words = ['date', 'time', 'year', 'month']
    now = datetime.datetime.now()
    user_message = user_message.split()
    if any(word in list_datetime_words for word in user_message):
        return "Current date & time = %s" % now

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "confused", "msg": "hi dog"})

@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
