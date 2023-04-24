from utils.texts import START_COMMAND_DESCRIPTION


def get_frame(frame=1000):
    return ('http://framex-dev.wadrid.net/api/video' +
            '/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)' +
            f'-wbSwFU6tY1c/frame/{frame}/')


def bisect(chat, message):
    if chat["right"] - chat["left"] < 1:
        return chat
    if message == 'yes':
        chat['right'] = chat['mid']
        chat['attempts'] = chat['attempts'] + 1
    if message == 'no':
        chat['left'] = chat['mid']
        chat['attempts'] = chat['attempts'] + 1
    chat['mid'] = int(((chat['right'] + chat['left']) / 2))
    return chat


def help_response_html():
    response = "<b>&#128640;Welcome to the Rocket Launch Bot!&#128640;</b>\n\n"
    response += "This bot shows you images of rocket launches and asks you "
    response += "if the rocket has been launched yet.\n\n"
    response += "<b>Available commands:</b>\n"
    response += "&#128073;<code>/help</code> - Shows this help message.\n"
    response += "&#128073;<code>/start</code> - "
    response += f"{START_COMMAND_DESCRIPTION}.\n\n"
    response += "Check out the <a href='https://github.com/juanmarcoscabezas"
    response += "/when-did-rocket-launch-bot'>GitHub repository</a> "
    response += "for the source code and more information."
    return response


def default_response_html():
    response = "<b>&#128532;I'm sorry, I don't understand your message</b>"
    response += "&#128532;\n\n"
    response += "<b>Available commands:</b>\n"
    response += "&#128073;<code>/help</code> - Shows the help command.\n"
    response += f"&#128073;<code>/start</code> - {START_COMMAND_DESCRIPTION}."
    response += "\n\n"
    return response


def congratulations_html(frame):
    response = "<b>&#127878;Congratulations&#127878;</b>\n\n"
    response += "We have found the frame in which the rocket launches.\n"
    response += f'The frame number is "{frame}"&#128640;'
    return response


def not_found_html():
    response = "<b>&#128546;I'm sorry&#128546;</b>\n\n"
    response += "We couldn't find the exact frame when the rocket "
    response += " was launched.\n"
    response += 'Please try again &#128257;'
    return response
