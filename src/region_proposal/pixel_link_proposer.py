import cv2
import numpy as np
import os
from src.pylib import util
from preprocessing import ssd_vgg_preprocessing
from neural_nets import pixel_link_symbol
import pixel_link
import tensorflow as tf
# from config import *

slim = tf.contrib.slim
import config

tf.app.flags.DEFINE_string('checkpoint_path', r'C:\my_repo\BizDoc-Ocr\model\model.ckpt-73018',
                           'the path of pretrained model to be used. If there are checkpoints in train_dir, this config will be ignored.')
tf.app.flags.DEFINE_float('gpu_memory_fraction', -1,
                          'the gpu memory fraction to be used. If less than 0, allow_growth = True is used.')
tf.app.flags.DEFINE_integer(
    'num_readers', 1,
    'The number of parallel readers that read data from the dataset.')
tf.app.flags.DEFINE_integer(
    'num_preprocessing_threads', 4,
    'The number of threads used to create the batches.')
tf.app.flags.DEFINE_bool('preprocessing_use_rotation', False,
                         'Whether to use rotation for data augmentation')
tf.app.flags.DEFINE_string(
    'dataset_name', 'icdar2015', 'The name of the dataset to load.')
tf.app.flags.DEFINE_string(
    'dataset_split_name', 'test', 'The name of the train/test split.')
tf.app.flags.DEFINE_string('dataset_dir',
                           util.io.get_absolute_path('~/dataset/ICDAR2015/Challenge4/ch4_test_images'),
                           'The directory where the dataset files are stored.')
tf.app.flags.DEFINE_integer('eval_image_width', 1280, 'Train image size')
tf.app.flags.DEFINE_integer('eval_image_height', 768, 'Train image size')
tf.app.flags.DEFINE_bool('using_moving_average', True,
                         'Whether to use ExponentionalMovingAverage')
tf.app.flags.DEFINE_float('moving_average_decay', 0.9999,
                          'The decay rate of ExponentionalMovingAverage')
FLAGS = tf.app.flags.FLAGS


