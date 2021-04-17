import os

import cv2
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path

np.set_printoptions(precision=3)


class ImageryProc:
    """
    Image Processing Class
    """

    def __init__(self, file, cache, std=True, use_cache=True):
        self.file = file
        self.cache = cache
        self.n_bands = 4
        self.img_shape = None
        self.std = std
        self.img = None
        self.feature_matrix = None
        self.cov = None
        self.PC = None
        self.use_cached = use_cache
        self.PC_2d = None
        self.eigenval, self.eigenvec = None, None
        self.bandnames = ['Band 1', 'Band 2', 'Band 3', 'Band 4']
        if self.load_cached():
            self.img_shape = self.img.shape[:2]
            print("Read to Imagery Completed")
        else:
            print("Unable to read the imagery file.")

    def get_data(self):
        """
        Returns image data
        :return: Numpy [, , 4]
        """
        return self.img

    def get_cached(self):
        """
        Get cache path
        :return: Str
        """
        return self.cache

    def init_pca(self):
        self.feature_matrix = np.zeros((self.img[:, :, 0].size, self.n_bands))

        for i in range(self.n_bands):
            feature_array = self.img[:, :, i].flatten()  # covert 2d to 1d array
            if self.std:
                feature_array_std = (feature_array - feature_array.mean()) / feature_array.std()
                self.feature_matrix[:, i] = feature_array_std
            else:
                self.feature_matrix[:, i] = feature_array

    def pca(self):
        self.cov = np.cov(self.feature_matrix.transpose())
        # Eigen Values
        self.eigenval, self.eigenvec = np.linalg.eig(self.cov)
        order = self.eigenval.argsort()[::-1]
        self.eigenval = self.eigenval[order]
        self.eigenvec = self.eigenvec[:, order]
        # Projecting data on Eigen vector directions resulting to Principal Components
        self.PC = np.matmul(self.feature_matrix, self.eigenvec)  # cross product

    def pca_viz(self):
        self.PC_2d = np.zeros((self.img_shape[0], self.img_shape[1], self.n_bands))
        for i in range(self.n_bands):
            self.PC_2d[:, :, i] = self.PC[:, i].reshape(-1, self.img_shape[1])

        PC_2d_Norm = np.zeros((self.img_shape[0], self.img_shape[1], self.n_bands))
        for i in range(self.n_bands):
            PC_2d_Norm[:, :, i] = cv2.normalize(self.PC_2d[:, :, i],
                                                np.zeros(self.img_shape), 0, 255, cv2.NORM_MINMAX)
            plt.imsave(os.path.join(self.cache, "pcs/", "pc_" + str(i) + ".png"), PC_2d_Norm[:, :, i])

        self.PC_2d = PC_2d_Norm

    def analyse(self):
        if self.use_cached:
            covar_path = Path(os.path.join(self.cache, "covar.png"))
            if not covar_path.exists():
                a = sns.pairplot(pd.DataFrame(self.feature_matrix,
                                              columns=self.bandnames),
                                 diag_kind='kde', plot_kws={"s": 3})
                a.fig.suptitle("Pair plot of Band images")
                a.savefig(covar_path.as_posix())

            pc_path = Path(os.path.join(self.cache, "pc.png"))
            if not pc_path.exists():
                PCnames = ['PC 1', 'PC 2', 'PC 3', 'PC 4']
                b = sns.pairplot(pd.DataFrame(self.PC,
                                              columns=PCnames),
                                 diag_kind='kde', plot_kws={"s": 3})
                b.fig.suptitle("Pair plot of PCs")
                b.savefig(pc_path.as_posix())

    def read_imagery(self):
        """
        Reads the imagery file
        :param file: input filename
        :param out: output filename
        """

        if not self.file == "":
            imagery = open(self.file, "rb+")

            self.img = np.zeros((1800, 1900, 4), dtype=float)
            # imagery=open(path,'rb+')
            print("File name: ", imagery.name)
            s = imagery.read(540)

            # -----------------------------------

            Band1 = np.zeros((5976, 6357))
            Band2 = np.zeros((5976, 6357))
            Band3 = np.zeros((5976, 6357))
            Band4 = np.zeros((5976, 6357))

            # -----------------------------------
            for j in range(5976):
                imagery.read(32)
                for i in range(6357):
                    s = imagery.read(1)
                    s = int.from_bytes(s, byteorder='little')
                    # print(s, end= ' ')
                    Band1[j][i] = s
                s = imagery.read(91)

                # -------------------------------
                imagery.read(32)
                for i in range(6357):
                    s = imagery.read(1)
                    s = int.from_bytes(s, byteorder='little')
                    Band2[j][i] = s
                s = imagery.read(91)

                # -------------------------------
                imagery.read(32)
                for i in range(6357):
                    s = imagery.read(1)
                    s = int.from_bytes(s, byteorder='little')
                    Band3[j][i] = s
                s = imagery.read(91)

                # -------------------------------

                imagery.read(32)
                for i in range(6357):
                    s = imagery.read(1)
                    s = int.from_bytes(s, byteorder='little')
                    Band4[j][i] = s
                s = imagery.read(91)

            # -----------------------------------
            self.img[:, :, 0] = cv2.resize(Band1 / 255, dsize=(1900, 1800), interpolation=cv2.INTER_CUBIC)
            self.img[:, :, 1] = cv2.resize(Band2 / 255, dsize=(1900, 1800), interpolation=cv2.INTER_CUBIC)
            self.img[:, :, 2] = cv2.resize(Band3 / 255, dsize=(1900, 1800), interpolation=cv2.INTER_CUBIC)
            self.img[:, :, 3] = cv2.resize(Band4 / 255, dsize=(1900, 1800), interpolation=cv2.INTER_CUBIC)

            del Band1, Band2, Band3, Band4
            imagery.close()

            # -----------------------------------
            np.save(os.path.join(self.cache, "imagery.npy"), self.img)

            return True
        else:
            return False

    def load_cached(self):
        """

        :return:
        """
        try:
            self.img = np.load(os.path.join(self.cache, "imagery.npy"))
            return True
        except:
            return self.read_imagery()
