from evaluation.fid_v2 import *
from evaluation.inception_score_v2 import *
from glob import glob
from evaluation.calculate_is_fid import get_generated_samples
import os


def load_images_from_directory(img_dir: str):
    filenames = glob(os.path.join(img_dir, '*.*'))
    images = [get_images(filename) for filename in filenames]
    images = np.transpose(images, axes=[0, 3, 1, 2])
    return images


def inception_score(images: np.array):
    # A smaller BATCH_SIZE reduces GPU memory usage, but at the cost of a slight slowdown
    BATCH_SIZE = 1

    # Run images through Inception.
    inception_images = tf.placeholder(tf.float32, [BATCH_SIZE, 3, None, None])

    logits = inception_logits(inception_images)

    IS = get_inception_score(BATCH_SIZE, images, inception_images, logits, splits=10)

    print()
    print("IS : ", IS)


def frechet_inception_distance(real_images: np.array, fake_images: np.array):
    # A smaller BATCH_SIZE reduces GPU memory usage, but at the cost of a slight slowdown
    BATCH_SIZE = 1

    # Run images through Inception.
    inception_images = tf.placeholder(tf.float32, [BATCH_SIZE, 3, None, None])
    real_activation = tf.placeholder(tf.float32, [None, None], name='activations1')
    fake_activation = tf.placeholder(tf.float32, [None, None], name='activations2')

    fcd = frechet_classifier_distance_from_activations(real_activation, fake_activation)
    activations = inception_activations(inception_images)

    FID = get_fid(fcd, BATCH_SIZE, real_images, fake_images, inception_images, real_activation, fake_activation,
                  activations)

    print()
    print("FID : ", FID / 100)


def main():
    experiment_name = "BigGAN_C10_seed0_Gch64_Dch64_bs50_nDs4_Glr2.0e-04_Dlr2.0e-04_Gnlrelu_Dnlrelu_GinitN02_DinitN02_ema"
    # file_name = "2020-10-23_15_24_32"
    file_name = "2020-10-22_21_18_55"
    npz_path = rf'.\samples\{experiment_name}\{file_name}.npz'
    generated_samples = get_generated_samples(npz_path)
    inception_score(generated_samples)
    # frechet_inception_distance()


if __name__ == '__main__':
    main()
