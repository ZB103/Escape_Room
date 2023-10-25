from tkinter import *

class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
    
    #method to create the rooms
    def createRooms(self):
        global currentRoom, r1, r2, r3, r4, r5

        #Initialize first four rooms
        r1 = Room("Room 1", "imgs/room1.gif")
        r2 = Room("Room 2", "imgs/room2.gif")
        r3 = Room("Room 3", "imgs/room3.gif")
        r4 = Room("Room 4", "imgs/room4.gif")
        r5 = Room("the Secret Room", "imgs/room5.gif")
        
        #Room 1
        #add exits
        r1.addExit("east", r2)
        r1.addExit("south", r3)
        #add grabbables
        r1.addGrabbable("key")
        #add items
        r1.addItem("chair", "Chair just chillin'.")
        r1.addItem("table", "Why is a raven like a writing desk? Also, there's a key on the table...")
        
        #Room 2
        #add exits
        r2.addExit("west", r1)
        r2.addExit("south", r4)
        #add items
        r2.addItem("rug", "Is that the pattern or is that a stain?")
        r2.addItem("fireplace", "Who brought the marshmallows?")
        
        #Room 3
        #add exits
        r3.addExit("north", r1)
        r3.addExit("east", r4)
        #add grabbables
        r3.addGrabbable("book")
        #add items
        r3.addItem("bookshelves", "So much knowledge, so little time...or maybe you're just easily distracted.")
        r3.addItem("statue", "Wow, it's (insert your favorite character here)!!")
        r3.addItem("desk", "Why is a raven like a writing table? also, there's a book on the desk...")
        
        #Room 4
        #add exits
        r4.addExit("north", r2)
        r4.addExit("west", r3)
        r4.addExit("south", None)
        #add grabbables
        r4.addGrabbable("6-pack")
        #add items
        r4.addItem("brewrig", "Not to be confused with a blue pig.")
        r4.addItem("kennel", "The pupper inside looks happy to see you, and sad when you walk away. Poor doggo.")
        
        #Room 5/Secret Room
        #add exits
        r5.addExit("west", r2)
        #add items
        r5.addItem("cat", "A cat sits in the center of the room, licking its paw...\nwhy do I hear boss music?\n\n")
        
        #Start game in Room 1 with nothing in inventory
        Game.currentRoom = r1
        Game.inventory = []
    
    #set up GUI - images, text box, input box
    def setupGUI(self):
        #organize GUI
        self.pack(fill = BOTH, expand = 1)
        #set up player input at bottom
        Game.player_input = Entry(self, bg = "white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side = BOTTOM, fill = X)
        Game.player_input.focus()
        #set up picture in left GUI
        img = None
        Game.image = Label(self, width = 400, image = img)
        Game.image.image = img
        Game.image.pack(side = LEFT, fill = Y)
        Game.image.pack_propagate(False)
        #set text to right in GUI
        text_frame = Frame(self, width = WIDTH // 2)
        #disabled by default
        Game.text = Text(text_frame, bg = "lightgrey", state = DISABLED)
        Game.text.pack(fill = Y, expand = 1)
        text_frame.pack(side = RIGHT, fill = Y)
        text_frame.pack_propagate(False)
    
    #set images on the left side of GUI
    def setRoomImage(self):
        global dogException, bookException, keyException, sixpackException
        #If player falls into the void - ending1
        if(Game.currentRoom == None):
            Game.img = PhotoImage(file = "imgs/void.gif")
        #if player reads the book
        elif(bookException):
            Game.img = PhotoImage(file = "imgs/book.gif")
            bookException = False
        #If player frees the dog
        elif(dogException):
            Game.img = PhotoImage(file = "imgs/pitbull.gif")
            dogException = False
        #If player collects the key
        elif(keyException):
            Game.img = PhotoImage(file = "imgs/key.gif")
            keyException = False
        #If player collects the six pack
        elif(sixpackException):
            Game.img = PhotoImage(file = "imgs/sixpack.gif")
            sixpackException = False
        #catthulu is displayed for ending 2 and at beginning of fight
        elif(bossFight or ending2):
            Game.img = PhotoImage(file = "imgs/cat.gif")
        
        elif(ending3):
            Game.img = PhotoImage(file = "imgs/dog.gif")
        #ending4 - player wins
        elif(ending4):
            Game.img = PhotoImage(file = "imgs/ending4.gif")
        #Default - displays image of room player is currently in
        else:
            Game.img = PhotoImage(file = Game.currentRoom.image)
        
        #display image
        Game.image.config(image = Game.img)
        Game.image.image = Game.img
    
    #set status displayed on right side GUI
    def setStatus(self, status):
        #enable, clear, set, and disable text widget
        Game.text.config(state = NORMAL, wrap = WORD)
        Game.text.delete("1.0", END)
        #if player falls into the void and dies
        if(Game.currentRoom == None):
            Game.text.insert(END, "You open the door to reveal an infinite void. Unable to resist its pull, you enter, falling out of the world.\n\nGAME OVER\nYou died.\n(Ending 1/4)\n")
            Game.text.insert(END, "The only thing you can do now is quit.\n")
        #Display final boss endings (2-4)
        elif(bossFight):
            #if player has the dog, tell to fight or run
            if(Game.hasDog()):
                Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(Game.inventory) + "\n\n" + status)
                Game.text.insert(END, "The cat stands, giving you a mischievous look.\nArching its back, it takes its final form of Cat-thulu!\nThe doggo growls, also transforming into its final form: Dogzilla!\nWhat do you do? (type \"run away\" or \"fight cat\")")
            #If player does not have dog, automatic loss - ending 2
            else:
                Game.text.insert(END, "The cat stands, giving you a mischievous look.\nArching its back, it takes its final form of Cat-thulu!\nAlmost before you can register what has happened, Cat-thulu has swiped its mighty paws and defeated you.\n\nGAME OVER\nYou died.\n(Ending 2/4)\n")
                Game.text.insert(END, "The only thing you can do now is quit.\n")
        #If player does not have dog, automatic loss - ending 2
        elif(ending2):
            Game.text.insert(END, "The cat stands, giving you a mischievous look.\nArching its back, it takes its final form of Cat-thulu!\nAlmost before you can register what has happened, Cat-thulu has swiped its mighty paws and defeated you.\n\nGAME OVER\nYou died.\n(Ending 2/4)\n")
            Game.text.insert(END, "The only thing you can do now is quit.\n")
        #If player has dog and stays to fight, loss - ending 3
        elif(ending3):
            Game.text.insert(END, "You try to help Dogzilla defeat Cat-thulu.\nDogzilla tries to protect you, but you are both defeated!\n\n\nGAME OVER\nYou died.\n(Ending 3/4)\n")
            Game.text.insert(END, "The only thing you can do now is quit.\n")
        #If player has dog and runs, true ending/win - ending 4
        elif(ending4):
            Game.text.insert(END, "You run to safety in another room.\nNot needing to worry about you, Dogzilla easily defeats Cat-thulu, clearing the way to the exit.\n\n\nYOU WIN!\nYou and doggo walk into the sunset and live happily ever after.\n(Ending 4/4)\n")
        
        #otherwise, display default status
        else:
            Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(Game.inventory) + "\n\n" + status)
        Game.text.config(state = DISABLED)
    
    #start game
    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")
        
    #process player input
    def process(self, event):
        global readBook, freeDog, bookException, dogException, keyException, sixpackException, bossFight, ending2, ending3, ending4
        #grab user input
        action = Game.player_input.get()
        action = action.lower()
        #default response
        response = "I don't understand. Try verb noun.\nValid verbs: go, look, take\nExample: \"go south\""
        if(action == "quit" or action == "exit" or action == "leave" or action == "bye" or action == "sionara!"):
            exit(0)
        
        #parse input for usable commands
        words = action.split()
        verb = ""
        noun = ""
        if(len(words) == 2):
            verb = words[0]
            noun = words[1]
        
        #If the player is able to read the book
        if(readBook and verb == "read"):
            bookException = True
            response = "The book tells you about a secret passage accessed through the east wall of Room 2."
            r2.addExit("east", r5)
            readBook = False
        
        #If the player is able to free the dog
        elif(freeDog and verb == "free"):
            dogException = True
            Game.inventory.remove("key")
            #add the dog in all rooms, as if it follows you around
            r4.replaceItem("kennel", "doggo", "wouf wouf") #Room 4

            r5.addItem("doggo", "Wouf wouf!")              #Room 5
            
            r3.addItem("doggo", "Wouf wouf!")              #Room 3

            r2.addItem("doggo", "Wouf wouf!")              #Room 2

            r1.addItem("doggo", "Wouf wouf!")              #Room 1
            
            Game.inventory.append("doggo")                      #Inventory
            
            response = "You free the doggo! He is so happy and follows you around.\n"
            freeDog = False
        
        #Check for the boss fight being enabled
        elif(bossFight):
            message = ""
            bossFight = False
            if(Game.hasDog()):
                if(verb == "run"):
                    ending4 = True
                elif(verb == "fight"):
                    ending3 = True
            else:
                ending2 = True
        
        #verb "go" implementation
        elif(verb == "go"):
            #default response
            response = "Invalid exit."
            #try to find exit, if found change room
            for i in range(len(Game.currentRoom.exits)):
                if(noun == Game.currentRoom.exits[i]):
                    Game.currentRoom = Game.currentRoom.exitLocations[i]
                    response = "Room changed."
                    break
        
        #verb "look" implementation
        elif(verb == "look"):
            #default response
            response = "I don't see that item."
            #try to find item, if found give description of item
            for i in range(len(Game.currentRoom.items)):
                if(noun == Game.currentRoom.items[i]):
                    response = Game.currentRoom.itemDescriptions[i]
                #Free dog from kennel
                if(Game.hasKey() and noun == "kennel"):
                    response = "Free the doggo? If so, type \"free dog\"."
                    freeDog = True
                #Dog defeats final boss cat
                if(noun == "cat"):
                    bossFight = True
                
        #verb "take" implementation
        elif(verb == "take"):
            #default response
            response = "I don't see that item."
            #Try to find grabbable, if found pick up
            for grabbable in Game.currentRoom.grabbables:
                if(noun == grabbable):
                    Game.inventory.append(grabbable)
                    Game.currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed."
                #Reading the book for access to a hidden room; show book picture
                if(noun == "book"):
                    response = "Read the book? If so, type \"read book\"."
                    readBook = True
                #show key picture
                if(noun == "key"):
                    keyException = True
                #show sixpack picture
                if(noun == "6-pack"):
                    sixpackException = True
                    
        #display image on left, text on right, and clear player input from bottom
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)
    
    #checks that the player has the key in their inventory
    def hasKey():
        for item in Game.inventory:
            if item == "key":
                return True
        return False
    
    #checks that the player has the dog in their inventory
    def hasDog():
        for item in Game.inventory:
            if item == "doggo":
                return True
        return False

