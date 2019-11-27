__author__ = "tjvsonsbeek"
__copyright__ = "tjvsonsbeek"
__license__ = "mit"

import cv2
import keras.applications.imagenet_utils
from keras.applications.vgg19 import preprocess_input
import keras.engine.training
from keras.engine.training import Container
from mock import patch
import ntpath
import numpy as np
import numpy.lib.shape_base
from numpy.lib.shape_base import matrix
import os
import python_metal_fe.feature_extraction.main
from python_metal_fe.feature_extraction.main import MetaFeatureExtraction
from python_metal_fe.utils import correlation_coefficient
from python_metal_fe.utils import mutual_information
from python_metal_fe.utils import normalize
from python_metal_fe.utils import read_nifti
from python_metal_fe.utils import shannon_entropy
import python_metal_fe.utils.main
from python_metal_fe.utils.main import PCA
import random
from random import Random
from scipy.ndimage import zoom
from scipy.stats import kurtosis
from scipy.stats import skew
from tqdm import tqdm
import unittest


class MainTest(unittest.TestCase):
    def test_gather_meta_features(self):
        self.assertEqual(
            MetaFeatureExtraction.gather_meta_features(self=<python_metal_fe.feature_extraction.main.MetaFeatureExtraction object at 0x000001CC0177EBE0>),
            None
        )


    @patch.object(python_metal_fe.utils.main, 'read_nifti')
    @patch.object(python_metal_fe.utils.main, 'normalize')
    def test_gather_meta_features_DL_NoTop(self, mock_normalize, mock_read_nifti):
        mock_normalize.return_value = array([[[0.55921053, 0.49342105, 0.44736842, ..., 0.58552632,
         0.63815789, 0.64473684],
        [0.55921053, 0.54605263, 0.54605263, ..., 0.60526316,
         0.65789474, 0.63815789],
        [0.56578947, 0.51315789, 0.46710526, ..., 0.56578947,
         0.60526316, 0.60526316],
        ...,
        [0.26315789, 0.28947368, 0.23026316, ..., 0.22368421,
         0.34210526, 0.13815789],
        [0.23684211, 0.23684211, 0.19078947, ..., 0.18421053,
         0.33552632, 0.29605263],
        [0.20394737, 0.19736842, 0.20394737, ..., 0.13815789,
         0.20394737, 0.35526316]],

       [[0.51315789, 0.51315789, 0.53289474, ..., 0.56578947,
         0.61842105, 0.65131579],
        [0.53947368, 0.52631579, 0.55921053, ..., 0.57894737,
         0.59868421, 0.63157895],
        [0.53947368, 0.50657895, 0.51315789, ..., 0.56578947,
         0.57894737, 0.61184211],
        ...,
        [0.25      , 0.25657895, 0.23684211, ..., 0.18421053,
         0.23684211, 0.10526316],
        [0.20394737, 0.21052632, 0.20394737, ..., 0.11184211,
         0.15789474, 0.09210526],
        [0.18421053, 0.15789474, 0.19078947, ..., 0.07236842,
         0.11842105, 0.15131579]],

       [[0.48684211, 0.5       , 0.53289474, ..., 0.54605263,
         0.57894737, 0.625     ],
        [0.55921053, 0.55921053, 0.58552632, ..., 0.55263158,
         0.56578947, 0.60526316],
        [0.56578947, 0.51973684, 0.53947368, ..., 0.54605263,
         0.58552632, 0.60526316],
        ...,
        [0.38815789, 0.32236842, 0.28289474, ..., 0.11842105,
         0.13157895, 0.07894737],
        [0.28289474, 0.22368421, 0.19736842, ..., 0.07894737,
         0.03289474, 0.05921053],
        [0.20394737, 0.13815789, 0.18421053, ..., 0.11184211,
         0.07236842, 0.07236842]],

       ...,

       [[0.30921053, 0.36842105, 0.40131579, ..., 0.52631579,
         0.59210526, 0.59868421],
        [0.38157895, 0.38157895, 0.31578947, ..., 0.59868421,
         0.63157895, 0.63815789],
        [0.32894737, 0.28947368, 0.25657895, ..., 0.59868421,
         0.61184211, 0.61842105],
        ...,
        [0.70394737, 0.67105263, 0.57236842, ..., 0.32894737,
         0.28947368, 0.26973684],
        [0.60526316, 0.63815789, 0.5       , ..., 0.26973684,
         0.27631579, 0.25657895],
        [0.5       , 0.54605263, 0.32236842, ..., 0.23684211,
         0.26973684, 0.25657895]],

       [[0.40131579, 0.40789474, 0.34210526, ..., 0.45394737,
         0.53947368, 0.54605263],
        [0.29605263, 0.30921053, 0.26315789, ..., 0.60526316,
         0.65131579, 0.65131579],
        [0.30921053, 0.31578947, 0.28289474, ..., 0.61842105,
         0.61842105, 0.61842105],
        ...,
        [0.55263158, 0.51315789, 0.56578947, ..., 0.28947368,
         0.27631579, 0.25657895],
        [0.50657895, 0.55263158, 0.51315789, ..., 0.27631579,
         0.27631579, 0.28289474],
        [0.44736842, 0.53947368, 0.35526316, ..., 0.29605263,
         0.30263158, 0.32236842]],

       [[0.34868421, 0.27631579, 0.23026316, ..., 0.33552632,
         0.41447368, 0.43421053],
        [0.36184211, 0.32894737, 0.32236842, ..., 0.54605263,
         0.60526316, 0.59868421],
        [0.45394737, 0.42105263, 0.40789474, ..., 0.61842105,
         0.63157895, 0.625     ],
        ...,
        [0.46710526, 0.34868421, 0.40131579, ..., 0.31578947,
         0.30921053, 0.28289474],
        [0.5       , 0.47368421, 0.40789474, ..., 0.33552632,
         0.30921053, 0.31578947],
        [0.5       , 0.42763158, 0.24342105, ..., 0.31578947,
         0.29605263, 0.30263158]]])
        mock_read_nifti.return_value = array([[[ 87,  77,  70, ...,  91,  99, 100],
        [ 87,  85,  85, ...,  94, 102,  99],
        [ 88,  80,  73, ...,  88,  94,  94],
        ...,
        [ 42,  46,  37, ...,  36,  54,  23],
        [ 38,  38,  31, ...,  30,  53,  47],
        [ 33,  32,  33, ...,  23,  33,  56]],

       [[ 80,  80,  83, ...,  88,  96, 101],
        [ 84,  82,  87, ...,  90,  93,  98],
        [ 84,  79,  80, ...,  88,  90,  95],
        ...,
        [ 40,  41,  38, ...,  30,  38,  18],
        [ 33,  34,  33, ...,  19,  26,  16],
        [ 30,  26,  31, ...,  13,  20,  25]],

       [[ 76,  78,  83, ...,  85,  90,  97],
        [ 87,  87,  91, ...,  86,  88,  94],
        [ 88,  81,  84, ...,  85,  91,  94],
        ...,
        [ 61,  51,  45, ...,  20,  22,  14],
        [ 45,  36,  32, ...,  14,   7,  11],
        [ 33,  23,  30, ...,  19,  13,  13]],

       ...,

       [[ 49,  58,  63, ...,  82,  92,  93],
        [ 60,  60,  50, ...,  93,  98,  99],
        [ 52,  46,  41, ...,  93,  95,  96],
        ...,
        [109, 104,  89, ...,  52,  46,  43],
        [ 94,  99,  78, ...,  43,  44,  41],
        [ 78,  85,  51, ...,  38,  43,  41]],

       [[ 63,  64,  54, ...,  71,  84,  85],
        [ 47,  49,  42, ...,  94, 101, 101],
        [ 49,  50,  45, ...,  96,  96,  96],
        ...,
        [ 86,  80,  88, ...,  46,  44,  41],
        [ 79,  86,  80, ...,  44,  44,  45],
        [ 70,  84,  56, ...,  47,  48,  51]],

       [[ 55,  44,  37, ...,  53,  65,  68],
        [ 57,  52,  51, ...,  85,  94,  93],
        [ 71,  66,  64, ...,  96,  98,  97],
        ...,
        [ 73,  55,  63, ...,  50,  49,  45],
        [ 78,  74,  64, ...,  53,  49,  50],
        [ 78,  67,  39, ...,  50,  47,  48]]], dtype=uint8)
        self.assertEqual(
            MetaFeatureExtraction.gather_meta_features_DL_NoTop(self=<python_metal_fe.feature_extraction.main.MetaFeatureExtraction object at 0x000001CC0177EBE0>),
            None
        )


    @patch.object(ntpath, 'join')
    @patch.object(Random, 'sample')
    def test_gather_random_addresses(self, mock_sample, mock_join):
        mock_sample.return_value = ['C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_168.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_283.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_043.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_247.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_110.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_117.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_209.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_278.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_198.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_339.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_291.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_285.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_392.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_082.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_028.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_151.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_179.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_237.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_073.nii.gz', 'C:\\Users\\s149561\\Documents\\DecathlonData\\Task04_Hippocampus/imagesTs\\hippocampus_369.nii.gz']
        mock_join.return_value = 'metafeature_extraction_result\\metadata'
        self.assertEqual(
            MetaFeatureExtraction.gather_random_addresses(self=<python_metal_fe.feature_extraction.main.MetaFeatureExtraction object at 0x000001CC0177EBE0>),
            None
        )


    @patch.object(matrix, 'expand_dims')
    @patch.object(Container, 'predict')
    @patch.object(keras.applications.imagenet_utils, 'preprocess_input')
    def test_im2features(self, mock_preprocess_input, mock_predict, mock_expand_dims):
        mock_preprocess_input.return_value = array([[[[-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         ...,
         [-103.51    , -116.35    , -123.251   ],
         [-103.51137 , -116.351364, -123.252365],
         [-103.51137 , -116.351364, -123.252365]],

        [[-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         ...,
         [-103.51    , -116.35    , -123.251   ],
         [-103.51137 , -116.351364, -123.252365],
         [-103.51137 , -116.351364, -123.252365]],

        [[-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         [-103.32058 , -116.160576, -123.06158 ],
         ...,
         [-103.51    , -116.35    , -123.251   ],
         [-103.51137 , -116.351364, -123.252365],
         [-103.51137 , -116.351364, -123.252365]],

        ...,

        [[-103.735054, -116.57505 , -123.47605 ],
         [-103.735054, -116.57505 , -123.47605 ],
         [-103.737335, -116.57733 , -123.47833 ],
         ...,
         [-103.34148 , -116.18147 , -123.08247 ],
         [-103.33374 , -116.17374 , -123.07474 ],
         [-103.33374 , -116.17374 , -123.07474 ]],

        [[-103.735054, -116.57505 , -123.47605 ],
         [-103.735054, -116.57505 , -123.47605 ],
         [-103.737335, -116.57733 , -123.47833 ],
         ...,
         [-103.34148 , -116.18147 , -123.08247 ],
         [-103.33374 , -116.17374 , -123.07474 ],
         [-103.33374 , -116.17374 , -123.07474 ]],

        [[-103.735054, -116.57505 , -123.47605 ],
         [-103.735054, -116.57505 , -123.47605 ],
         [-103.737335, -116.57733 , -123.47833 ],
         ...,
         [-103.34148 , -116.18147 , -123.08247 ],
         [-103.33374 , -116.17374 , -123.07474 ],
         [-103.33374 , -116.17374 , -123.07474 ]]]], dtype=float32)
        mock_predict.return_value = array([[[[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  8.141227  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          29.961752  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        , 29.71879   ],
         [ 0.        ,  0.        ,  2.835238  , ...,  0.        ,
           0.        , 15.518286  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.6441987 ,  6.586091  ],
         ...,
         [ 0.        ,  0.        ,  0.580748  , ...,  0.        ,
           2.0914862 ,  5.675252  ],
         [ 0.        ,  0.        ,  1.2477144 , ...,  0.        ,
           8.349115  ,  6.786959  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          38.001587  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           9.460437  , 12.843406  ],
         [ 0.        ,  0.        ,  4.551975  , ...,  0.        ,
           1.1275748 ,  0.23358706],
         [ 0.        ,  0.        ,  2.824609  , ...,  0.        ,
           2.9222782 ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  4.5289993 , ...,  0.        ,
           2.7016513 ,  0.        ],
         [ 0.        ,  0.        ,  5.3546715 , ...,  0.        ,
           8.162596  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          28.414124  ,  0.        ]],

        ...,

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.060561  ,  1.5057058 ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           3.1433582 ,  0.        ],
         [ 0.        ,  0.        ,  0.51929885, ...,  0.        ,
          22.511705  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.562549  ,  7.6590276 ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.519301  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.947106  ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           9.874453  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           6.3303103 ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          24.514198  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.23088229, 42.302994  ],
         [ 0.        ,  0.        , 11.719561  , ...,  0.        ,
          11.762271  , 28.06691   ],
         [ 0.        ,  0.        ,  8.519634  , ...,  0.        ,
          12.18072   , 18.185322  ],
         ...,
         [ 0.        ,  0.        ,  7.27026   , ...,  0.        ,
           9.187942  , 17.866184  ],
         [ 0.        ,  0.        ,  8.820536  , ...,  0.        ,
           7.339248  , 24.715927  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          26.812273  , 26.495995  ]]]], dtype=float32)
        mock_expand_dims.return_value = array([[[[-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         ...,
         [-123.251   , -116.35    , -103.51    ],
         [-123.252365, -116.351364, -103.51137 ],
         [-123.252365, -116.351364, -103.51137 ]],

        [[-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         ...,
         [-123.251   , -116.35    , -103.51    ],
         [-123.252365, -116.351364, -103.51137 ],
         [-123.252365, -116.351364, -103.51137 ]],

        [[-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         [-123.06158 , -116.160576, -103.32058 ],
         ...,
         [-123.251   , -116.35    , -103.51    ],
         [-123.252365, -116.351364, -103.51137 ],
         [-123.252365, -116.351364, -103.51137 ]],

        ...,

        [[-123.47605 , -116.57505 , -103.735054],
         [-123.47605 , -116.57505 , -103.735054],
         [-123.47833 , -116.57733 , -103.737335],
         ...,
         [-123.08247 , -116.18147 , -103.34148 ],
         [-123.07474 , -116.17374 , -103.33374 ],
         [-123.07474 , -116.17374 , -103.33374 ]],

        [[-123.47605 , -116.57505 , -103.735054],
         [-123.47605 , -116.57505 , -103.735054],
         [-123.47833 , -116.57733 , -103.737335],
         ...,
         [-123.08247 , -116.18147 , -103.34148 ],
         [-123.07474 , -116.17374 , -103.33374 ],
         [-123.07474 , -116.17374 , -103.33374 ]],

        [[-123.47605 , -116.57505 , -103.735054],
         [-123.47605 , -116.57505 , -103.735054],
         [-123.47833 , -116.57733 , -103.737335],
         ...,
         [-123.08247 , -116.18147 , -103.34148 ],
         [-123.07474 , -116.17374 , -103.33374 ],
         [-123.07474 , -116.17374 , -103.33374 ]]]], dtype=float32)
        self.assertEqual(
            MetaFeatureExtraction.im2features(self=<python_metal_fe.feature_extraction.main.MetaFeatureExtraction object at 0x000001CC0177EBE0>,im=array([[0.24170616, 0.27014217, 0.43601897, ..., 0.35545024, 0.3222749 ,
        0.2748815 ],
       [0.22748816, 0.3507109 , 0.55450237, ..., 0.45971566, 0.4265403 ,
        0.40758294],
       [0.4265403 , 0.51658773, 0.54028434, ..., 0.5687204 , 0.53080565,
        0.48341233],
       ...,
       [0.3507109 , 0.3364929 , 0.3507109 , ..., 0.54028434, 0.42180094,
        0.3507109 ],
       [0.35545024, 0.2606635 , 0.25118485, ..., 0.38388628, 0.36966825,
        0.33175358],
       [0.22748816, 0.17061612, 0.24170616, ..., 0.24170616, 0.25118485,
        0.2748815 ]], dtype=float32)),
            array([[[[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  8.1096735 ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          29.744665  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        , 29.499908  ],
         [ 0.        ,  0.        ,  3.0435605 , ...,  0.        ,
           0.        , 16.362541  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.77060723,  6.805277  ],
         ...,
         [ 0.        ,  0.        ,  0.29119036, ...,  0.        ,
           2.1170866 ,  5.7534957 ],
         [ 0.        ,  0.        ,  0.9777852 , ...,  0.        ,
           8.4180975 ,  6.490175  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          37.715023  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           9.238224  , 13.015331  ],
         [ 0.        ,  0.        ,  5.0521483 , ...,  0.        ,
           1.3193543 ,  0.        ],
         [ 0.        ,  0.        ,  3.290788  , ...,  0.        ,
           2.9520316 ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  4.2575765 , ...,  0.        ,
           2.84291   ,  0.        ],
         [ 0.        ,  0.        ,  5.118063  , ...,  0.        ,
           8.333411  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          28.447735  ,  0.        ]],

        ...,

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.09842   ,  2.0288312 ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.        ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           3.2852535 ,  0.        ],
         [ 0.        ,  0.        ,  0.47811043, ...,  0.        ,
          22.539162  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.752235  ,  7.4551573 ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          11.9097    ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          12.205123  ,  0.        ],
         ...,
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           9.898854  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
           6.580569  ,  0.        ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          24.278385  ,  0.        ]],

        [[ 0.        ,  0.        ,  0.        , ...,  0.        ,
           0.49857038, 42.17754   ],
         [ 0.        ,  0.        , 11.72733   , ...,  0.        ,
          12.191268  , 28.420885  ],
         [ 0.        ,  0.        ,  8.683831  , ...,  0.        ,
          12.391597  , 18.71187   ],
         ...,
         [ 0.        ,  0.        ,  7.2902384 , ...,  0.        ,
           9.356304  , 18.013643  ],
         [ 0.        ,  0.        ,  8.937866  , ...,  0.        ,
           7.572917  , 25.315353  ],
         [ 0.        ,  0.        ,  0.        , ...,  0.        ,
          26.833672  , 27.171438  ]]]], dtype=float32)
        )


    def test_load_model(self):
        self.assertEqual(
            MetaFeatureExtraction.load_model(self=<python_metal_fe.feature_extraction.main.MetaFeatureExtraction object at 0x000001CC0177EBE0>,model=<keras.engine.training.Model object at 0x000001CC0177E278>),
            None
        )


if __name__ == "__main__":
    unittest.main()
