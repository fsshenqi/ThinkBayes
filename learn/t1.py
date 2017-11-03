from bayescode.thinkbayes import Pmf



class Suite(Pmf):
    def __init__(self, hypos=tuple()):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
        self.Print()

    def Update(self, data):
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()
        print "=====  data:", data, " ====="
        self.Print()

    def Likelihood(self, data, hypo):
        return 1


class Cookie(Suite):
    mixs = {
        'Bowl 1': dict(vanilla=0.75, chocolate=0.25),
        'Bowl 2': dict(vanilla=0.5, chocolate=0.5)
    }

    def Likelihood(self, data, hypo):
        mix = self.mixs[hypo]
        like = mix[data]
        return like


class Monty(Suite):

    def Likelihood(self, data, hypo):

        if hypo == data:
            return 0
        elif hypo == "A":
            return 1.0 / 2
        else:
            return 1


class Monty2(Suite):
    def Likelihood(self, data, hypo):
        if hypo == data:
            return 0
        else:
            return 1.0 / 2

class Dice(Suite):
    def Likelihood(self, data, hypo):
        if data > hypo:
            return 0
        else:
            return 1.0 / hypo

if __name__ == '__main__':
    # cookie = Cookie(['Bowl 1', 'Bowl 2'])
    # for data in ['chocolate', 'chocolate', 'vanilla']:
    #     cookie.Update(data)
    #
    # monty = Monty2('ABC')
    # monty.Update('B')

    dice = Dice([4, 6, 8, 12, 20])
    dice.Update(6)
    dice.Update(2)
    dice.Update(13)