import os
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi']=200
import numpy as np
import imageio
from dataclasses import dataclass

@dataclass
class Bound2D:
    """Class for keeping track of an item in inventory."""
    xmin: float = 0
    xmax: float = 1
    ymin: float = 0
    ymax: float = 1
    xlabel: str = "x"
    ylabel: str = "y"

def plot4d_CS(func, z_plot, z_label='z', bound2D=Bound2D(), wbounds=None, color_num=21, path=None, func_name=None):
    """Plot a 4D function w(x,y,z) at z=z_plot with a countour plot.

    Args:
        func: function to plot
        bound2D: Class Bound2D object.
        wbounds: bounds on the w axis (color dimension). If not provided with be auto fitted.
        color_num: Number of colors to be used for countour plot. Defaults to 21.
        path: Path to save the generated plot. Defaults to None.
        func_name: Name to be displayed in the title of the plot

    Returns:
        None
    """
    xmin, xmax = bound2D.xmin, bound2D.xmax
    ymin, ymax = bound2D.ymin, bound2D.ymax
    x = np.linspace(xmin, xmax, color_num)
    y = np.linspace(ymin, ymax, color_num)
    w = np.array([func(i,j,z_plot) for j in y for i in x])

    X, Y = np.meshgrid(x, y)
    W = w.reshape(color_num, color_num)
    
    if wbounds == None:
        wbounds = (W.min(), W.max())
    wmin, wmax = wbounds
    levels = np.linspace(wmin, wmax, color_num)
    img=plt.contourf(X, Y, W, levels=levels)
    plt.colorbar(img)
    
    plt.xlabel(bound2D.xlabel)
    plt.ylabel(bound2D.ylabel)
    if func_name == None:
        func_name = "Crosssection"
    title_str = "%s at %s=%.2f"%(func_name, z_label, z_plot)
    plt.title(title_str)
    
    if path == None:
        save_path = "Figures/"
    else:
        save_path = path
        save_path += '/' if path[-1]!= '/' else ''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    filename = save_path + title_str + ".png"
    plt.savefig(filename)
    
    plt.show() if path==None else plt.close()
    return filename

def plot4d(func, z_values, wbounds=None, path=None, func_name=None, z_label='z', save_images=True, color_num = 21, bound2D=Bound2D(), fps=1):
    """Plot a 4D function w(x,y,z) by crosssections and create a gif for it. 

    Args:
        func (function): Function to plot.
        z_values (interable): Values of z at cross sections we want to plot at.
        path (str, optional): Path for generated images. Default to None. 
        wbounds (tuple, optional): Color bar range. Should be set at all times to prevent color bars auto-adjusting frame to frame. 
        func_name (str, optional): Name of the 4D function we are plotting. 
        z_label (str, optional): Label on the z axis. Defaults to 'z'.
        save_images (bool, optional): If true then save the cross section png files. Defaults to True.
        fps (int, optional): Frames per second used in gif. Defaults to 1.

    Returns:
        _type_: _description_
    """    
    if path==None:
        path = os.getcwd() + "/temp"
    filenames = []
    for z in z_values:
        fn = plot4d_CS(func, z, func_name=func_name, z_label=z_label, wbounds=wbounds, color_num=color_num, path=path, bound2D=bound2D)
        filenames.append(fn)
    
    gif_name = "Cross Sections" if func_name==None else func_name
    gif_name += ".gif"
    with imageio.get_writer(gif_name, mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            if not save_images:
                os.remove(filename)

    # remove path if folder is empty
    if not list(os.walk(path))[1:]:
        os.rmdir(path)
    return gif_name