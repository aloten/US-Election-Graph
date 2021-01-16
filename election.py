import sys
import csv
import math
from region import Region
from plot import Plot

def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def main(results, boundaries, output, width, style):

    def to_point(coords):
        return [(float(coords[2*i]), mercator(float(coords[2*i+1])))
                 for i in range(len(coords)//2)]

    with open(results) as results_fp, open(boundaries) as boundaries_fp:
        regions = [Region(to_point(boundary[2:]), int(r), int(d), int(o))
                   for (co,st,r,d,o), boundary in zip(csv.reader(results_fp),
                                                      csv.reader(boundaries_fp))]

    min_long = min([r.min_long() for r in regions])
    max_long = max([r.max_long() for r in regions])
    min_lat = min([r.min_lat() for r in regions])
    max_lat = max([r.max_lat() for r in regions])
    min_votes = min([r.total_votes() for r in regions])
    max_votes = max([r.total_votes() for r in regions])
    print(min_long, max_long, min_lat, max_lat)
   

    p = Plot(width, min_long, min_lat, max_long, max_lat)

    for region in regions:
        p.draw(region,style)

    p.save(output)

if __name__ == '__main__':
    results = sys.argv[1]
    boundaries = sys.argv[2]
    output = sys.argv[3]
    width = int(sys.argv[4])
    style = sys.argv[5]
    main(results, boundaries, output, width, style)
