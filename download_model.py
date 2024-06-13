# Use a pipeline as a high-level helper
from transformers import pipeline

pipeline("image-classification", model="Falconsai/nsfw_image_detection")
