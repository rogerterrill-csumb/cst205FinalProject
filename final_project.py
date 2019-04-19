class Room(object):
    def __init__(self, x, y, *args):
        self.x = x
        self.y = y
        self.args = args

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


class StartRoom(Room):
    def __init__(self, x, y, *args):
        super(StartRoom, self).__init__(x, y, *args)

    def intro_text(self):
        print "This is the intro"


class Hallway(Room):
    def __init__(self, x, y):
        super(Hallway, self).__init__(x, y)

    def hallway_text(self):
        print "This is just a hallway, nothing here"


def main():
    location = StartRoom(0, 0, 'n', 's', 'e', 'w')
    location.intro_text()

    while True:
        direction = raw_input("What direction do you want to go [n,w,s,e]? ").lower()
        location.move(direction)
        if location.print_room() == (0, 0):
            location.intro_text()
        print type(location.print_room())


if __name__ == '__main__':
    main()
