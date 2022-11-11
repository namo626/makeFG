import numpy as np
import sys
import argparse

template = """FOR BEST RESULTS, PLEASE KEEP COMMENTS OUT OF THE FIRST 50 CHARACTERS ON EACH LINE.
12345678901234567890123456789012345678901234567890
4                                                  ! Level of screen output.
                                                  ! Path where GMT executables are located.
                                                  ! Path where GhostScript executable is located.
Temp/                                              ! Path where temporary files will be created.
adcirc                                             ! Alphanumeric label for these plots.
1,ADCIRC                                            ! Plot label flag and plot label.
1                                                  ! Time bar flag: 0 to ignore, 1 to plot time bar.
 -360.25                                            ! Lat/lon box.
 -358.5                                           !
 -0.25                                               !
 1.5                                               !
fort.14                                            ! Name of grid file.
1                                                  ! Plot grid flag: 0 to ignore, 1 to plot triangular grid on figure.
PARAMETERS FOR CONTOURS:
1                                                  ! Contour fill flag: 0 to ignore, 1 to plot filled contours, 2 to plot differences.
0                                                  ! Contour lines flag: 0 to ignore, 1 to plot contour lines, 2 to plot differences.
maxele.63                                            ! Name(s) of file(s) to use for contours.
ADCIRC-OUTPUT                                      ! Contour file format flag: ADCIRC-OUTPUT, GRID-BATH/SIZE/DECOMP-#, 13-MANNING/CANOPY/TAU0/EVIS/WIND-REDUCTION(-#).
1.00000                                            ! Unit conversion factor for contours.
m                                                  ! Alphanumeric label for units after conversion.
SMS                                                ! Color palette flag: RGB, SMS(+INTERVALS), CPT(+INTERVALS).
Default2.pal                                       ! Name of SMS color palette.
DEFAULT                                            ! Color lines flag: DEFAULT, CONTOUR-LINES, GRID-BATH/SIZE/DECOMP-#.  Requires GMT4.3.0.
0.0,1.0                                               ! Minimum,maximum in contour range (or FIND to determine from file).
0.25                                               ! Interval in contour range.
100                                                ! Number of times to split contour interval (for smoother plots).
1                                                  ! Label every xth contour line on the plot (or 0 for no labels).
0.5                                                ! Require contour line labels to be more than x inches apart.
0                                                  ! Rotation angle for contour line labels (or n for normal or p for parallel.)
8                                                  ! Font size for contour line labels.
1.0                                                ! Label the scale at intervals of x.
0.25                                               ! Width (inches) of scale.
PARAMETERS FOR PARTICLES:
0                                                  ! Particle flag: 0 to ignore, N to plot every Nth particle in the file.
pth.201006290000.nc                                ! Name of path file to use for particles (*.pth).
1,0,Brown                                          ! Particle size (pixels), pattern and color.
PARAMETERS FOR VECTORS:
0                                                  ! Vector flag: 0 to ignore, 1 to plot vectors.
baroclinic.fort.64.nc                              ! Name of file to use for vectors (fort.64, fort.74).
ADCIRC-OUTPUT                                      ! Vector file format flag: ADCIRC-OUTPUT.
1.00000                                            ! Unit conversion factor for vectors.
m/s                                                ! Alphanumeric label for units after conversion.
180.0                                              ! Magnitude of vector corresponding to one inch on the page.
0.15                                               ! Spacing between vectors indegrees.
0.06,0.04,0.01                                     ! Vector head length, head width, tail width.
-1,8                                               ! Magnitude of vector to show in the vector scale (or FIND to determine from file).
PARAMETERS FOR OVERALL PLOT(S):
0,Brown                                            ! Boundaries flag: 0 to ignore, 1 to plot roads/levees from grid.
0,White,4,4,1                                      ! Coastline flag: 0 to ignore, 1 to plot coastline with color, resolution (1[Least]-4[Most]), water bodies (1[Least]-4[Most]).
0,Black,st001.trk                                  ! Dots/lines flag: 0 to ignore, 1 to plot unconnected dots, 2 to plot connected line segments from an external file.
0,labels.txt                                       ! Labels flag: 0 to ignore, 1 to plot labels from external file.
0,TL,2.0,CHG.eps                                   ! Logo flag: 0 to ignore, 1 to plot logo at position (TL,TR,BL,BR) and width (inches) from an external file.
0,LATEX.txt                                        ! Background images: 0 to ignore, 1 to plot geo-referenced images from a list in an external file.
8.00                                               ! Width (inches) of plot.
0.25                                               ! Distance (inches) between edge of plot and contour scale, vector scale, time bar, plot label, etc.
1.00                                               ! Alternate black and white boxes on the border at every xth degree.
0.25                                               ! Annotate on the border at every xth degree.
1                                                  ! Image trim flag: 0 to ignore, 1 to trim image close to plot.
300                                                ! Resolution (dpi) of images.
JPG                                                ! Raster file format(s): PNG, JPG, BMP, TIFF, EPS, PDF.
0,75,2,20050828120000                              ! Flag for Google KMZ file, transparency (0-100) of images, number of layers, and time stamp of first record in 63 file for animation.
0,0                                                ! Flag for georeferencing: (0 to ignore, 1 for images, 2 for zipped images), and lowermost layer (or 0 to optimize).
0                                                  ! Number of records for which to produce images (or 0 for all).
0                                                  ! List of records (ignored if the number of records is 0)."""

