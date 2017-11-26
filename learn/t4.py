from bayescode.thinkbayes import Suite

class Euro(Suite):

    def Likelihood(self, data, hypo):
        if data == 'H':
            return hypo / 100.0
        else:
            return 1- hypo / 100.0


if __name__ == "__main__":
    euro = Euro(xrange(0, 101))
    for data in 'H' * 140 + 'F' * 110:
        euro.Update(data)
    print euro.MaximumLikelihood()
    print euro.Prob(euro.MaximumLikelihood())
