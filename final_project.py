class Room(object):
    def __init__(self, x, y, *args):
        self.x = x
        self.y = y
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
            print "That is not a valid direction"

    def print_room(self):
        print self.x, self.y
        return self.x, self.y

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y


class StartRoom(Room):
    def __init__(self, x, y, *args):
        super(StartRoom, self).__init__(x, y, *args)

    def print_room_text(self):
        print "This is the intro"


class Hallway(Room):
    def __init__(self, x, y, *args):
        super(Hallway, self).__init__(x, y, *args)

    def print_room_text(self):
        print "This is just a hallway, nothing here"


class Cave(Room):
    def __init__(self, x, y, *args):
        super(Cave, self).__init__(x, y, *args)

    def print_room_text(self):
        print "You are in a cave"


def room_execute(room):
    location = room
    location.reset()
    location.print_room_text()
    return location


def main():
    start_room = StartRoom(0, 0, 'n', 's', 'e', 'w')
    north_tile = Hallway(0, 1, 'n', 's')
    cave_tile = Cave(0, -1, 'n', 's')
    location = start_room
    location.print_room_text()

    while True:
        direction = raw_input("What direction do you want to go [n,w,s,e]? ").lower()
        location.move(direction)
        if location.print_room() == (0, 0):
            location = room_execute(start_room)
            # location = start_room
            # location.reset()
            # location.print_room_text()
        elif location.print_room() == (0, 1):
            location = north_tile
            location.reset()
            location.print_room_text()
        elif location.print_room() == (0, -1):
            location = cave_tile
            location.reset()
            location.print_room_text()

        location.print_room()


if __name__ == '__main__':
    main()
