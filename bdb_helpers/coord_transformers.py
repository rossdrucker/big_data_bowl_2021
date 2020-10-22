"""
@author: Ross Drucker
"""
def convert_trans(df, start = 'ft', trans = True, x_tran = 60, y_tran = 80/3):
    """
    Convert the units from feet to yards (or feet to yards), and translate
    to accomodate the desired origin of field coordinates
    
    Parameters
    ----------
    df: a dataframe to convert from starting units to ending units
    start: a string stating the starting units. Default is 'ft'
    trans: a bool of whether or not to translate the field. Default is True
    x_tran: how much to translate x by in NEW units. Default is 0
    y_tran: how much to translate y by in NEW units. Default is 0

    Returns
    -------
    df : the original dataframe, converted and translated
    """
    # If the starting unit is in feet, divide it by 3 to convert units to yards
    if start == 'ft':
        df['x'] = df['x'] / 3
        df['y'] = df['y'] / 3
    
    # Otherwise, multiply by 3 to convert from yards to feet
    else:
        df['x'] = df['x'] * 3
        df['y'] = df['y'] * 3
    
    # If the coordinates need to be translated, apply the translation
    if trans:
        df['x'] = df['x'] + x_tran
        df['y'] = df['y'] + y_tran
    
    return df
