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
  factor=float(maxPossibleSampleValue)/largest
  for sample in getSamples(sound):
    value = getSampleValue(sample)
    setSampleValue(sample, value*factor)
  return sample
  
def resize(pic):
  width = getWidth(pic)
  height = getHeight(pic)
  target = makeEmptyPicture(1000,1000)
  percentWidth = width / 1000.0 
  percentHeight = height / 1000.0
  for x in range(0,999):
    for y in range(0,999):
      color = getColor(getPixel(pic,int(x*percentWidth),int(y*percentHeight))) 
      setColor(getPixel(target, x, y),color)
  return target

def win_image(image_file):
  pic = makePicture(image_file)
  pic = resize(pic)
  pixels = getPixels(pic)
  for p in pixels:
    newColor = makeColor(getRed(p)+50, getGreen(p)+50, getBlue(p)+50)
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
    avg_color = avg_color = (getRed(p)*.299 + getGreen(p)*.587 + getBlue(p)*.114)
    newColor = makeColor(avg_color,avg_color,avg_color)
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
    def __init__(self, health, weapons):
        self.health = health
        self.weapons = weapons

    def print_stats(self):
        print self.health
        print self.weapons


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


class Hallway(Tile):
    def __init__(self, x, y, player, *args):
        super(Hallway, self).__init__(x, y, player, *args)

    def increase_health(self, amount):
        self.player.health += amount

    def take_weapon(self):
        if 'Axe' not in self.player.weapons:
            self.player.weapons.append('Axe')
        else:
            print "Already been here and taken the axe"

    def print_room_text(self):
        print "***This is just a hallway, nothing here***\n"


class Cave(Tile):
    def __init__(self, x, y, *args):
        super(Cave, self).__init__(x, y, *args)

    def print_room_text(self):
        print "***You are in a cave***\n"


class OgreRoom(Tile):
    def __init__(self, x, y, *args):
        super(OgreRoom, self).__init__(x, y, *args)

    def print_room_text(self):
        print "***You are in the ogre room***\n"


class SecretRoom(Tile):
    def __init__(self, x, y, *args):
        super(SecretRoom, self).__init__(x, y, *args)

    def print_room_text(self):
        print "***You are in the secret room***\n"


def room_execute(room):
    location = room
    location.reset()
    location.print_room_text()
    return location

def welcome():
    print "-It is the distant future, a year after pigs took over the world.-"
    print "They have taken over the surface of Earth after they rebelled against the human race. " \
          "We were powerless against the hog leaders."
    print "The disenfranchise masses had to escape. Some found shelter on tropical island, away from the main " \
          "invasions."
    print "We found shelter on a new technological advancement, free floating sky islands that kept us away from " \
          "the pink menace."
    print "But a troubling message came in during my shifft at the Onlook tower."


def main():
    setMediaPath()
    win_image_file = getMediaPath() + 'win.jpg'
    lose_image_file = getMediaPath() + 'lose.jpg'
    win_sound_file = getMediaPath() + 'win.wav'
    lose_sound_file = getMediaPath() + 'lose.wav'

    init_health = 50
    weapons = []
    direction = ''
    player_1 = Player(init_health, weapons)
    start_room = TowerStart(0, 0, player_1, 'n', 's', 'e', 'w')
    hallway_tile_1 = Hallway(0, 1, player_1, 's')
    cave_tile = Cave(0, -1, 'n')
    ogre_tile = OgreRoom(0, -1, 'e')
    secret_tile = SecretRoom(1, 0, 'w')

    welcome()

    location = start_room
    location.print_room_text()

    while direction != 'quit':
        player_1.print_stats()
        direction = raw_input("What direction do you want to go [n,w,s,e]? ").lower()
        location.move(direction)
        if location.print_room() == (0, 0):
            location = room_execute(start_room)
        elif location.print_room() == (0, 1):
            location = room_execute(hallway_tile_1)
            location.take_weapon()
            #win_image(win_image_file)
            sound(win_sound_file)
            direction = 'quit'
        elif location.print_room() == (0, -1):
            location = room_execute(cave_tile)
        elif location.print_room() == (-1, 0):
            location = room_execute(ogre_tile)
        elif location.print_room() == (1, 0):
            location = room_execute(secret_tile)


if __name__ == '__main__':
    main()
