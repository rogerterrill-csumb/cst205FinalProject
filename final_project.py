__author__ = "Roger Terrill, Abby Packham, Carlos Orduna"
__copyright__ = "Copyright 2019, CST205"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "rchicasterrill@csumb.edu, apackham@csumb.edu, cordunacorrales@csumb.edu  "
__status__ = "Production"


def sound(sound_file):
    sound = makeSound(sound_file)
    targetIndex = 0
    clip = makeEmptySound(15340)
    for ii in range(0, 15340):
        x = getSampleValueAt(sound, ii)
        setSampleValueAt(clip, targetIndex, x)
        targetIndex = targetIndex + 1
    max = maxVolume(clip)
    play(clip)


def maxSample(sound):
    max_val = 0
    for sample in getSamples(sound):
        max_val = max(max_val, getSampleValue(sample))
    return max_val


def maxVolume(sound):
    largest = maxSample(sound)
    maxPossibleSampleValue = 32767.0
    factor = float(maxPossibleSampleValue) / largest
    for sample in getSamples(sound):
        value = getSampleValue(sample)
        setSampleValue(sample, value * factor)
    return sample


def resize(pic):
    width = getWidth(pic)
    height = getHeight(pic)
    target = makeEmptyPicture(1000, 1000)
    percentWidth = width / 1000.0
    percentHeight = height / 1000.0
    for x in range(0, 999):
        for y in range(0, 999):
            color = getColor(getPixel(pic, int(x * percentWidth), int(y * percentHeight)))
            setColor(getPixel(target, x, y), color)
    return target


def win_image(image_file):
    pic = makePicture(image_file)
    pic = resize(pic)
    pixels = getPixels(pic)
    for p in pixels:
        newColor = makeColor(getRed(p) + 50, getGreen(p) + 50, getBlue(p) + 50)
        setColor(p, newColor)

    phrase = "You win!"
    import java.awt.Font as Font
    myFont = makeStyle("Comic Sans", Font.BOLD, 80)
    addTextWithStyle(pic, 350, 500, phrase, myFont, black)
    repaint(pic)


def lose_image(image_file):
    pic = makePicture(image_file)
    pic = resize(pic)
    pixels = getPixels(pic)
    for p in pixels:
        avg_color = avg_color = (getRed(p) * .299 + getGreen(p) * .587 + getBlue(p) * .114)
        newColor = makeColor(avg_color, avg_color, avg_color)
        setColor(p, newColor)

    phrase = "You lose."
    import java.awt.Font as Font
    myFont = makeStyle("Comic Sans", Font.BOLD, 80)
    addTextWithStyle(pic, 350, 500, phrase, myFont, red)
    repaint(pic)


def win():
    setMediaPath()
    win_image = getMediaPath() + 'win.jpg'
    lose_image = getMediaPath() + 'lose.jpg'
    win_sound = getMediaPath() + 'win.wav'
    lose_sound = getMediaPath() + 'lose.wav'


class Player:
    def __init__(self, moves, resources):
        self.moves = moves
        self.resources = resources

    def print_stats(self):
        print "*********************************************************"
        print "[You have " + str(self.moves) + " moves left]"
        print "[You have the following resources " + str(self.resources)
        print "*********************************************************"


class Tile(object):
    def __init__(self, x, y, player, *args):
        self.x = x
        self.y = y
        self.player = player
        self.args = args
        self.initial_x = x
        self.initial_y = y

    def move(self, direction):
        if direction in self.args:
            if direction == 'n':
                self.y += 1
            elif direction == 'e':
                self.x += 1
            elif direction == 's':
                self.y -= 1
            elif direction == 'w':
                self.x -= 1
        else:
            print "You can't go that way"

    def print_room(self):
        # print self.x, self.y
        return self.x, self.y

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y


