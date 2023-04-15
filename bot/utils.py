import math


def get_frame(frame=1000):
    return ('http://framex-dev.wadrid.net/api/video' +
            '/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)' +
            f'-wbSwFU6tY1c/frame/{frame}/')


def bisect(chat, message):
    if message == 'yes':
        chat['right'] = chat['mid']
        chat['mid'] = int(math.ceil((chat['right'] + chat['left']) / 2))
    if message == 'no':
        chat['left'] = chat['mid']
        chat['mid'] = int(math.ceil((chat['right'] + chat['left']) / 2))
    chat['attempts'] = chat['attempts'] + 1
    return chat
