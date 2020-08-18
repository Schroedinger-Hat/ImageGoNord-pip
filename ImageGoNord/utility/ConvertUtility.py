# -*- coding: utf-8 -*-

class ConvertUtility:
  """
  An utility class used for converting image to the nord palette

  Methods
  -------
  color_difference(color1, color2)
    Find the color difference between the two given colors

  get_avg_color(pixels, row, col, w, h)
    Get the avg color of a given area and return it as tuple containing rgb
  """

  def color_difference(color1, color2):
    """
    Find the color difference between the two given colors

    Parameters
    ----------
    color1 : tuple
        color in rgb
    color2 : tuple
        color in rgb

    Returns
    -------
    tuple
      the resultant color
    """
    return sum([abs(component1-component2) for component1, component2 in zip(color1, color2)])

  def get_avg_color(pixels, row, col, w=-2, h=3):
    """
    Get the avg color of a given area and return it as tuple containing rgb

    Parameters
    ----------
    pixels : dict
      The pixel map of the source image
    row : int
      Row counter where to start
    col : int
      Col counter where to start
    w : int
      Box's wdith
    h : int
      Box's height

    Returns
    -------
    tuple
      the resultant color in rgb format
    """
    average_sum = []
    for k in range(w, h):
      for l in range(w, h):
        try:
          average_sum.append(pixels[row+k, col+l])
        except:
          pass

    size = len(average_sum)
    if (size <= 0):
      size = 1

    r = 0
    g = 0
    b = 0
    a = 255
    for x in average_sum:
      r += x[0]
      g += x[1]
      b += x[2]
      if (len(x) > 3):
        a += x[3]

    avg_color = (int(r/size), int(g/size), int(b/size))
    if (a != 255):
      avg_color = avg_color + (int(a/size), )

    return avg_color