def welcome():
    print "-It is the distant future, a year after pigs took over the world.-"
    print "They have taken over the surface of Earth after they rebelled against the human race. " \
          "We were powerless against the hog leaders."
    print "The disenfranchise masses had to escape. Some found shelter on tropical island, away from the main " \
          "invasions."
    print "We found shelter on a new technological advancement, free floating sky islands that kept us away from " \
          "the pink menace."
    print "But a troubling message came in during my shift at the Onlook tower."
    print "Careful, any wasted movement will lose you some time!"


class TowerStart(Tile):
    def __init__(self, x, y, player, *args):
        super(TowerStart, self).__init__(x, y, player, *args)

    def print_room_text(self):

        # Onlook Tower Start
        print ".--. .. --. ... / -.-. .- -. / ..-. .-.. -.-- .-.-.-"
        print "'The day is today. Pigs can fly. USAF planes piloted by pigs attacked us and you are next.'\n"
        print "The morse code coming in shakes you out of your chair"
        print "It comes from the island 30 miles from yours giving you sometime to notify the Comander, Citadel " \
              "and people of the message."
        print "...Unless this is just a cruel joke from the other island"
        print "Let's head over East towards the Barracks, Citadel and Suburbs to notify the others of the message"
        print "ONCE YOU HAVE ALL THE RESOURCES, RETURN HOME TO THE TOWER!!! HURRY!"

        if 'Radar' in self.player.resources:
            print "Bill install the radar to the tower's system and you see 4 Unknown Flying Objects coming from the West"
            print "The UFO's should be enough proof for the Comander.\n"
        elif 'Radar' in self.player.resources and 'Proof' in self.player.resources:
            print "Let's alert everyone that pigs are flying!\n"
        else:
            print "Trying to get in contact with the other island is fruitless"
            print "Your messages aren't responded.\n"

        print "you can only go 'e'-East towards the Barracks\n\n"

    def take_resource(self):
        if 'Proof' not in self.player.resources:
            print "When you showed the picture of the UFO's, the Comander shouted at everybody to get in the artillery to protect the island"
            print "We should be closer in defending the island.\n"
            self.player.resources.append('Proof')
        else:
            print "The Comander is waiting impatiently for any means to prove the message.\n"


    def win(self):
        if 'Radar' in self.player.resources and 'Wyvern' in self.player.resources and 'People Safe' in self.player.resources:
            print "**********-You Win!-**********"
            print "The artillery shoots at the planes before the pigs get in enough range."
            print "The Mayor's Wyvern takes flight and clips off a couple pigs from the sky."
            print "The remaining pigs fire at the suburbs but their shots land on the barren districts."
            print "Nobody was damaged and the remaining flyings pigs are taken care of.\n\n"
            print "However you thought you'd never see the day pigs fly... It is time we take our planet away from them!"
            print "You have won today!"
            return 'win'
        else:
            print "\nYou are missing resources!!!!!!!! Hurry!!!!"


class Barracks(Tile):
    def __init__(self, x, y, player, *args):
        super(Barracks, self).__init__(x, y, player, *args)

    def print_room_text(self):
        print "**********-Barracks-**********"
        print "You approach the Commander and give him the news..."
        print "He looks at you with disbelief, afterall you are telling him that pigs can fly."
        print "He mentions he needs proof before he allows you to get the defenses loaded. You should look for " \
              "a means to locate were they are coming from.\n"

        print "-Go 'n' to the Artillery"
        print "-Go 'e' to the Citadel"
        print "-Go 'w' to the Onlook tower"
        print "-Go 's' to the Lab\n\n"

