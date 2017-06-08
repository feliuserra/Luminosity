import os
import numpy as np
import random as rd

DEF_SRC_PATH = 'data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
START_YEAR = 1992
END_YEAR = 2010


class LaggedFeatureNotFound(Exception):
    def __init___(self, target_file):
        super().__init__(
            self,
            "Couldn't find all the features for target file {}"
            .format(target_file))


class WrongImageSize(Exception):
    def __init___(self, target_file):
        super().__init__(
            self,
            "Some file had the wrong dimensions for target file {}"
            .format(target_file))


class LaggedFeatureLoader(object):

    def __init__(self, lags=3, batch_size=100,
                 check_integrity=True, cv=False,
                 img_shape=(300, 300), shuffle=True,
                 SRC_PATH=DEF_SRC_PATH):
        self.lags = lags
        self.batch_size = batch_size
        self.img_shape = img_shape
        self.cv = cv
        self.src = SRC_PATH
        files = [f for f
                 in os.listdir(self.src)
                 if 'sections' not in f]
        self.target_files = [f for f in files
                             if int(f[:4]) > START_YEAR + lags
                             and int(f[:4]) < END_YEAR]
        if shuffle is True:
            rd.shuffle(self.target_files)
        self.features = []
        if check_integrity is True:
            for t in self.target_files:
                for l in range(lags):
                    found = os.path.exists(
                        self.src + str(int(t[:4]) - l) + t[4:])
                    if not found:
                        raise LaggedFeatureNotFound(t)

        print('Feature loader initialized with {} observations'
              .format(len(self.target_files)))

    def load(self, offset=None):
        if offset is None:
            offset = np.random.randint(0, len(self.target_files))
        target_file = self.target_files[offset]
        target = np.load(self.src + target_file)['arr_0']
        feature = []
        for l in range(self.lags):
            lagged_feature = np.load(
                self.src + str(int(target_file[:4]) - l) +
                target_file[4:])['arr_0']
            feature.append(lagged_feature)

        feature = np.stack(feature, axis=2)
        try:
            self.assess_size(feature, target, target_file)
        except WrongImageSize as e:
            print(e)
            feature, target = self.load(offset=offset+1)  # >゜)))><
            pass
        return feature, target

    def load_batch(self, batch=None):
        features = []
        targets = []
        if batch is None:
            batch = np.random.randint(
                0, len(self.target_files) / self.batch_size)
        for i in range(batch * self.batch_size,
                       (batch + 1) * self.batch_size):
            feature, target = self.load(i)
            features.append(feature)
            targets.append(target)

        features = np.stack(features)
        targets = np.stack(targets)
        return features, targets

    def batch_iterator(self):
        counter = 0
        while counter < len(self.target_files):
            counter += 1
            yield self.load_batch(counter)

    def batch_x_iterator(self):
        counter = 0
        while counter < len(self.target_files):
            counter += 1
            yield self.load_batch(counter)[0]

    def batch_y_iterator(self):
        counter = 0
        while counter < len(self.target_files):
            counter += 1
            yield self.load_batch(counter)[1]

    def assess_size(self, features, target, target_file):
        if not features.shape == (self.img_shape[0],
                                  self.img_shape[1],
                                  self.lags):
            raise WrongImageSize(target_file)
        if not target.shape == (self.img_shape):
            raise WrongImageSize(target_file)
