''' E-mail functionality '''
import smtplib
import io_api.logger as logger


def get_msg_from_name(name, player_data):
    ''' Returns message to email to player containing role. '''
    return 'Hi ' + name + '! Your role for this round is ' +\
           player_data[name].get_role_name() + '.'


def send_email(to_email, message):
    ''' Sends an email with a certain message. '''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    game_master_email = 'mafia.storyteller@gmail.com'
    game_master_passwd = '^34Qnmjgl!leIIkV7UdSxabx$&6pFG&Y'
    server.login(game_master_email, game_master_passwd)

    try:
        server.sendmail(game_master_email, to_email, message)
    except smtplib.SMTPRecipientsRefused:
        logger.log_debug('E-mail address not valid.')

    server.quit()
