# I referenced the GitHub repository of the paper, https://arxiv.org/pdf/2310.05146.pdf, https://github.com/tanchongmin/ARC-Challenge/.

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def load_json_data(folder):
    json_files = [pos_json for pos_json in os.listdir(folder) if pos_json.endswith('.json')]
    data = {}
    for js in json_files:
        with open(os.path.join(folder, js)) as json_file:
            data[js] = json.load(json_file)
    return data


def array_to_string(grid):
    # if grid is already in string form, just return it
    if isinstance(grid[0][0], str): return grid

    mapping = {0:'.',1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i'}
    newgrid = [[mapping[grid[i][j]] for j in range(len(grid[0]))] for i in range(len(grid))]
    return newgrid

def string_to_array(grid):
    # if grid is already in integer form, just return it
    if isinstance(grid[0][0], int): return grid

    mapping = {0:'.',1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i'}
    revmap = {v:k for k,v in mapping.items()}
    newgrid = [[revmap[grid[i][j]] for j in range(len(grid[0]))] for i in range(len(grid))]
    return newgrid

def plot_2d_grid(data, file_name):
    
    cvals  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    colors = ["#000000", "#0074D9", "#FF4136", "#2ECC40", "#FFDC00", "#AAAAAA", "#F012BE", "#FF851B", "#7FDBFF", "#870C25"]
    norm=plt.Normalize(min(cvals),max(cvals))
    tuples = list(zip(map(norm,cvals), colors))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)

    
    output_folder = 'training_IO_pair_image'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    fig, axs = plt.subplots(len(data['train']), 2, figsize=(4, len(data['train']) * 3 * 0.8))
    axs = axs.reshape(-1, 2)  # Reshape axs to have 2 dimensions
    for i, example in enumerate(data['train']):
        axs[i, 0].set_title(f'Training Input {i+1}')
        # display gridlines
        rows, cols = np.array(string_to_array(example['input'])).shape
        axs[i, 0].set_xticks(np.arange(cols + 1) - 0.5, minor=True)
        axs[i, 0].set_yticks(np.arange(rows + 1) - 0.5, minor=True)
        axs[i, 0].tick_params(which='minor', size=0)
        axs[i, 0].grid(True, which='minor', color='#555555', linewidth=0.5)
        axs[i, 0].set_xticks([]); axs[i, 0].set_yticks([])
        axs[i, 0].imshow(np.array(string_to_array(example['input'])), cmap=cmap, vmin=0, vmax=9)
        
        axs[i, 1].set_title(f'Training Output {i+1}')
        # display gridlines
        rows, cols = np.array(string_to_array(example['output'])).shape
        axs[i, 1].set_xticks(np.arange(cols + 1) - 0.5, minor=True)
        axs[i, 1].set_yticks(np.arange(rows + 1) - 0.5, minor=True)
        axs[i, 1].tick_params(which='minor', size=0)
        axs[i, 1].grid(True, which='minor', color='#555555', linewidth=0.5)
        axs[i, 1].set_xticks([]); axs[i, 1].set_yticks([])
        axs[i, 1].imshow(np.array(string_to_array(example['output'])), cmap=cmap, vmin=0, vmax=9)
        
        case_file_name = f"{os.path.splitext(file_name)[0]}.png"
        output_file_path = os.path.join(output_folder, case_file_name)

        plt.tight_layout()
        plt.savefig(output_file_path, format='png', dpi=300)
        
    
    plt.close()
    
    
# load the json files
folder = 'original_data/training'
myjson_train = load_json_data(folder)
file_names_train = list(myjson_train.keys())

# Load the task mapping from the CSV file
csv_file = 'original_data/filtered_LARC_with_input_output.csv'

# Generate and save the images
for i in range(0, 400):
    file_name_str = file_names_train[i]
    plot_2d_grid(myjson_train[file_name_str], file_name_str)
