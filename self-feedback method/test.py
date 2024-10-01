import os
import csv
import pandas as pd
import random
import base64
from mimetypes import guess_type
from openai import AzureOpenAI
from utils import local_image_to_data_url, select_random_images_and_convert_to_data_urls, select_constraints, log_wrong_format_error, log_openai_error, shuffle_responses_in_csv

# shuffle csv
directory = "C:/Users/oollccddss/Desktop/Work/MC-LARC/MC-LARC-EMNLP.ver/student-teacher model/results/initial_MC-LARC"
shuffle_responses_in_csv(directory)