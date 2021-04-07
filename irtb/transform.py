import os

import cv2
import numpy as np

np.set_printoptions(precision=3)


class TransformProc:
    """
    Image Processing Class
    """

    def __init__(self, file, cache_dir, params):
        self.file = file
        self.cache_dir = cache_dir
        self.params = params
        self.interp = params['interp_method']

        self.T = None
        self.T_t = None
        self.T_r = None
        self.T_v = None
        self.T_s = None

    def init_transforms(self):
        self.T_t = np.concatenate((np.eye(2), [
            [self.params['t_x']],
            [self.params['t_y']]
        ]), axis=1)

        self.T_s = np.concatenate((np.diag([self.params['scale_x'],
                                            self.params['scale_y']]),
                                   [[0], [0]]), axis=1)

        self.T_v = np.concatenate(([[0, self.params['skew_x']],
                                    [self.params['skew_y'], 0]],
                                   [[0], [0]]), axis=1)
        theta = self.params['rot']
        self.T_r = np.array([[np.cos(theta), np.sin(theta), 0],
                             [-np.sin(theta), np.cos(theta), 0]], dtype=float)

        self.T = self.T_r.dot(self.T_t).dot(self.T_v).dot(self.T_s)
        return

    def tranform(self):
        self.init_transforms()
        src = cv2.imread(self.file)

        src_t = cv2.warpAffine(src, self.T_t, (src.shape[1], src.shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 't.png'), src_t)

        src_s = cv2.warpAffine(src, self.T_s, (src.shape[1], src.shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 's.png'), src_s)

        src_v = cv2.warpAffine(src, self.T_v, (src.shape[1], src.shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'v.png'), src_v)

        src_r = cv2.warpAffine(src, self.T_r, (src.shape[1], src.shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'r.png'), src_r)

        src_w = cv2.warpAffine(src, self.T, (src.shape[1], src.shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'T.png'), src_w)

        return {'T': os.path.join(self.cache_dir, 'T.png'),
                'r': os.path.join(self.cache_dir, 'r.png'),
                'v': os.path.join(self.cache_dir, 'v.png'),
                's': os.path.join(self.cache_dir, 's.png'),
                't': os.path.join(self.cache_dir, 't.png')}