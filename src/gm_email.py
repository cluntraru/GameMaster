import smtplib

def send_email(to_email, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    game_master_email = 'mafia.storyteller@gmail.com'
    game_master_passwd = '^34Qnmjgl!leIIkV7UdSxabx$&6pFG&Y'
    server.login(game_master_email, game_master_passwd)
     
    server.sendmail(game_master_email, to_email, message)
    server.quit()