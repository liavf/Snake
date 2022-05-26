
class Bomb:
    def __init__(self, location, radius, time):
        self.location = location
        self.radius = radius
        self.time = time
        self.shock_location = self.location
        self.is_shock = False
        self.shock_timer = 0

    def get_time(self):
        return self.time

    def update_timer(self):
        if self.time > 0:
            self.time -= 1
        else:
            self.shock_timer += 1
            self.is_shock = True

    def get_shock_couples(self):
        couples = []
        for i in range(self.shock_timer + 1):
            couples.append((i, self.shock_timer - i))
        return couples

    def get_shock_location(self):
        x, y = self.location
        coup_list = []
        for coup in self.get_shock_couples():
            first, second = coup
            a = (x + first, y + second)
            b = (x + first, y - second)
            c = (x - first, y + second)
            d = (x - first, y - second)
            for i in [a,b,c,d]:
                if i not in coup_list:
                    coup_list.append(i)
        return coup_list

    def finished(self):
        if self.shock_timer == self.radius:
            return True
        else:
            return False

    def get_location(self):
        if not self.is_shock:
            return [self.location]
        else:
            return self.get_shock_location()

    def get_is_shock(self):
        return self.is_shock