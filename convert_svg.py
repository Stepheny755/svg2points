from svg.path import parse_path
from xml.dom import minidom

import numpy as np

import argparse
import sys
import os


parser = argparse.ArgumentParser(description="Converts SVG file into 2D (x,y) Points")
parser.add_argument("-f", "--file", help="SVG file to add", required=True)
parser.add_argument("-o", "--output", help="Output file name", default="points.csv")
parser.add_argument("--density", help="Density of SVG points", default=1)
parser.add_argument("--scale", help="Scale of the image", default=5)
parser.add_argument("--x_offset", help="x offset for SVG points", default=0)
parser.add_argument("--y_offset", help="y offset for SVG points", default=0)
args = parser.parse_args()


def get_point_at(path, distance, scale, offset):
    pos = path.point(distance)
    pos += offset
    pos *= scale
    return pos.real, pos.imag


def points_from_path(path, density, scale, offset):
    step = int(path.length() * density)
    last_step = step - 1

    if last_step == 0:
        yield get_point_at(path, 0, scale, offset)
        return

    for distance in range(step):
        yield get_point_at(path, distance / last_step, scale, offset)


def points_from_doc(doc, density=5, scale=1, offset=0):
    offset = offset[0] + offset[1] * 1j
    points = []
    for element in doc.getElementsByTagName("path"):
        for path in parse_path(element.getAttribute("d")):
            points.extend(points_from_path(path, density, scale, offset))

    return points


# open svg file
if not os.path.exists(args.file):
    print(f"Error: could not find file {args.file}")
    sys.exit()
with open(args.file, "r") as file:
    data = file.read().replace("\n", "")

# parse svg path into xy points
doc = minidom.parseString(data)
points = points_from_doc(
    doc,
    density=args.density,
    scale=args.scale,
    offset=(args.x_offset, args.y_offset),
)
doc.unlink()

# save to csv
points = np.array(points)
np.savetxt(args.output, points, delimiter=",", fmt="%s")
