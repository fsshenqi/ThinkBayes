
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
            data = [int(float(nsAvg)*10), int(strengthGrade)]
            res.append(data)
        except ValueError:
            pass

    fp.close()
    return zip(*res)

class StrengthGrade(thinkbayes.Suite):
    def makeMap(self, dataset):
        dataMap = {}
        for data in dataset:
            oldValue = dataMap.get(data, 0)
            dataMap[data] = oldValue + 1
        self.dataMap = dataMap
        return dataMap

    def LogLikelihood(self, dataMap, hypo):
        return dataMap.get(hypo, 0)

class StrengthAvg(thinkbayes.Suite):
    pass


class Hypo(thinkbayes.Suite):

    def __init__(self, data):
        thinkbayes.Suite.__init__(self)
        self.data = data
        strengths = []
        for strength in data[1]:
            if not strength in strengths:
                strengths.append(strength)
        strengths.sort()
        hypos = strengths
        self.strengthGradePmf = self.makeStrengthGradePmf()
        self.likelihoodPdfs = self.makeStrengthAvgPdfs()
        for hypo in hypos:
            self.Set(hypo, self.strengthGradePmf.Prob(hypo))
        self.Normalize()


    def Likelihood(self, data, hypo):
        pdf = self.likelihoodPdfs[hypo]
        return pdf.Density(data)

    def makeStrengthGradePmf(self):
        nsavg = self.data[1]
        hypos = xrange(min(nsavg), int(max(nsavg)) + 1)
        pmf = StrengthGrade(hypos)
        dataMap = pmf.makeMap(nsavg)
        pmf.LogUpdate(dataMap)
        pmf.Normalize()
        return pmf

    def makeStrengthAvgPdfs(self):
        strengths = []
        for strength in self.data[1]:
            if not strength in strengths:
                strengths.append(strength)
        strengths.sort()

        rowData = zip(*self.data)
        hypoStrengthSet = {}
        for hypo in strengths:
            hypoStrengthSet[hypo] = []
        for row in rowData:
            hypo = row[1]
            avg = row[0]
            hypoStrengthSet[hypo].append(avg)

        pdfs = {}
        for hypo in strengths:
            s = thinkbayes.EstimatedPdf(hypoStrengthSet[hypo])
            pdfs[hypo] = s

        return pdfs


def main():
    data = ReadData()
    hypo = Hypo(data)
    for data in [
        43.7,
        43.3,
        43.4,
        42.5,
        42.2,
        43.4,
        42.6,
        43.9,

    ]:
        hypo.Update(data*10)
        hypo.Print()
        print data, "="*10

if __name__ == '__main__':
    main()
