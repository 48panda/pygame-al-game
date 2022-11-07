from colorsys import rgb_to_hls, hls_to_rgb
import pygame 
import pygame.gfxdraw

def draw_circle(surface, x, y, radius, color):
     pygame.gfxdraw.aacircle(surface, x, y, radius, color)
     pygame.gfxdraw.filled_circle(surface, x, y, radius, color)

def draw_rounded_rect(surface, rect, color, corner_radius):
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners

    draw_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    draw_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    draw_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    draw_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)
    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

def adjust_color(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))
    
def lighten_color(r, g, b, factor=0.1):
    return adjust_color(r, g, b, 1 + factor)
    
def darken_color(r, g, b, factor=0.1):
    return adjust_color(r, g, b, 1 - factor)