from pylib.util import log
from pylib.util import dtype
from pylib.util import plt
from pylib.util import np
from pylib.util import img
_img = img
from pylib.util import dec
from pylib.util import rand
from pylib.util import mod
from pylib.util import proc
from pylib.util import test
from pylib.util import neighbour as nb
#import mask
from pylib.util import str_ as str
import io as sys_io
from pylib.util import io_ as io
from pylib.util import feature
from pylib.util import thread_ as thread
from pylib.util import caffe_ as caffe
from pylib.util import tf
from pylib.util import cmd
from pylib.util import ml
from pylib.util import url
from pylib.util import time_ as time
from pylib.util.progress_bar import ProgressBar
import sys
# log.init_logger('~/temp/log/log_' + get_date_str() + '.log')

def exit(code = 0):
    sys.exit(0)
    
is_main = mod.is_main
init_logger = log.init_logger

def get_temp_path(name = ''):
    _count = get_count();
    path = '~/temp/no-use/images/%s_%d_%s.png'%(log.get_date_str(), _count, name)
    return path
def sit(img = None, format = 'rgb', path = None, name = ""):
    if path is None:
        path = get_temp_path(name)
        
    if img is None:
        plt.save_image(path)
        return path
    
        
    if format == 'bgr':
        img = _img.bgr2rgb(img)
    if type(img) == list:
        plt.show_images(images = img, path = path, show = False, axis_off = True, save = True)
    else:
        plt.imwrite(path, img)
    
    return path
_count = 0;

def get_count():
    global _count;
    _count += 1;
    return _count    

def cit(img, path = None, rgb = True, name = ""):
    _count = get_count();
    if path is None:
        img = np.np.asarray(img, dtype = np.np.uint8)
        path = '~/temp/no-use/images/%s_%s_%d.jpg'%(name, log.get_date_str(), _count)
        _img.imwrite(path, img, rgb = rgb)
    return path        

argv = sys.argv
    
