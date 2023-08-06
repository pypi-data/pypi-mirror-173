from hcai_models.core.abstract_model import Model

from datetime import datetime
from pathlib import Path

from tensorflow import keras
import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt

from hcai_models.models.generative.hcai_cycle_gan.classifier import build_classifier
from hcai_models.models.generative.hcai_cycle_gan.discriminator import build_discriminator
from hcai_models.models.generative.hcai_cycle_gan.generator import build_generator


class CycleGAN(Model):

    def __init__(self,
                 *args,
                 img_rows: int = 224,
                 img_cols: int = 224,
                 channels: int = 3,
                 use_wasserstein: bool = False,
                 filters_generator: int = 32,
                 filters_discriminator: int = 64,
                 # component learning rates
                 lr_classifier: float = 0.00001,
                 lr_src_classifier: float = 0.00001,
                 lr_discriminator: float = 0.00005,
                 lr_generator: float = 0.0001,
                 # Loss weights
                 lambda_cycle: float = 100.0,  # Cycle-consistency loss
                 lambda_identity: float = 100.0,  # Identity loss
                 lambda_classifier: float = 0.0,  # Classification loss
                 lambda_source_classifier: float = 1.0,  # Counterfactual loss
                 lambda_discriminator: float = 10.0,  # Discriminator loss,
                 clip_value: float = 0.05,
                 classifier = None,
                 **kwargs):
        # Input shape
        super().__init__(*args, **kwargs)

        self.img_rows = img_rows
        self.img_cols = img_cols
        self.channels = channels
        self.img_shape = (self.img_rows, self.img_cols, self.channels)

        # Calculate output shape of D (PatchGAN)
        patch = int(self.img_rows / 2 ** 4)
        self.disc_patch = (patch, patch, 1)

        self.use_wasserstein = use_wasserstein

        # Number of filters in the first layer of G and D
        self.gf = filters_generator
        self.df = filters_discriminator

        self.lr_classifier = lr_classifier
        self.lr_src_classifier = lr_src_classifier
        self.lr_discriminator = lr_discriminator
        self.lr_generator = lr_generator
        self.lambda_cycle = lambda_cycle
        self.lambda_identity = lambda_identity
        self.lambda_classifier = lambda_classifier
        self.lambda_source_classifier = lambda_source_classifier
        self.lambda_discriminator = lambda_discriminator

        self.clip_value = clip_value

        self.d_source = None
        self.d_target = None
        self.g_target = None
        self.g_source = None
        self.combined = None
        self.classifier = classifier
        self._premade_classifier = classifier is not None
        self.source_classifier = None

    def preprocessing(self, sample: object) -> object:
        pass

    def postprocessing(self, prediction: object, **kwargs) -> object:
        pass

    def load_weights(self, filepath):
        pass

    def predict(self, sample):
        pass

    def train_classifier(self, paired_set, epochs: int = 1):

        paired_set = paired_set.map(lambda batch: (batch["image_source"] / 255, batch["label_source"]))
        self.classifier.fit(paired_set, epochs=epochs)

    def train_source_classifier(self, source_set, epochs: int = 1):

        source_set = source_set.map(lambda x, y: (x / 255, y))
        self.source_classifier.fit(source_set, epochs=epochs)

    def fit(self, *args,
            paired_set=None,
            source_set=None,
            batch_size: int = 16,
            epochs: int = 1,
            epochs_classifier: int = 1,
            epochs_source_classifier: int = 1,
            image_dir: str = None,
            log_callback=None,
            image_callback=None,
            **kwargs):

        start_time = datetime.now()
        # train the classifiers
        if not self._premade_classifier:
            self.train_classifier(paired_set, epochs_classifier)
        self.train_source_classifier(source_set, epochs_source_classifier)

        # Adversarial loss ground truths
        if not self.use_wasserstein:
            # regular: binary class labels valid = 1 fake = 0
            valid = np.full(shape=(batch_size,) + self.disc_patch, fill_value=1)
            fake = np.full(shape=(batch_size,) + self.disc_patch, fill_value=0)
        else:
            # wasserstein: multiplier for classifier outputs - minimize valid score, maximize fake score
            valid = np.full(shape=(batch_size,) + self.disc_patch, fill_value=1.0)
            fake = np.full(shape=(batch_size,) + self.disc_patch, fill_value=-1.0)

        # source and target label are inverted from the training set of the source classifier
        class_source = np.ones(batch_size)
        class_target = np.zeros(batch_size)

        stop_early = False
        for epoch in range(epochs):

            if stop_early:
                break

            iterator = paired_set.as_numpy_iterator()
            for batch_i, batch in enumerate(iterator):

                imgs_source = batch["image_source"] / 255
                imgs_target = batch["image_target"] / 255

                labels_source = batch["label_source"]

                if imgs_source.shape[0] != batch_size:
                    continue

                # ----------------------
                #  Train Discriminators
                # ----------------------

                # Translate images to opposite domain
                fake_target = self.g_target.predict(imgs_source)
                fake_source = self.g_source.predict(imgs_target)

                # Train the discriminators (original images = real / translated = Fake)
                disc_steps = 5 if self.use_wasserstein else 1

                for step in range(disc_steps):
                    disc_source_loss_real = self.d_source.train_on_batch(imgs_source, valid)
                    disc_source_loss_fake = self.d_source.train_on_batch(fake_source, fake)
                    disc_source_loss = 0.5 * np.add(disc_source_loss_real, disc_source_loss_fake)

                    disc_target_loss_real = self.d_target.train_on_batch(imgs_target, valid)
                    disc_target_loss_fake = self.d_target.train_on_batch(fake_target, fake)
                    disc_target_loss = 0.5 * np.add(disc_target_loss_real, disc_target_loss_fake)

                    # Total disciminator loss
                    disc_loss = 0.5 * np.add(disc_source_loss, disc_target_loss)

                    self.after_train_discriminator()

                # ------------------
                #  Train Generators
                # ------------------

                gen_loss = self.combined.train_on_batch(
                    [imgs_source, imgs_target],
                    [
                        valid,
                        valid,
                        class_source,
                        class_target,
                        labels_source,
                        imgs_source,
                        imgs_target,
                        imgs_source,
                        imgs_target,
                    ],
                )

                elapsed_time = datetime.now() - start_time
                # Plot the progress
                if batch_i % 10 == 0:
                    progress_str = (
                        f"[Epoch: {epoch}/{epochs}] [Batch: {batch_i}] [D_loss: {disc_loss[0]:.5f}, acc: {100 * disc_loss[1]:.5f}] "
                        f"[G_loss: {gen_loss[0]:.5f}, generator_N: {gen_loss[1]:.5f}, generator_P: {gen_loss[2]:.5f} "
                        f"source_classifier_N: {gen_loss[3]:.5f}, source_classifier_P: {gen_loss[4]:.5f} "
                        f"classifier_cycled: {gen_loss[5]:.5f} "
                        f"reconstruction: {np.mean(gen_loss[6:8]):.5f} "
                        f"identity: {np.mean(gen_loss[8:10]):.5f}] "
                        f"time: {elapsed_time}"
                    )
                    print(progress_str)

                    if log_callback is not None:
                        log_callback(
                            {"Epoch": epoch,
                             "D_loss": disc_loss[0],
                             "acc": 100 * disc_loss[1],
                             "G_loss": gen_loss[0], "generator_N": gen_loss[1], "generator_P": gen_loss[2],
                             "source_classifier_N": gen_loss[3], "source_classifier_P": gen_loss[4],
                             "classifier_cycled": gen_loss[5],
                             "reconstruction": np.mean(gen_loss[6:8]),
                             "identity": np.mean(gen_loss[8:10])
                             }
                        )

                # If at save interval => save generated image samples
                if image_dir is not None and batch_i % 100 == 0:
                    self.sample_images(image_dir, epoch, batch_i, imgs_source[0], imgs_target[0],
                                       image_callback=image_callback)

        pass

    def sample_images(self, image_dir, epoch, batch_i, testN, testP, image_callback=None):

        image_dir = Path(image_dir)

        r, c = 2, 3

        img_N = testN[np.newaxis, :, :, :]
        img_P = testP[np.newaxis, :, :, :]

        # Translate images to the other domain
        fake_P = self.g_target.predict(img_N)
        fake_N = self.g_source.predict(img_P)
        # Translate back to original domain
        reconstr_N = self.g_source.predict(fake_P)
        reconstr_P = self.g_target.predict(fake_N)

        if image_callback is not None:
            image_callback({
                "img_N": img_N,
                "img_P": img_P,
                "fake_N": fake_N,
                "fake_P": fake_P,
                "reconstr_N": reconstr_N,
                "reconstr_P": reconstr_P
            })

        imgs = [img_N, fake_P, reconstr_N, img_P, fake_N, reconstr_P]
        gen_imgs = np.concatenate(imgs)

        fig, axs = plt.subplots(r, c, figsize=(15, 10))
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i, j].imshow(gen_imgs[cnt][:, :, :])
                axs[i, j].axis("off")
                cnt += 1

        image_dir.mkdir(exist_ok=True)
        img_name = str(image_dir / f"{epoch}_{batch_i}.png")
        fig.savefig(img_name)
        plt.close()

    # hook for wasserstein-gan weight normalization
    def after_train_discriminator(self):
        if not self.use_wasserstein:
            return

        for layer in self.d_source.layers:
            weights = layer.get_weights()
            weights = [np.clip(w, -self.clip_value, self.clip_value) for w in weights]
            layer.set_weights(weights)
        for layer in self.d_target.layers:
            weights = layer.get_weights()
            weights = [np.clip(w, -self.clip_value, self.clip_value) for w in weights]
            layer.set_weights(weights)

    def _build_model(self):
        # build classifier if necessary
        if not self._premade_classifier:
            self.classifier = build_classifier(self.img_shape, 6, "classifier")
            opt_classifier = keras.optimizers.Adam(self.lr_classifier, 0.5)
            self.classifier.compile(
                optimizer=opt_classifier,
                loss="sparse_categorical_crossentropy",
                metrics="accuracy"
            )

        # build source classifier
        self.source_classifier = build_classifier(self.img_shape, 1, "source_classifier")
        opt_src_classifier = keras.optimizers.Adam(self.lr_src_classifier, 0.5)
        self.source_classifier.compile(
            optimizer=opt_src_classifier,
            loss="binary_crossentropy",
            metrics="accuracy"
        )

        # Build the discriminators
        self.d_source = build_discriminator(self.img_shape, self.df, normalize=not self.use_wasserstein)
        self.d_target = build_discriminator(self.img_shape, self.df, normalize=not self.use_wasserstein)

        # Build the generators
        self.g_target = build_generator(self.img_shape, self.gf, self.channels)
        self.g_source = build_generator(self.img_shape, self.gf, self.channels)

        optimizer_disc = keras.optimizers.Adam(self.lr_discriminator, 0.5)

        def wasserstein_loss(y_true, y_pred):
            return tf.math.reduce_mean(y_true * y_pred)

        disc_loss = wasserstein_loss if self.use_wasserstein else "binary_crossentropy"
        self.d_source.compile(loss=disc_loss, optimizer=optimizer_disc, metrics=["accuracy"])
        self.d_target.compile(loss=disc_loss, optimizer=optimizer_disc, metrics=["accuracy"])

        # Input images from both domains
        img_source = keras.Input(shape=self.img_shape)
        img_target = keras.Input(shape=self.img_shape)

        # Translate images to the other domain
        fake_target = self.g_target(img_source)
        fake_source = self.g_source(img_target)
        # Translate images back to original domain
        reconstructed_source = self.g_source(fake_target)
        reconstructed_target = self.g_target(fake_source)
        # Identity mapping of images
        identity_source = self.g_source(img_source)
        identity_target = self.g_target(img_target)

        # For the combined model we will only train the generators
        self.d_source.trainable = False
        self.d_target.trainable = False
        self.classifier.trainable = False
        self.source_classifier.trainable = False

        # Discriminators determines validity of translated images
        validity_source = self.d_source(fake_source)
        validity_target = self.d_target(fake_target)

        class_reconstructed = self.classifier(reconstructed_source)
        source_class_source = self.source_classifier(fake_source)
        source_class_target = self.source_classifier(fake_target)

        # Combined model trains generators to fool discriminators
        self.combined = keras.Model(
            inputs=[img_source, img_target],
            outputs=[
                validity_source,
                validity_target,

                source_class_source,
                source_class_target,

                class_reconstructed,

                reconstructed_source,
                reconstructed_target,
                identity_source,
                identity_target,
            ],
        )

        optimizer_gen = keras.optimizers.Adam(self.lr_generator, 0.5)

        losses = [
            "binary_crossentropy" if not self.use_wasserstein else wasserstein_loss,
            "binary_crossentropy" if not self.use_wasserstein else wasserstein_loss,
            "binary_crossentropy",
            "binary_crossentropy",
            "sparse_categorical_crossentropy",
            "mae",
            "mae",
            "mae",
            "mae"
        ]

        self.combined.compile(
            loss=losses,
            loss_weights=[
                self.lambda_discriminator,
                self.lambda_discriminator,
                self.lambda_source_classifier,
                self.lambda_source_classifier,
                self.lambda_classifier,
                self.lambda_cycle,
                self.lambda_cycle,
                self.lambda_identity,
                self.lambda_identity,
            ],
            optimizer=optimizer_gen,
        )

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        pass

    def _info(self):
        pass

    def save(self, model_dir: str):

        model_dir = Path(model_dir)

        # Save discriminators to disk
        self.d_source.save(model_dir / "discriminator_source.h5")
        self.d_target.save(model_dir / "discriminator_target.h5")

        # Save generators to disk
        self.g_target.save(model_dir / "generator_target.h5")
        self.g_source.save(model_dir / "generator_source.h5")

        # Save classifiers
        self.classifier.save(model_dir / "classifier.h5")
        self.source_classifier.save(model_dir / "source_classifier.h5")
