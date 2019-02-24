from tkinter import *

COLORS = ["red","green","blue","brown","orange","purple"]
NOBODY = "NONE"

assassinatedPerson = NOBODY
checkedPerson = NOBODY
savedPerson = NOBODY

def createVotingScreen(player_window, player_names, vote_function): #populates all voting screens

    top_frame = Frame(player_window)
    top_frame.pack()

    bottom_frame = Frame(player_window)
    bottom_frame.pack()

    numberOfPlayers = len(player_names)
    for i in range(0, numberOfPlayers):
        playerName = player_names[i]
        if (i < numberOfPlayers / 2):
            currFrame = top_frame
        else:
            currFrame = bottom_frame
        b = Button(currFrame, fg=COLORS[i % len(COLORS)], height=20, width=17,
                   text=playerName, command=vote_function(player_window, playerName))
        b.pack(side=LEFT)

    player_window.mainloop()  # make sure buttons are constantly displayed

def dayVote(player_names):
    playerVotes = {}
    for playerName in player_names:
        playerVotes[playerName] = 0
    playerVotes[NOBODY] = 0
    for playerName in player_names:

        currWindow = Tk()
        currPlayer = playerName
        currWindow.title("DAY PHASE: " + currPlayer + " votes ")

        def dayVoteFunction(playerWindow,playerName):
            def callback():
                playerVotes[playerName] += 1
                playerWindow.destroy()
            return callback

        createVotingScreen(currWindow, player_names, dayVoteFunction)


    hangedPlayer = NOBODY
    for playerName in player_names:
        if (playerVotes[playerName] > len(player_names)/2):
            hangedPlayer = playerName
    print("The victim was: " + hangedPlayer)
    return hangedPlayer

def nightAssassinVote(town_names):
    currWindow = Tk()
    currWindow.title("NIGHT PHASE: " +  "Assassins kill: ")

    def assassinVoteFunction(playerWindow, playerName):
        def callback():
            global assassinatedPerson
            assassinatedPerson = playerName
            playerWindow.destroy()

        return callback

    createVotingScreen(currWindow, town_names, assassinVoteFunction)

    global assassinatedPerson
    return assassinatedPerson

def nightCopVote(player_names):
    currWindow = Tk()
    currWindow.title("NIGHT PHASE: " +  "Cop checks: ")

    def copVoteFunction(playerWindow, playerName):
        def callback():
            global checkedPerson
            checkedPerson = playerName
            playerWindow.destroy()

        return callback

    createVotingScreen(currWindow, player_names, copVoteFunction)

    global checkedPerson
    return checkedPerson

def nightDoctorVote(player_names):
    currWindow = Tk()
    currWindow.title("NIGHT PHASE: " +  "Doctor saves: ")

    def doctorVoteFunction(playerWindow, playerName):
        def callback():
            global savedPerson
            savedPerson = playerName
            playerWindow.destroy()

        return callback

    createVotingScreen(currWindow, player_names, doctorVoteFunction)

    global savedPerson
    return savedPerson




nightDoctorVote(["Marcel","Ionela","Trump","Putin","Atcineva"])