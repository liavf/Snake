
class Bomb:
    def __init__(self, x, y, radius, time, shock_time):
        self.location = (x, y)
        self.radius = radius
        self.time = time
        self.shock_location = self.location

    def get_time(self):
        return self.time

    def update_time(self):
        self.time -= 1

    def reg_turn(self):
        self.update_time()
        return self.location, RED

    def shock_turn(self):
        self.update_shock_time()
        loc = self.get_shock_location()
        return loc, ORANGE

    def update_shock_time(self):
        self.radius -= 1

    def get_shock_couples(self):
        couples = []
        for i in self.radius:
            couples.append((i, self.radius - i))
        return couples

    def get_shock_location(self):
        x, y = self.location
        coup_list = []
        for coup in self.get_shock_couples():
            first, second = coup
            a = (x + first, y)
            b = (x - first, y)
            c = (x, y + second)
            d = (x, y - second)
            for i in [a,b,c,d]:
                if i not in coup_list:
                    coup_list.append(i)
        return coup_list

    def do_turn(self):
        if self.time >= 0:
            return self.reg_turn()
        else:
            return self.shock_turn()


