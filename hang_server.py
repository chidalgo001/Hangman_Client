from socket import*
import random

# List used to set a word for the game, chosen at random.
# add more to increase the list.

word_list = ['battery' , 'jazz' , 'rhinocerous' , 'server' , 'mix' , 'face' , 'glass' , 'kiosk' , 'silver' ,
             'bear' , 'platipus' , 'dentistry' , 'keyboard' , 'dragonborn' , 'sword' , 'ostrich' , 'coinage' ,
             'cruise' , 'vixen' , 'adventurer' , 'explorer' , 'impossible' , 'rattlesnake' , 'shuffling' ,
             'cryptography' , 'documentation' , 'random' , 'TROLLED' , 'parameters' , 'hunt' , 'python' , 
             'necromancer' , 'merfolk' , 'wizzard' , 'lizzard' , 'gizzard' , 'headache' , 'hornet' , 'pie' ,
             'die' , 'debug' , 'team' , 'build' , 'floral' , 'oral' , 'coral' , 'caricature' , 'expedite' , 
             'overflow' , 'deformation' , 'flicker' , 'blinker' , 'thinker' , 'though' , 'cough' , 'afloat' ,
             'deathclaw' , 'grunt' , 'grim' , 'buoyancy' , 'failure' , 'optimistic' , 'cheerful' , 'exception' ,
             'analyzer' , 'handkerchief' , 'rhythm' , 'weird' , 'millennium' , 'pharaoh' , 'ecstasy' , 'pronounciation' ,
             'arctic' , 'recommend' , 'deductible' , 'encryption' , 'partitioning' , 'flank' , 'plank' , 'blank' , 'zoo',
             'ostrich' , 'sphynx' , 'transitive' , 'skeleton', 'paradox','asphyxiation' , 'deprive' , 'monotone' , 'suffocation']
#-----------------------
# global variables

global hidden
global actual_word
global word_not_set
global counter
global cur_player

#------------------------
# initialization of global variables
counter = 0
word_not_set = True
actual_word = '*'
hidden = ''
cur_player = '' 

#------------------------
# Program constants

servername = '127.0.0.1'
port = 12000
clients = []
players = []

INIT_COUNT = 6
RLET = "RLET "
CNTR = "CNTR "
QUIT = "QUITCOMM"
SETWRD = "SETWRD "
SETWRD2 = "SETWRD2 "
CHECKSET = "CHECKSET "
UPDATEWRD = "UPDATEWRD "


def broadcast( clients , message , sock , addr):

    tokens = message.split()

    for client in clients:

        if (tokens[0] == 'SETWRD'):
            handle_setword( client , message , sock , addr , tokens[0])

        if( message == '!^q!' and str(client) == str(cur_player)):
            sock.sendto("\nYou Won! Congratulations!\n".encode() , client)

        elif( message == '!^q!'):
            sock.sendto("\nYou were HANGED! Game Over!\n".encode() , client)

        else:
            if( message != '!^q!' ):
                sock.sendto(message.encode() , client)
            

def handle_setword( client , message , sock , addr , word):
    
    if (client != addr and word == 'SETWRD'):

        sock.sendto(message.encode() , client)
            

    elif (client == addr and word == 'SETWRD'):
        
        print("nothing")
           
def hide_word( word ):
    
    global hidden 

    hidden = '*' * len(word)

    return hidden

def checkset(clients , servsocket , addr):

    set = CHECKSET + str(word_not_set)
    broadcast(clients , set , servsocket , addr)

def player_quit(clients , servsocket , addr , player):

    
    left = player + " LEFT THE CHAT ROOM.\n"
    servsocket.sendto(QUIT.encode() , addr)
    broadcast(clients , left , servsocket , addr)
    clients.remove(addr)
    

def setwrd(clients , servsocket , addr , player , word):

    global word_not_set , actual_word , counter , hidden , cur_player

    if(word_not_set == True):

        counter = INIT_COUNT
        cur_player = str(addr)

        print("this is the current player: " + cur_player)

        message = player + " has set a word in play.\n"
        print(message)

        message2 = "Incorrect guesses left: [" + str(counter) + "]\n"
        message3 = CNTR + str(counter)

        actual_word = word
        hidden = hide_word(actual_word)

        update = UPDATEWRD + actual_word + " True"
        broadcast(clients , update , servsocket , addr)

        set = tokens[1] + " " + hidden
        print("This is set: " + set)

        broadcast(clients , message , servsocket , addr)
        broadcast(clients , set , servsocket , addr)
        broadcast(clients , message2 , servsocket , addr)
        broadcast(clients , message3 , servsocket , addr)


servsocket = socket(AF_INET , SOCK_DGRAM)
servsocket.bind((servername , port))

print("Ready to receive:")



