from __future__ import division
import PIL
from PIL import Image
import logging
import numpy as np
import scipy.stats


class ImageQueryError(Exception):
    def __init__(self):
        pass
    def ImageQueryShapeNotMatchError(self):
        pass

class ImageQuery(ImageQueryError):
    def __init__(self,im_path):
        super(ImageQueryError,self).__init__()
        self.im=im_path

    def _create_and_image(self):
        try:
            pic=Image.open(self.im)
            return pic
        except (FileNotFoundError) as e:
            logging.error(f'Failed to open image:{self.im}:{e}')
            return None
        except (PIL.UnidentifiedImageError) as e:
            logging.error(f'Failed to identify image {self.im}: {e}')
            return None
        finally:
            pass

    def pixel_difference(self,compared_im):
        if (self._create_and_image().size!=compared_im._create_and_image().size):
            logging.error(f'Image shape not match,pic1 size:{self._create_and_image.size},pic2 size:{compared_im._create_and_image.size}')
            raise ImageQueryError.ImageQueryShapeNotMatchError("图片尺寸不匹配")
        pix1=np.array(self._create_and_image())
        pix2=np.array(compared_im._create_and_image())
        pix_minus=np.abs(pix1-pix2)
        pix_sum=np.sum(pix_minus)
        similarity=1-pix_sum/len(list(self._create_and_image().getdata()))
        return similarity
        
    def pearson_similarity(self,compared_im):
        x=self._create_and_image().histogram()
        y=compared_im._create_and_image().histogram()
        similarity=scipy.stats.pearsonr(x, y)[0]
        return similarity
    
    def spearman_similarity(self,compared_im):
        x=self._create_and_image().histogram()
        y=compared_im._create_and_image().histogram()
        similarity=scipy.stats.spearmanr(x, y)[0]
        return similarity
    
    def kendall_similarity(self,compared_im):
        x=self._create_and_image().histogram()
        y=compared_im._create_and_image().histogram()
        similarity=scipy.stats.kendalltau(x, y)[0]
        return similarity

im1=ImageQuery(r'C:/Users/黄煜旸/Desktop/lfw/Aaron_Sorkin/Aaron_Sorkin_0001.jpg')
im2=ImageQuery(r'C:/Users/黄煜旸/Desktop/lfw/Aaron_Sorkin/Aaron_Sorkin_0002.jpg')
pic1=im1._create_and_image()
pic2=im2._create_and_image()
sim1=im1.pixel_difference(im2)
sim2=im1.spearman_similarity(im2)
sim3=im1.kendall_similarity(im2)
print(sim1)
print(sim2)
print(sim3)