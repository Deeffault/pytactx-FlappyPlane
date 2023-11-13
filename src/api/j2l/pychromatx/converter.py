# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__libdir__ = os.path.dirname(__workdir__)
sys.path.append(__libdir__)

import pyanalytx.logger as anx

def colorFromPercent(percent:float):
    LED_MAGENTA_THRESHOLD = 300.0/360.0
    LED_BLUE_THRESHOLD = 240.0/360.0
    LED_CYAN_THRESHOLD = 180.0/360.0
    LED_GREEN_THRESHOLD = 90.0/360.0
    LED_YELLOW_THRESHOLD = 60/360.0
    LED_RED_THRESHOLD = 0.0/360.0
    if ( percent < 0.0 ):
        percent = 0.0
    r = 0
    g = 0
    b = 0
    if ( percent <= LED_RED_THRESHOLD ):
        r = 255
    elif ( percent <= LED_YELLOW_THRESHOLD ):
        r = 255
        g = int(255.0 * (percent - LED_RED_THRESHOLD)  / (LED_YELLOW_THRESHOLD-LED_RED_THRESHOLD))
    elif ( percent <= LED_GREEN_THRESHOLD ):
        r = int(255.0 - 255.0 * (percent - LED_YELLOW_THRESHOLD)  / (LED_GREEN_THRESHOLD-LED_YELLOW_THRESHOLD))
        g = 255
    elif ( percent <= LED_CYAN_THRESHOLD ):
        b = int(255.0 * (percent - LED_GREEN_THRESHOLD)  / (LED_CYAN_THRESHOLD-LED_GREEN_THRESHOLD))
        g = 255
    elif ( percent <= LED_BLUE_THRESHOLD ):
        b = 255
        g = int(255.0 - 255.0 * (percent - LED_CYAN_THRESHOLD)  / (LED_BLUE_THRESHOLD-LED_CYAN_THRESHOLD))
    elif ( percent <= LED_MAGENTA_THRESHOLD ):
        b = 255
        r = int(255.0 * (percent - LED_BLUE_THRESHOLD)  / (LED_MAGENTA_THRESHOLD-LED_BLUE_THRESHOLD))
    else:
        r = 255
        b = int(255.0 - 255.0 * (percent - LED_MAGENTA_THRESHOLD)  / (1.0-LED_MAGENTA_THRESHOLD))
    return (r,g,b)

def RGBToHSL(r,g,b): 
    # Make r, g, and b fractions of 1
    r /= 255
    g /= 255
    b /= 255
    # Find greatest and smallest channel values
    cmin = min(r,g,b)
    cmax = max(r,g,b)
    delta = cmax - cmin
    h = 0
    s = 0
    l = 0
    # Calculate hue
    # No difference
    if (delta == 0):
        h = 0
    # Red is max
    elif (cmax == r):
        h = ((g - b) / delta) % 6
    # Green is max
    elif (cmax == g):
        h = (b - r) / delta + 2
    # Blue is max
    else:
        h = (r - g) / delta + 4
    h = int(h * 60)
    # Make negative hues positive behind 360°
    if (h < 0):
        h += 360
    # Calculate lightness
    l = (cmax + cmin) / 2
    # Calculate saturation
    if ( delta == 0 ):
        s = 0 
    else:
        s = delta / (1 - abs(2 * l - 1))
    # Multiply l and s by 100
    s = int(s * 100)
    if ( s > 100 ):
        s = 100
    l = int(l * 100)
    if ( l > 100 ):
        l = 100
    return (h,s,l)

def HSLToRGB(h,s,l):
    # Must be fractions of 1
    s /= 100.0
    l /= 100.0
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r = 0
    g = 0
    b = 0
    if (0 <= h and h < 60):
        r = c
        g = x
        b = 0
    elif (60 <= h and h < 120):
        r = x
        g = c
        b = 0
    elif (120 <= h and h < 180):
        r = 0
        g = c
        b = x
    elif (180 <= h and h < 240):
        r = 0
        g = x
        b = c
    elif (240 <= h and h < 300):
        r = x
        g = 0
        b = c
    elif (300 <= h and h < 360):
        r = c
        g = 0
        b = x
    r = int((r + m) * 255)
    if ( r > 255 ):
        r = 255
        g = int((g + m) * 255)
    if ( g > 255 ):
        g = 255
        b = int((b + m) * 255)
    if ( b > 255 ):
        b = 255
    return (r,g,b)

if __name__ == '__main__':
    anx.warning("⚠️ Nothing to run from lib "+str(__file__))