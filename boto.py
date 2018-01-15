"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    if "My name is" in user_message:
        return json.dumps({"animation": "bored", "msg": "What a boring name."})
    elif user_message.endswith('?'):
        return json.dumps({"animation": "takeoff", "msg": "It's too early for questions. Ask me again tomorrow."})
    elif any('fuck') in user_message:
        return json.dumps({"animation": "crying", "msg": "Ouch, that hurt my feelings."})

# def swear_func(user_message):
    # list_swear_words = ['fuck', 'shit', 'bullshit', 'motherfucker', 'dipshit', 'ass', 'loser', 'mofo', 'asshole']
    # user_message.split(",")
    # if "fuck" in user_message:
    # return json.dumps({"animation": "crying", "msg": "Ouch, that hurt my feelings."})
    # print "yuck"
    # return user_message

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