#Room class
class Room:
    #constructor - name, exits, exitLocations, items, itemDescriptions, grabbables
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.exits = []
        self.exitLocations = []
        self.items = []
        self.itemDescriptions = []
        self.grabbables = []
    
    #getters
    #image getter
    @property
    def image(self):
        return self._image
    
    #name getter
    @property
    def name(self):
        return self._name
    
    #exits getter
    @property
    def exits(self):
        return self._exits
    
    #exitLocations getter
    @property
    def exitLocations(self):
        return self._exitLocations
    
    #items getter
    @property
    def items(self):
        return self._items
    
    #itemDescriptions getter
    @property
    def itemDescriptions(self):
        return self._itemDescriptions
    
    #grabbables getter
    @property
    def grabbables(self):
        return self._grabbables
    
    #setters
    #image setter
    @image.setter
    def image(self, new):
        self._image = new
    
    #name setter
    @name.setter
    def name(self, new):
        self._name = new
        
    
    #exits setter
    @exits.setter
    def exits(self, new):
        self._exits = new
    
    #exitLocations setter
    @exitLocations.setter
    def exitLocations(self, new):
        self._exitLocations = new
    
    #items setter
    @items.setter
    def items(self, new):
        self._items = new
    
    #itemDescriptions setter
    @itemDescriptions.setter
    def itemDescriptions(self, new):
        self._itemDescriptions = new
    
    #grabbables setter
    @grabbables.setter
    def grabbables(self, new):
        self._grabbables = new
    
    
    #method to add exit to a room
    def addExit(self, exit, room):
        self._exits.append(exit)
        self._exitLocations.append(room)
    
    #method to add item to a room
    def addItem(self, item, desc):
        self._items.append(item)
        self._itemDescriptions.append(desc)
        
    #method to remove item from a room and change it to something else
    def replaceItem(self, oldItem, newItem, desc):
        for i in range(len(self.items)):
            if(self.items[i] == oldItem):
                self._itemDescriptions[i] = desc
                self.items[i] = newItem
                break
    
    #method to add grabbable to a room
    def addGrabbable(self, item):
        self._grabbables.append(item)
    
    #method to remove grabbable from a room
    def delGrabbable(self, item):
        self._grabbables.remove(item)
    
    #string overload
    def __str__(self):
        #room name
        s = "You are in {}.\n".format(self.name)
        #items in room
        s += "You see: "
        for item in self.items:
            s += item + " "
        s += "\n"
        #exits from room
        s += "Exits: "
        for exit in self.exits:
            s += exit + " "
        #return full string
        return s

#Creates the basic window structure
def createWindow():
    window = Tk()
    window.title("Room Adventure")
    g = Game(window)
    g.play()
    window.mainloop()

#Defines all global variables that will be used throughout the game in order to
#show specific text and images during specific events
def defineInitials():
    global HEIGHT, WIDTH, readBook, freeDog, bookException, dogException, keyException, sixpackException, bossFight, ending2, ending3, ending4
    HEIGHT = 800
    WIDTH = 600
    readBook = False
    freeDog = False
    bookException = False
    dogException = False
    keyException = False
    sixpackException = False
    bossFight = False
    ending2 = False
    ending3 = False
    ending4 = False
#MAIN--------------------------------------------------------------------------------------------

defineInitials()
createWindow()