class PixelLinkProposer():
    _sess = None
    _graph = None
    _net = None
    _masks = None
    _image = None

    def __init__(self):
        self._config_initialization()
        # build up computation graph
        image = tf.placeholder(dtype=tf.int32, shape=[None, None, 3])
        processed_image, _, _, _, _ = ssd_vgg_preprocessing.preprocess_image(image, None, None, None, None,
                                                                             out_shape=config.image_shape,
                                                                             data_format=config.data_format,
                                                                             is_training=False)
        b_image = tf.expand_dims(processed_image, axis=0)

        # build model and loss
        net = pixel_link_symbol.PixelLinkNet(b_image, is_training=False)
        masks = pixel_link.tf_decode_score_map_to_mask_in_batch(
            net.pixel_pos_scores, net.link_pos_scores)
        self._image = image
        self._net = net
        self._masks = masks
        # end of build up

        global_step = slim.get_or_create_global_step()
        sess_config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
        if FLAGS.gpu_memory_fraction < 0:
            sess_config.gpu_options.allow_growth = True
        elif FLAGS.gpu_memory_fraction > 0:
            sess_config.gpu_options.per_process_gpu_memory_fraction = FLAGS.gpu_memory_fraction;

        checkpoint_dir = FLAGS.checkpoint_path

        if FLAGS.using_moving_average:
            variable_averages = tf.train.ExponentialMovingAverage(
                FLAGS.moving_average_decay)
            variables_to_restore = variable_averages.variables_to_restore()
            variables_to_restore[global_step.op.name] = global_step
        else:
            variables_to_restore = slim.get_variables_to_restore()

        saver = tf.train.Saver(var_list=variables_to_restore)

        # with tf.Session(graph=self._graph) as sess:
        #     saver.restore(sess, checkpoint_dir)
        #     self._graph = sess.graph
            # self._graph = tf.get_default_graph()
            # self._var_list = tf.all_variables()
            # self._sess = sess
        sess = tf.Session(config=sess_config)
        saver.restore(sess, checkpoint_dir)
        # self._graph = tf.get_default_graph()
        #     self._var_list = tf.all_variables()
        self._sess = sess


    def get_text_regions(self, image_data):

        # global_step = slim.get_or_create_global_step()
        # sess_config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
        # if FLAGS.gpu_memory_fraction < 0:
        #     sess_config.gpu_options.allow_growth = True
        # elif FLAGS.gpu_memory_fraction > 0:
        #     sess_config.gpu_options.per_process_gpu_memory_fraction = FLAGS.gpu_memory_fraction;
        #
        # checkpoint_dir = FLAGS.checkpoint_path
        #
        # if FLAGS.using_moving_average:
        #     variable_averages = tf.train.ExponentialMovingAverage(
        #         FLAGS.moving_average_decay)
        #     variables_to_restore = variable_averages.variables_to_restore()
        #     variables_to_restore[global_step.op.name] = global_step
        # else:
        #     variables_to_restore = slim.get_variables_to_restore()
        #
        # saver = tf.train.Saver(var_list=variables_to_restore)

        #with tf.Session(graph=self._graph) as sess:
        # sess.run(self._var_list)
        # saver.restore(sess, checkpoint_dir)
        link_scores, pixel_scores, mask_vals = self._sess.run(
            [self._net.link_pos_scores, self._net.pixel_pos_scores, self._masks],
            feed_dict={self._image: image_data})
        h, w, _ = image_data.shape

        def resize(img):
            return util.img.resize(img, size=(w, h),
                                   interpolation=cv2.INTER_NEAREST)

        def get_bboxes(mask):
            return pixel_link.mask_to_bboxes(mask, image_data.shape)

        def draw_bboxes(img, bboxes, color):
            for bbox in bboxes:
                points = np.reshape(bbox, [4, 2])
                cnts = util.img.points_to_contours(points)
                util.img.draw_contours(img, contours=cnts,
                                       idx=-1, color=color, border_width=1)

        image_idx = 0
        pixel_score = pixel_scores[image_idx, ...]
        mask = mask_vals[image_idx, ...]

        bboxes_det = get_bboxes(mask)
        print(bboxes_det)
        mask = resize(mask)
        pixel_score = resize(pixel_score)

        return bboxes_det

    def _get_bbox(self, image_data, pixel_pos_scores, link_pos_scores):

        mask = pixel_link.decode_batch(pixel_pos_scores, link_pos_scores)[0, ...]
        bboxes = pixel_link.mask_to_bboxes(mask, image_data.shape)

        return bboxes

    def _config_initialization(self):
        image_shape = (FLAGS.eval_image_height, FLAGS.eval_image_width)
        config.load_config(FLAGS.checkpoint_path)
        config.init_config(image_shape,
                           batch_size=1,
                           pixel_conf_threshold=0.9,
                           link_conf_threshold=0.1,
                           num_gpus=1,
                           )


def draw_bboxes(img, bboxes, color):
    for bbox in bboxes:
        points = np.reshape(bbox, [4, 2])

        cnts = util.img.points_to_contours(points)
        util.img.draw_contours(img, contours=cnts,
                               idx=-1, color=color, border_width=5)

# proposer = PixelLinkProposer()
# mode = cv2.IMREAD_COLOR
# image = cv2.imread(r'C:\my_repo\BizDoc-Ocr\volvo.jpg', mode)
# bboxes_det = proposer.get_text_regions(image)
# draw_bboxes(image, bboxes_det, util.img.COLOR_RGB_RED)
# # proposer.get_text_regions()
# cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\volvo_result.jpg', image)

# response = ''
# for bbox in bboxes_det:
#     points = np.reshape(bbox, [4, 2])
#     cnts = util.img.points_to_contours(points)
#     crop = util.img.get_contour_region_in_rect(image, contours=cnts)
#     text = self.__ocr.read_text(crop)
#     response = response + ' ' + text
