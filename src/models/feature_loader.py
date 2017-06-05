import os
import numpy as np

DEF_SRC_PATH = 'data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
START_YEAR = 1992
END_YEAR = 2000


class LaggedFeatureNotFound(Exception):
    def __init___(self, target):
        Exception.__init__(self,
                           "Couldn't find all the features for target {}"
                           .format(target))
        self.target = target


class FeatureTensorLoader(object):

    def __init__(self, lags=3, batch_size=100,
                 check_integrity=True, cv=False,
                 SRC_PATH=DEF_SRC_PATH):
        self.lags = lags
        self.batch_size = batch_size
        self.cv = cv
        self.src = SRC_PATH
        files = [f for f
                 in os.listdir(self.src)
                 if 'sections' not in f]
        self.target_files = [f for f in files
                             if int(f[:4]) > START_YEAR + lags
                             and int(f[:4]) < END_YEAR]
        self.features = []
        if check_integrity is True:
            for t in self.target_files:
                for l in range(lags):
                    found = os.path.exists(
                        self.src + str(int(t[:4]) - l) + t[4:])
                    if not found:
                        raise LaggedFeatureNotFound(t)

    def load(self, offset):
        target_file = self.target_files[offset]
        target = np.load(self.src + target_file)['arr_0']
        feature = []
        for l in range(self.lags):
            lagged_feature = np.load(
                self.src + str(int(target_file[:4]) - l) +
                target_file[4:])['arr_0']
            feature.append(lagged_feature)

        feature = np.stack(feature)
        return feature, target

    def load_batch(self, batch):
        features = []
        targets = []
        for i in range(batch * self.batch_size,
                       (batch + 1) * self.batch_size):
            feature, target = self.load(i)
            features.append(feature)
            targets.append(target)

        return features, targets