class Artillery(Tile):
    def __init__(self, x, y, *args):
        super(Artillery, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Artillery-**********"
        print "The mighty Cannons that protect your island stand here. But nobody is manning them. You can't " \
              "defend the island alone.\n"

        if 'Proof' in self.player.resources:
            print "Your brothers in arms stand in wait to attack the flying pigs once they get in range!\n"

        print "-Go 's' to the Barracks"
        print "-Go 'e' to the Suburbs\n\n"

    def take_resource(self):
        if 'Artillery Manned' not in self.player.resources:
            print "You have received the Artillery Manned"
            self.player.resources.append('Artillery Manned')
        else:
            print "Already been here and taken the Artillery Manned"
            print "Let's hurry before it is too late!\n"

class Laboratory(Tile):
    def __init__(self, x, y, *args):
        super(Laboratory, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Laboratory-**********"
        print "The Laboratory is where all the new technology is created. If we bring a scientist with us we could " \
              "look for an upgrade for our Tower.\n"

        if 'Scientist' in self.player.resources:
            print "Bill works at the Laboratory and unlocks the gate."
            print "He grabs the new Radar prototype he was working on for your Tower, this should give you enough proof if pigs are really coming!\n"
        print "-Go 'n' to the Barracks\n\n"

    def take_resource(self):
        if 'Radar' not in self.player.resources:
            print "You have received the radar"
            self.player.resources.append('Radar')
        else:
            print "Already been here and taken the radar"
            print "Let's hurry before it is too late!\n"

class Citadel(Tile):
    def __init__(self, x, y, *args):
        super(Citadel, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Citadel-**********"
        print "You approach the Mayor to tell him about the incoming flying pigs..."
        print "Luckily he believes every word you say and claims he has been saying it since the beginning, that one day pigs will fly!"
        print "Unfortunately he is very busy documenting the taxes that the population owe him and tells you it's up to you to collect his pet frogs at the lake with a bug net."
        print "...you begin to question the Mayor's leadership.\n"

        if 'Frogs' in self.player.resources:
            print "The Mayor thanks you and throws the frogs into an open hole in the corner of the room."
            print "From the window you see a wyvern emerge from the side of the Citadel and see it go towards the Onlook Tower."
            print "Maybe the Mayor is on this position for a reason...\n"
        elif 'Wyvern' in self.player.resources:
            print "The Mayor has released a Wyvern to defend the island. But other's should be warned\n"
        else:
            print "The Mayor just shooshs you away telling you to collect his pet frogs from the lake.\n"

        print "-Go 'n' to the Suburbs"
        print "-Go 'e' to the Sanctuary"
        print "-Go 'w' to the Barracks\n\n"

    def take_resource(self):
        if 'Frog Net' not in self.player.resources:
            print "You have received the Frog Net"
            self.player.resources.append('Frog Net')
        else:
            print "Already been here and taken the radar"

    def take_wyvern(self):
        if 'Wyvern' not in self.player.resources:
            print "You have received the Wyvern"
            self.player.resources.append('Wyvern')
        else:
            print "Already been here and taken the Wyvern"

class Suburbs(Tile):
    def __init__(self, x, y, *args):
        super(Suburbs, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Suburbs-**********"
        print "You try to get the attention of people walking around but they don't seem to believe your tale of flying pigs."
        print "Fortunately you recognize Bill, your scientist buddy who decides to join your party after hearing your plea."
        print "Bill can rally his friends to make everyone flee, now you need to find a place for everyone to shelter in.\n"

        if 'Scientist' in self.player.resources:
            print "We should find somewhere where people can find shelter!\n"
        if 'People Safe' in self.player.resources:
            print "We need to warn the others of the danger coming in, we don't have much time!\n"

        print "-Go 'e' to the Suburbs"
        print "-Go 'w' to the Sanctuary\n\n"

    def take_resource(self):
        if 'Scientist' not in self.player.resources:
            print "You have received the Scientist"
            self.player.resources.append('Scientist')
        else:
            print "Already been here and taken the Scientist"



class Lake(Tile):
    def __init__(self, x, y, *args):
        super(Lake, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Lake-**********"
        print "A lake in the corner of your island and the source of fresh water. Not much for us to do here.\n"

        if 'Frog Net' in self.player.resources:
            print "You spend some time but capture all the frogs, you wonder if this is a good use of your time.\n"
        if 'Frogs' in self.player.resources:
            print "Let's hurry and alert everyone before it is too late!\n"

        print "-Go 'w' to the Suburbs"
        print "-Go 's' to the Sanctuary\n\n"

    def take_resource(self):
        if 'Frogs' not in self.player.resources:
            print "You have received the Frogs"
            self.player.resources.append('Frogs')
        else:
            print "Already been here and taken the Frogs"


class Sanctuary(Tile):
    def __init__(self, x, y, *args):
        super(Sanctuary, self).__init__(x, y, *args)

    def print_room_text(self):
        print "**********-Sanctuary-**********"
        print "The door is shut but a priestess can be seen by the window."
        print "You get her attention and tell her that you need a place for everyone to hide while the flying pigs are taken care of."
        print "She, reluctantly, hears your story and tells you she will shelter everyone down at the catacombs."
        print "Now we just need to alert the people to come take shelter.\n"

        print "-Go 'w' to the Citadel\n\n"

    def take_resource(self):
        if 'People Safe' not in self.player.resources:
            print "You have received the People Safe"
            self.player.resources.append('People Safe')
        else:
            print "Already been here and taken the People Safe"


def room_execute(room, player):
    location = room
    location.reset()
    location.print_room_text()
    player.moves -= 1
    return location


def main():
    setMediaPath()
    win_image_file = getMediaPath() + 'win.jpg'
    lose_image_file = getMediaPath() + 'lose.jpg'
    win_sound_file = getMediaPath() + 'win.wav'
    lose_sound_file = getMediaPath() + 'lose.wav'

    init_move = 20
    resources = []
    direction = ''
    player_1 = Player(init_move, resources)
    onlook_tower_start = TowerStart(0, 1, player_1, 'e')
    barracks = Barracks(1, 1, player_1, 'n', 'e', 'w', 's')
    artillery = Artillery(1, 2, player_1, 's', 'e')
    laboratory = Laboratory(1, 0, player_1, 'n')
    citadel = Citadel(2, 1, player_1, 'n', 'e', 'w')
    suburbs = Suburbs(2, 2, player_1, 'e', 'w', 's')
    lake = Lake(3, 2, player_1, 's', 'w')
    sanctuary = Sanctuary(3, 1, player_1, 'w', 'n')

    welcome()

    location = onlook_tower_start
    location.print_room_text()

    while direction != 'win' and direction != 'quit' and player_1.moves > 0:
        player_1.print_stats()
        direction = raw_input("What direction do you want to go [n,w,s,e]? ").lower()
        location.move(direction)
        if location.print_room() == (0, 1):
            location = room_execute(onlook_tower_start, player_1)
            if 'Radar' in player_1.resources:
                location.take_resource()
            direction = location.win()
        elif location.print_room() == (1, 1):
            location = room_execute(barracks, player_1)
        elif location.print_room() == (1, 2):
            location = room_execute(artillery, player_1)
            if 'Proof' in player_1.resources:
                location.take_resource()
        elif location.print_room() == (1, 0):
            location = room_execute(laboratory, player_1)
            if 'Scientist' in player_1.resources:
                location.take_resource()
        elif location.print_room() == (2, 1):
            location = room_execute(citadel, player_1)
            location.take_resource()
            if 'Frogs' in player_1.resources:
                location.take_wyvern()
        elif location.print_room() == (2, 2):
            location = room_execute(suburbs, player_1)
            location.take_resource()
        elif location.print_room() == (3, 2):
            location = room_execute(lake, player_1)
            if 'Frog Net' in player_1.resources:
                location.take_resource()
        elif location.print_room() == (3, 1):
            location = room_execute(sanctuary, player_1)
            location.take_resource()

    if direction == 'lose':
        print "**********-You Lose-**********"
        print "It's too late... You thought you'd never see the day but, the day pigs fly is here and nobody believed you."
        print "You brace yourself as the pink menace opens fire to the island..."
