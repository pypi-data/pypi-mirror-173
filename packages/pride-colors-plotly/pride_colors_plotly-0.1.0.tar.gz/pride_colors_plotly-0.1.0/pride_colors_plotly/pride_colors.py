import matplotlib
import plotly
import plotly.colors
import plotly.io as pio


def get_continuous_color(colorscale, intermed):
    """Compute intermediate
    colors for any value in the range [0,1] which PlotLy continuous colorscales are assigned to.

    Args:
        colorscale (): A plotly continuous colorscale defined with RGB string colors.
        intermed (float): Value in the range [0, 1]
    
    Returns:
        str: color in rgb string format
    """
    if len(colorscale) < 1:
        raise ValueError("colorscale must have at least one color")

    if intermed <= 0 or len(colorscale) == 1:
        return colorscale[0][1]
    if intermed >= 1:
        return colorscale[-1][1]

    for cutoff, color in colorscale:
        if intermed > cutoff:
            try:
                low_cutoff, low_color = cutoff, plotly.colors.label_rgb(plotly.colors.hex_to_rgb(color))
            except ValueError:
                low_cutoff, low_color = cutoff, plotly.colors.label_rgb(color)
                if low_color == 'rgb(r, g, b)': #if it's already rgb
                    low_color = color
        else:
            try:
                high_cutoff, high_color = cutoff, plotly.colors.label_rgb(plotly.colors.hex_to_rgb(color))
            except ValueError:
                high_cutoff, high_color = cutoff, plotly.colors.label_rgb(color)
                if high_color == 'rgb(r, g, b)':
                    high_color = color
            break

    # noinspection PyUnboundLocalVariable
    return plotly.colors.find_intermediate_color(
        lowcolor=low_color, highcolor=high_color,
        intermed=((intermed - low_cutoff) / (high_cutoff - low_cutoff)),
        colortype="rgb")
        

def get_flagcolors():
    """Hex code colors of various Pride flags: philadelphia, rainbow, bi, trans, asexual, aromantic, lesbian_new, pan
    Args:
    
    Returns:
        dict: Dictionary of hex code colors used in Pride flags"""
    flagcolors={}
    flagcolors['bi']=["#ff0080","#a349a4","#0000ff"]
    flagcolors['philadelphia']=['#FF0018','#FFA52C','#FFFF41','#008018','#0000F9','#86007D','#784F17','#000000']
    flagcolors['rainbow']=['#FF0018','#FFA52C','#FFFF41','#008018','#0000F9','#86007D']
    flagcolors['trans']=['#55CDFC','#FFFFFF','#F7A8B8']
    flagcolors['asexual']=['#000000', '#A4A4A4', '#FFFFFF','#810081']
    flagcolors['aromantic']=['#000000','#339933','#ffff66','#99cc66','#999999']
    flagcolors['lesbian_new']=['#D62900', '#FF9B55', '#FFFFFF', '#D461A6', '#A50062']
    flagcolors['pan']=['#FF1B8D','#FFDA00','#1BB3FF']
    return flagcolors
    
def set_pride_template(flag='philadelphia',plot_bg='lightgrey'):
    """Set color cycles for PlotLy and matplotlib using pride flag colors
    
    Args:
        flag (str, optional): Name of flag color sceme to use. Defaults to 'philadelphia'
        plot_bg (str, optional): Background color to use for PlotLy figure"""
    flagcolors=get_flagcolors()
    #plotly
    pio.templates["pride"] = plotly.graph_objects.layout.Template(layout_colorway=flagcolors[flag],layout_plot_bgcolor=plot_bg)
    pio.templates.default = "pride"
    #mpl
    matplotlib.rcParams['axes.prop_cycle']=matplotlib.cycler(color=flagcolors[flag])

def pride_colors_plotly(flag='philadelphia',continuous_colorscale=False,ncolors=256):
    """Get either a list of flag colors or a continuous colorscale of flag colors.
    
    Args:
        flag (str, optional): Name of flag color sceme to use. Defaults to 'philadelphia'
        continuous_colorscale (bool, optional): Return a PlotLy colorscale instead of a list of colors. Defaults to False.
        ncolors (int, optional): Number of discrete colors to interpolate. Defaults to 256
    
    Returns:
        list or colorscale: a list of flag colors or a continuous colorscale of flag colors.
        """
    flagcolors=get_flagcolors()
    if not continuous_colorscale:
        return flagcolors[flag] #discrete list
    else:
        colorscale = plotly.colors.make_colorscale(flagcolors[flag])
    return [get_continuous_color(colorscale, intermed=i/ncolors) for i in range(ncolors)][1:]
    
def pride_colors_matplotlib(flag='philadelphia'):
    """Get a matplotlib colormap using Pride flag colors
    
    Args:
        flag (str, optional): Name of flag color sceme to use. Defaults to 'philadelphia'
    Returns:
        matplotlib.colors.LinearSegmentedColormap: Colormap based on flag scheme."""
    flagcolors=get_flagcolors()
    return matplotlib.colors.LinearSegmentedColormap.from_list("", flagcolors[flag])
