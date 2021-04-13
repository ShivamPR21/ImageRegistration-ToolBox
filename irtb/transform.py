import os

import cv2
import numpy as np

np.set_printoptions(precision=3)


def add_row(mat):
    tmp = np.eye(np.max(np.shape(mat)))
    tmp[:np.shape(mat)[0], :np.shape(mat)[1]] = mat
    return tmp


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
        self.T_t = np.float32(np.concatenate((np.eye(2), [
            [self.params['t_x']],
            [self.params['t_y']]
        ]), axis=1))

        self.T_s = np.float32(np.concatenate((np.diag([self.params['scale_x'],
                                            self.params['scale_y']]),
                                   [[0], [0]]), axis=1))

        self.T_v = np.float32(np.concatenate(([[1, self.params['skew_x']],
                                    [self.params['skew_y'], 1]],
                                   [[0], [0]]), axis=1))
        theta = self.params['rot']
        self.T_r = np.array([[np.cos(theta), np.sin(theta), 0],
                             [-np.sin(theta), np.cos(theta), 0]], dtype=np.float32)

        self.T = np.float32(add_row(
            self.T_r).dot(
            add_row(self.T_t)).dot(
            add_row(self.T_v)).dot(
            add_row(self.T_s)))[:2, :3]
        return

    def transform(self):
        """
        Transforms the image and store the information
        :return: Dict WarpedImages path
        """
        self.init_transforms()
        src = cv2.imread(self.file, flags=cv2.CV_32F)

        final_shape = np.asarray(src.shape[:2], dtype=float)*np.array([abs(self.params['scale_x'])*2,
                                                                       abs(self.params['scale_y'])*2])
        final_shape = np.array(final_shape, dtype=int)

        src_t = cv2.warpAffine(src, self.T_t, (final_shape[1], final_shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'trans.jpeg'), src_t)

        src_s = cv2.warpAffine(src, self.T_s, (final_shape[1], final_shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'scale.jpeg'), src_s)

        src_v = cv2.warpAffine(src, self.T_v, (final_shape[1], final_shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'skew.jpeg'), src_v)

        src_r = cv2.warpAffine(src, self.T_r, (final_shape[1], final_shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'rot.jpeg'), src_r)

        src_w = cv2.warpAffine(src, self.T, (final_shape[1], final_shape[0]))
        cv2.imwrite(os.path.join(self.cache_dir, 'transform.jpeg'), src_w)

        return {'translation': os.path.join(self.cache_dir, 'trans.jpeg'),
                'rotation': os.path.join(self.cache_dir, 'rot.jpeg'),
                'scale': os.path.join(self.cache_dir, 'scale.jpeg'),
                'skew': os.path.join(self.cache_dir, 'skew.jpeg'),
                'transformation': os.path.join(self.cache_dir, 'transform.jpeg')}
