class Player:
    def __init__(self, name, health, weapons):
        self.name = name
        self.health = health
        self.weapons = weapons

    def print_stats(self):
        print self.health
        print self.weapons


class Room(object):
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


class StartRoom(Room):
    def __init__(self, x, y, player, *args):
        super(StartRoom, self).__init__(x, y, player, *args)

    def print_room_text(self):
        print "***This is the starting point***\n"


class Hallway(Room):
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


class Cave(Room):
    def __init__(self, x, y, *args):
        super(Cave, self).__init__(x, y, *args)

    def print_room_text(self):
        print "***You are in a cave***\n"


class OgreRoom(Room):
    def __init__(self, x, y, *args):
        super(OgreRoom, self).__init__(x, y, *args)

    def print_room_text(self):
        print "***You are in the ogre room***\n"


class SecretRoom(Room):
    def __init__(self, x, y, *args):
        super(SecretRoom, self).__init__(x, y, *args)



    def print_room_text(self):
        print "***You are in the secret room***\n"


def room_execute(room):
    location = room
    location.reset()
    location.print_room_text()
    return location


def main():
    name = raw_input("What is your name? ")
    init_health = 50
    weapons = []
    direction = ''
    player_1 = Player(name, init_health, weapons)
    start_room = StartRoom(0, 0, player_1, 'n', 's', 'e', 'w')
    hallway_tile_1 = Hallway(0, 1, player_1, 's')
    cave_tile = Cave(0, -1, 'n')
    ogre_tile = OgreRoom(0, -1, 'e')
    secret_tile = SecretRoom(1, 0, 'w')

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
        elif location.print_room() == (0, -1):
            location = room_execute(cave_tile)
        elif location.print_room() == (-1, 0):
            location = room_execute(ogre_tile)
        elif location.print_room() == (1, 0):
            location = room_execute(secret_tile)


if __name__ == '__main__':
    main()