while True:

    try:

        message , addr = servsocket.recvfrom(1024)

        print(str(addr) + " sent " + message.decode() )#---tracer for msgs rcvd from clients
        
        modmsg = message.decode()
        tokens = modmsg.split()

        if addr not in clients:

            #this will add the username into the list of connected addresses
            #-----------------------
            clients.append(addr)
            welcome = str( message.decode() ) + " has joined the chat\n"
            broadcast(clients , welcome , servsocket , addr)
            #-----------------------

        else:
            #this else will decode any command sent by a client.
            if tokens[1] == '^q':

                player = tokens[0]
                player_quit(clients , servsocket , addr , player )


            elif tokens[1] == 'CHECKSET':

                checkset(clients , servsocket , addr)

            elif tokens[1] == 'SETWRD':

                player = tokens[0]
                word = tokens[2].lower()

                setwrd(clients , servsocket , addr , player , word)

            elif tokens[1] == 'RLET':

                index  = 0
                player = tokens[0]
                letter = tokens[2]
                count = len(actual_word)
                temp = ''
                hit = '0' #--- indictor that a letter has matched (0-false , 1-true)

                while index < count:

                    if ( actual_word[index] == letter ):

                        print( str( actual_word[index] ) + " This is index" )#---tracer for letter found in word
                        temp = temp + letter

                        hit = '1'

                    else:

                        temp = temp + hidden[index]

                    index = index + 1

                if hit == '1':

                    message = "Player " + player + " guessed a letter\n"
                    broadcast(clients , message , servsocket , addr)

                if hit == '0':

                    counter = counter - 1
                    message = "Player " + player + " failed to guess a letter\n"
                    message2 = "Incorrect guesses left: [" + str(counter) + "]\n"
                    usedletter = RLET + letter
                    message3 = CNTR + str(counter)

                    broadcast(clients , usedletter , servsocket , addr)
                    broadcast(clients , message , servsocket , addr)
                    broadcast(clients , message2 , servsocket , addr)
                    broadcast(clients , message3 , servsocket , addr)


                if counter == 0:

                    print("GAME OVER " + str(counter) )

                    #------------- this block sends the right message to the player who
                    #------------- won or lost
                    won = "!^q!"
                    broadcast(clients , won , servsocket , cur_player)
                    message = "The word has been displayed.\n"
                    broadcast(clients , message , servsocket , addr)
                    #------------------------------------------------------------------

                    set = SETWRD2 + actual_word + " False"
                    broadcast(clients , set , servsocket , addr)

                    cur_player = '' #resets the current player

                hidden = temp
                    
                if (hidden == actual_word):

                    win_image = CNTR + " W" 
                    winmsg = tokens[0] + " guessed the word!!\n" 
                    broadcast(clients , win_image , servsocket , addr)
                    broadcast(clients , winmsg , servsocket , addr)
                    set = SETWRD2 + hidden + " False"

                else:
                    if counter != 0:
                        set = SETWRD2 + hidden + " True"

                broadcast(clients , set , servsocket , addr) # this will update the players with the status of the 
                #hidden word

            elif tokens[1] == 'GUESSWRD':

                player = tokens[0]
                guessword = tokens[2]

                if (actual_word == guessword):

                    message = "Player " + player + " guessed the correct word!\n"
                    set = SETWRD2 + actual_word + " False"
                    win_image = CNTR + " W" 

                    broadcast(clients , set , servsocket , addr) # this will display to all players the actual word
                    broadcast(clients , message , servsocket , addr) # message to all players that someone guessed the word
                    broadcast(clients , win_image , servsocket , addr) 
                    
                else:
                    counter = counter - 2

                    if counter < 0 :
                        counter = 0

                    message2 = "Incorrect guesses left: [" + str(counter) + "]\n"
                    message = player + " tried to guess the word! But failed.\n"
                    message3 = CNTR + str(counter)

                    broadcast(clients , message , servsocket , addr) # message to all players that someone failed a guess
                    broadcast(clients , message2 , servsocket , addr)
                    broadcast(clients , message3 , servsocket , addr) # updates every player with the counter

                    if counter == 0:

                        print("GAME OVER " + str(counter) )

                    #------------- this block sends the right message to the player who
                    #------------- won or lost
                        won = "!^q!"
                        broadcast(clients , won , servsocket , cur_player)
                        message = "The word has been displayed.\n"
                        broadcast(clients , message , servsocket , addr)
                    #-------------

                        set = SETWRD2 + actual_word + " False"
                        broadcast(clients , set , servsocket , addr)

                        cur_player = '' #resets the current player

            elif tokens[1] == 'RANDOMWRD':

                chosen = random.choice(word_list)

                actual_word = chosen
                counter = INIT_COUNT   
                hidden = hide_word(actual_word)     
                                        
                update = UPDATEWRD + actual_word + " True"

                print("Random: " + actual_word )#---tracer

                message = tokens[0] + " has set a random word in play.\n"
                print(message)#---tracer

                message2 = "Guesses left: [" + str(counter) + "]\n"
                message3 = CNTR + str(counter)

                set = SETWRD2 + hidden + ' True'
                print("This is set: " + set)#---tracer

                broadcast(clients , update , servsocket , addr)
                broadcast(clients , message , servsocket , addr)
                broadcast(clients , set , servsocket , addr)
                broadcast(clients , message2 , servsocket , addr)
                broadcast(clients , message3 , servsocket , addr)


            else:

                broadcast( clients , modmsg , servsocket , addr)

    except:
        pass
        
rT.join()
servsocket.close()
