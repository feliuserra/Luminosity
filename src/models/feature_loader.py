import os

DEF_SRC_PATH = '../data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
START_YEAR = 1992


class LaggedFeatureNotFound(Exception):
    def __init___(self, target):
        Exception.__init__(self,
                           "Couldn't find all the features for target {}"
                           .format(target))
        self.target = target


class FeatureTensorLoader(object):

    def __init__(self, lags=3, batch_size=1,
                 SRC_PATH=DEF_SRC_PATH):
        files = [f for f
                 in os.listdir(SRC_PATH)
                 if 'sections' not in f]
        self.targets = [f for f in files
                        if int(f[:4]) > START_YEAR + lags]
        self.features = []
        for t in self.targets:
            for l in range(lags):
                found = os.path.exists(
                    SRC_PATH + str(int(t[:4]) - l) + t[4:])
                if not found:
                    raise LaggedFeatureNotFound(t)

    # def load(self, offset):
    #     target = self.targets[offset]