tmplines = template.splitlines()

def get_comment(idx):
    return tmplines[idx].split('!')[1]

def replace_line(idx, string):
    comment = get_comment(idx)
    tmplines[idx] = string.ljust(50) + ' ! ' + comment

def set_filename(filename):
    replace_line(6, filename)

def set_plot_label(label):
    if label:
        replace_line(7, '1,' + label)
    else:
        replace_line(7, '0')

def set_time_bar(opt):
    if opt:
        replace_line(8, '1')
    else:
        replace_line(8, '0')

def set_grid_flag(opt):
    if opt:
        replace_line(14, '1')
    else:
        replace_line(14, '0')

def set_contour_fill(choice):
    replace_line(16, choice)

def set_contour_line(choice):
    replace_line(17, choice)

def set_contour_file(filename):
    replace_line(18, filename)

def set_contour_file_format(fmt):
    replace_line(19, fmt)

def invert_contour_unit():
    replace_line(20, '-1')

def set_color_line_flag(fmt):
    replace_line(24, fmt)

def set_box():
    with open("fort.14") as f14:
        l = f14.readline()
        l = f14.readline()
        numNodes = int(l.split()[1])

    arr = np.loadtxt("fort.14", skiprows=2, max_rows=numNodes)
    minvals = np.min(arr,0)
    maxvals = np.max(arr,0)

    minX = minvals[1]; minY = minvals[2]
    maxX = maxvals[1]; maxY = maxvals[2]

    replace_line(9, str(minX))
    replace_line(10, str(maxX))
    replace_line(11, str(minY))
    replace_line(12, str(maxY))

def plot_grid():
    set_time_bar(False)
    set_contour_fill('0')
    set_contour_line('0')
    set_grid_flag(True)
    set_contour_file('fort.14')
    set_contour_file_format('GRID-BATH')
    invert_contour_unit()
    set_color_line_flag('GRID-BATH')

def plot_bathy():
    set_time_bar(False)
    set_contour_fill('1')
    set_contour_line('0')
    set_contour_file('fort.14')
    set_contour_file_format('GRID-BATH')
    invert_contour_unit()
    set_color_line_flag('DEFAULT')

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-n", "--name", metavar="File name", default="plot")
    # parser.add_argument("-l", "--label", metavar="Plot label")
    parser.add_argument("-o", "--outfile", required=True)
    parser.add_argument("-m", "--mode", choices=["63", "grid","bathy"],
                        required=True)
    args = vars(parser.parse_args())

    set_filename("filename")
    set_plot_label("plotname")
    set_box()

    if args["mode"] == "grid":
        plot_grid()

    if args["mode"] == "bathy":
        plot_bathy()

    with open(args["outfile"], 'w') as f:
        f.write("\n".join(tmplines))


main()
