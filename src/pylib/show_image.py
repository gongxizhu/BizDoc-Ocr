import src.pylib.util as util
path = util.argv[1]
util.plt.imshow(path, util.img.imread(path, rgb = True))