
import csv
import numpy
from bayescode import thinkbayes


def ReadData(filename='016a.csv'):
    """Reads a CSV file of data.

    Args:
      filename: string filename

    Returns: sequence of (price1 price2 bid1 bid2 diff1 diff2) tuples
    """
    fp = open(filename)
    reader = csv.reader(fp)
    res = []

    for t in reader:
        reportno_in = t[0]
        nsAvg = t[1]
        strengthGrade = (t[3] + '').replace('C', '')
        try:
            data = [int(float(nsAvg)*10), strengthGrade]
            res.append(data)
        except ValueError:
            pass

    fp.close()
    return zip(*res)

class NSAvg(thinkbayes.Suite):
    def makeMap(self, dataset):
        dataMap = {}
        for data in dataset:
            oldValue = dataMap.get(data, 0)
            dataMap[data] = oldValue + 1
        self.dataMap = dataMap
        return dataMap

    def LogLikelihood(self, dataMap, hypo):
        return dataMap.get(hypo, 0)

class StrengthGrade(thinkbayes.Suite):
    def LogLikelihood(self, data, hypo):
        if data == hypo:
            return 1
        return 0

def makeStrengthPmfs(data):
    nsavg = data[0]
    hypos = xrange(min(nsavg), int(max(nsavg))+1)
    strengths = []
    for strength in data[1]:
        if not strength in strengths:
            strengths.append(strength)
    strengths.sort()
    rowData = zip(*data)
    print rowData[:10]
    hypoStrengthSet = []
    for i in xrange(0, max(hypos)+1):
        hypoStrengthSet.append([])
    for row in rowData:
        hypo = row[0]
        strength = row[1]
        hypoStrengthSet[hypo].append(strength)

    pmfs = []
    for hypo in range(len(hypoStrengthSet)):
        s = StrengthGrade(strengths)
        s.LogUpdateSet(hypoStrengthSet[hypo])
        s.Normalize()
        pmfs.append(s)

    return pmfs

def makeAvgPmf(data):
    nsavg = data[0]
    hypos = xrange(min(nsavg), int(max(nsavg))+1)
    avg = NSAvg(hypos)
    dataMap = avg.makeMap(nsavg)
    avg.LogUpdate(dataMap)
    avg.Normalize()
    return avg

class AvgStrength(thinkbayes.Suite):
    def __init__(self, data):
        self.avgPmf = makeAvgPmf(data)
        self.strengthPmfs = makeStrengthPmfs(data)
        thinkbayes.Suite.__init__(self)
        nsavg = data[0]

        hypos = xrange(min(nsavg), int(max(nsavg)) + 1)
        for hypo in hypos:
            self.Set(hypo, self.avgPmf.Prob(hypo))
        self.Normalize()

    def Likelihood(self, data, hypo):
        return self.strengthPmfs[hypo].Prob(data)
        return 1

def main():
    data = ReadData()
    avg = AvgStrength(data)
    avg.Update('30')
    avg.Print()


if __name__ == '__main__':
    main()
