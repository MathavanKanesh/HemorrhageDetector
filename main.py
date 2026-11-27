# From kaggle workspace 
# Imports
import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import os
from PIL import Image
from pathlib import Path
import pandas as pd
import pydicom
import torch.nn as nn
import torch.nn.functional as F


# Image path
image_path = "/kaggle/input/competitions/rsna-intracranial-hemorrhage-detection/rsna-intracranial-hemorrhage-detection/stage_2_train"

# Images
training_images_path = Path(image_path)
training_image_files = list(training_images_path.glob("*.dcm"))

print("Number of images:", len(training_image_files))


# Label path
training_label_path = "/kaggle/input/competitions/rsna-intracranial-hemorrhage-detection/rsna-intracranial-hemorrhage-detection/stage_2_train.csv"

# Load labels
training_labels = pd.read_csv(training_label_path)

training_labels = training_labels[
    training_labels["ID"].str.endswith("_any")
]

print(training_labels.shape)




# Load DINOv3
REPO_DIR = "/kaggle/working/dinov3"

checkpoint_path = "/kaggle/input/datasets/mk0928/dinov3weights/dinov3_vits16_pretrain_lvd1689m-08c60483.pth"

dinov3_vits16 = torch.hub.load(
    REPO_DIR,
    "dinov3_vits16",
    source="local",
    weights=str(checkpoint_path)
)

dinov3_vits16.eval()


# Initialize feature and label lists
imagefeatures = []
imagelabels = []


# Extract pretrained features
with torch.no_grad():  # Disable gradient calculations for baseline model evaluation

    for i in range(100):

        # Load DICOM image
        image = pydicom.dcmread(training_image_files[i])
        image_array = image.pixel_array

        # Resize image to 256 x 256
        resized_array = np.resize(image_array, (256, 256))

        # Convert grayscale image to RGB
        resized_array = np.stack([resized_array] * 3, axis=-1)

        # Convert image to PyTorch tensor
        image_tensor = torch.tensor(resized_array)
        image_tensor = image_tensor.float()

        # Normalize pixel values to range 0 to 1
        image_tensor /= 255.0

        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)

        # Rearrange dimensions to [batch, channels, height, width]
        image_tensor = image_tensor.permute(0, 3, 2, 1)

        # Pass image through DINOv3
        features = dinov3_vits16.forward_features(image_tensor)

        # Extract CLS token (384 features per image)
        cls_features = features["x_norm_clstoken"]

        # Find corresponding image label
        matching_row = training_labels[
            training_labels["ID"] == training_image_files[i].stem + "_any"
        ]

        label = matching_row["Label"].iloc[0]

        # Store features and corresponding label
        imagefeatures.append(cls_features)
        imagelabels.append(label)



# Combine 100 feature tensors into one tensor with shape [100, 384]
featurematrix = torch.cat(imagefeatures)

# Convert PyTorch tensor to NumPy array
featurematrix = featurematrix.numpy()

# Convert labels to NumPy array
labels = np.array(imagelabels)

print(labels.shape)
print(featurematrix.shape)


# Apply PCA to reduce 384 features to 2 dimensions
