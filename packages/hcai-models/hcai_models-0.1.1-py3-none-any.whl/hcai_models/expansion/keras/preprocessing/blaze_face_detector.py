from hcai_models.models.image.hcai_blaze_face.blaze_face import BlazeFace
import numpy as np
import tensorflow as tf


class BlazeFaceDetector:
    def __init__(self, min_score_thres: float = 0.7, force_cpu=False):
        self.detector = BlazeFace(weights="ls3d-w", min_score_thres=min_score_thres)
        if force_cpu:
            self.detector._device = "cpu"
        self.detector.build_model()

    def __call__(self, image, *args, **kwargs):
        return tf.py_function(func=self._internal_call, inp=[image], Tout=tf.float32)

    def _internal_call(self, image, *args, **kwargs):

        try:
            image = np.array(image)
        except:
            return np.array([0, 0, 0, 0, 0.0])

        input_img, (xshift, yshift), orig_size = self.detector.preprocessing(image)
        preds = self.detector.predict(np.expand_dims(input_img, 0))
        detected_face = self.detector.postprocessing(
            preds, shifts=(xshift, yshift), orig_size=orig_size
        )

        if detected_face.size == 0:
            # face not found -> none
            return np.array([0, 0, 0, 0, 0.0])
        else:
            return detected_face[0]
