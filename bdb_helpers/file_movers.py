"""
@author: Ross Drucker
"""
import os
import shutil
import imageio

import bdb_filepaths as fp
import bdb_helpers.lookup as find

def make_gif_temp_dir(gid, pid):
    """
    Make a temporary directory for the static files of a play while making a
    gif

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    None.
    """
    # Make the desired path
    desired_path = os.path.join(fp.img_dir, 'temp', f'{gid}_{pid}')
    
    # Check if the path exists. If not, create one
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    
    return None

def collect_gif_play_frames(gid, pid):
    """
    Collects the files needed to make a gif

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    imgs: a list of images ready to be made into a gif
    """
    # Find the desired path with static images
    desired_path = os.path.join(fp.img_dir, 'temp', f'{gid}_{pid}')
    
    # Go through the directory and select only the .png files for the gif
    files = [file for file in os.listdir(desired_path) if file.endswith('png')]
    
    # Reorder since the files may be read out of order, but their order is
    # known and matters
    files.sort()
    
    # Read in the actual image files
    imgs = [imageio.imread(os.path.join(desired_path, file)) for file in files]
    
    return imgs

def make_gif(gid, pid, images, fname = ''):
    """
    Make and save the actual gif to the img/gif/{game_id} folder

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    images: a list of images to convert to a gif

    Returns
    -------
    None.
    """
    # Get the home and away team for subdirectory naming
    home, away = find.game_teams(gid)
    
    # Make the desired saving path
    output_path = os.path.join(fp.gif_dir, f'{gid}_{home}_{away}')
    
    # Check if the folder for this game's gifs already exists. If not, make it
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Save the gif
    if fname == '':
        fname = f'{pid}.gif'
        
    if fname[-4:] != '.gif':
        fname = f'{fname}.gif'
        
    try:  
        imageio.mimwrite(
            os.path.join(output_path, fname),
            images
        )
    except:
        imageio.mimwrite(
            os.path.join(output_path, f'{pid}.gif'),
            images
        )
    
    return None

def remove_temp_static_frame_directory(gid, pid):
    """
    Remove the temporary directory with the static files

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    None.
    """
    # Remove the temporary directory
    shutil.rmtree(os.path.join('img', 'temp'))
    
    return None