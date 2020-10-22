"""
@author: Ross Drucker
"""
import os
import shutil
import imageio

import bdb_helpers.lookup as find

def make_play_img_dir(gid, pid):
    desired_path = os.path.join('img', 'temp', f'{gid}_{pid}')
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    
    return None

def collect_play_frames(gid, pid):
    desired_path = os.path.join('img', 'temp', f'{gid}_{pid}')
    files = [file for file in os.listdir(desired_path) if file.endswith('png')]
    files.sort()
    imgs = [imageio.imread(os.path.join(desired_path, file)) for file in files]
    
    return imgs

def make_gif(gid, pid, images):
    home, away = find.game_teams(gid)
    output_path = os.path.join('img', 'gif', f'{gid}_{home}_{away}')
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    imageio.mimwrite(
        os.path.join(output_path, f'{pid}.gif'),
        images
    )
    
    return None

def remove_static_frame_directory(gid, pid):
    shutil.rmtree(os.path.join('img', 'temp'))
    
    return None