# Characters Clustering

This program clusters monochromatic images representing
characters.

## Solution description
I'm using hierarchical clustering with average linkage.
I'm preprocessing images so that all pixels are
black or white and there are no white borders.
My metric is checking number of matching black pixels,
image size and proportions, length of
vertical white pixels sequences.

On my computer 5000 images are being clustered for
3-4 minutes.

The output of this program are two files with results
(`index.html` and `results`).

## How to run
 - To run clustering on images listed in file with path
 `file_path` simply run `python3 run.py file_path`.
 - (only on Windows) To install needed libraries
 and run clustering on images listed in file with path
 `file_path` run `.\prepare_and_run.bat file_path`. 
 
