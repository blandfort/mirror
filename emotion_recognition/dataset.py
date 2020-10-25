import os
import numpy as np
from PIL import Image
from torchvision.datasets.vision import VisionDataset


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


class FERPlus(VisionDataset):
    """`FERPlus <https://github.com/microsoft/FERPlus>`_ Dataset"""

    training_dir = 'FER2013Train'
    test_dir = 'FER2013Valid'
    classes = ('neutral', 'happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear', 'contempt', 'unknown', 'NF')

    def __init__(self, root, loader=pil_loader, train=True, transform=None, target_transform=None):
        super(FERPlus, self).__init__(root, transform=transform, target_transform=target_transform)
        self.loader = loader
        self.train = train

        if not self._check_exists():
            raise RuntimeError('Dataset not found.')

        if self.train:
            data_dir = os.path.join(self.root, self.training_dir)
        else:
            data_dir = os.path.join(self.root, self.test_dir)
        self.data = []
        self.targets = []

        # Read the labels
        labels = {}  # image_name: class
        with open(os.path.join(data_dir, 'label.csv')) as f:
            for line in f:
                img_name = line.split(',')[0]
                annotations = line.rstrip().split(',')[-10:]

                # Using majority voting mode to identify label
                labels[img_name] = np.argmax(annotations)

        #TODO since the dataset is small, could also load everything into working memory for faster processing
        for img_name, label in labels.items():
            img_path = os.path.join(data_dir, img_name)

            if os.path.isfile(img_path):
                self.data.append(img_path)
                self.targets.append(label)

        print("Read %d images."%len(self.data))

    def _check_exists(self):
        return (os.path.exists(os.path.join(self.root,
                                            self.training_dir)) and
                os.path.exists(os.path.join(self.root,
                                            self.test_dir)))

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        path, target = self.data[index], self.targets[index]

        img = self.loader(path)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.data)
