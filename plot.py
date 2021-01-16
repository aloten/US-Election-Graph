"""
Aidan Loten
12/10/2020
"""
from PIL import Image, ImageDraw
from PIL.ImageColor import getrgb


class Plot:

    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x1 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        return int((x_1 - x_2) / (x_3 - x_2) * newlength)

    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        return int((height / width) * new_width)

    @staticmethod
    def fill(region, style):
        """return the fill color for region according to the given 'style'"""
        if style == "GRAD":
            return Plot.gradient(region)
        else:
            return Plot.solid(region)

    @staticmethod
    def solid(region):
        """
        a solid color based on a region's plurality of votes
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple (RGB values between 0 and 255)
        """
        if region.plurality() == "REPUBLICAN":
            return getrgb("RED")
        elif region.plurality() == "DEMOCRAT":
            return getrgb("BLUE")
        else:
            return getrgb("GREEN")
    @staticmethod
    def gradient(region):
        """
        a gradient color based on percentages of votes in a region
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple (RGB values between 0 and 255)
        Currently thinking of applying a weight based on a min of 64 votes in a region and a max of 2,652,072, but don't have time before submission of assignment
        """
        return (int(255 * region.republican_percentage()), int(255 * region.other_percentage()), int(255 * region.democrat_percentage()))

    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """
        self.height = self.proportional_height(width, max_long - min_long, max_lat - min_lat)
        self.im = Image.new("RGB", (width, self.height), (255, 255, 255))
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat
        self.width = width
        
    def save(self, filename):
        """save the current image to 'filename'"""
        self.im.save(filename, "PNG")

    def draw(self, region, style):
        """
        Draws 'region' in the given 'style' at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
            style (str): 'GRAD' or 'SOLID' to determine the polygon's fill
        """
        
        def trans_long(long):
            '''interpolate a longitude value'''
            result = self.interpolate(long, self.min_long, self.max_long, self.width)
            return result
        inter_longs = [trans_long(long) for long in region.longs()]
        
        def trans_lat(lat):
            '''interpolate a latitude value and subtract from height to account for (0,0) being top left of image'''
            result = self.height - self.interpolate(lat, self.min_lat, self.max_lat, self.height)
            return result
        inter_lats = [trans_lat(lat) for lat in region.lats()]
            
        '''combine longs and lats into [x,y,x,y,...] coordinates list'''    
        coordinates = []
        for long, lat in zip(inter_longs, inter_lats):
            coordinates.append(long)
            coordinates.append(lat)        
        
        
        ImageDraw.Draw(self.im).polygon(coordinates, Plot.fill(region, style), outline=None)
