#! /usr/bin/env python

"""
-------
xray.py
-------
A simple command line interface for xarray
To be used for quick exploration of a Dataset
Script with xarray if more elaborate stuff is needed
-------
A. Spiga 02/04/2018
-------
example: dust climatologies on Mars
http://www-mars.lmd.jussieu.fr/mars/dust_climatology/index.html
(python) xray.py /home/aspiga/data/datadir/dust_MY29.nc -v cdod -d latitude 4.5 -d longitude 135. -s Time Ls
-------
"""

import argparse
import xarray as xr
import matplotlib.pyplot as plt

if __name__ == '__main__':

  ## set argument parser
  parser = argparse.ArgumentParser(description='Command Line Interface for xarray')
  parser.add_argument('files', metavar='F', type=str, nargs='+', \
    help='file(s) to explore')
  parser.add_argument('-v', '--var', metavar='V', type=str, \
    help='data variables [append possible]',action='append')
  parser.add_argument('-d', '--dim', metavar=('C','V'), type=str, nargs=2, \
    help='reduce coordinate C to value V [append possible]',action='append')
  parser.add_argument('-i', '--index', metavar=('C','I'), type=str, nargs=2, \
    help='reduce coordinate C to index I [append possible]',action='append')
  parser.add_argument('-m', '--mean', metavar='C', type=str, default=None, \
    help='compute mean on coordinate C [append possible]',action='append')
  parser.add_argument('--decode_times', metavar='False/True', type=bool, default=False, \
    help='decode times axis in dataset [default is False]')
  parser.add_argument('-s', '--swap', metavar=('C','V'), type=str, nargs=2, \
    help='swap dimensions: V in place of C')
  args = parser.parse_args()

  ## loop on files
  for ff in args.files:

    ## open dataset
    ds = xr.open_dataset(ff,decode_times=args.decode_times)
    
    ## swap dimensions
    if args.swap is not None:
      ds = ds.swap_dims({args.swap[0]: args.swap[1]})
    
    ## if no data variables, simply describe dataset
    if args.var is None:
      print(ds)
      quit()

    ## loop on variables
    for vv in args.var:

      ## get variable inside dataset
      ## raise an error if not found
      try:
        dsred = ds[vv]
      except KeyError:
        print("Error: Data variable {0} not in file.".format(vv))
        print("------------------------")
        print(ds.data_vars)
        quit()  

      ## (if applicable) get dimension reduction (value)
      if args.dim is not None:
        for aaa in args.dim: 
          d = {}
          d[aaa[0]] = float(aaa[1])
          try:
            dsred = dsred.loc[d]
          except ValueError:
            print("Error: Dimension {0} not in file for data variable {1}".format(aaa[0],vv))
            print("------------------------")
            print(dsred.dims)
            quit()
          except KeyError:
            print("Error: Value {0} not in file for dimension {1}".format(aaa[1],aaa[0]))
            print("------------------------")
            print(ds.coords[aaa[0]])
            quit()
            
      ## (if applicable) get dimension reduction (index)
      if args.index is not None:
        for aaa in args.index: 
          d = {}
          d[aaa[0]] = int(aaa[1])
          try:
            dsred = dsred[d]
          except ValueError:
            print("Error: Dimension {0} not in file for data variable {1}".format(aaa[0],vv))
            print("------------------------")
            print(dsred.dims)
            quit()
          except IndexError:
            print("Error: Index {0} not in file for dimension {1}".format(aaa[1],aaa[0]))
            print("------------------------")
            print(ds.coords[aaa[0]])
            quit()
            
      ## (if applicable) compute mean
      ## NB: dsred = dsred.mean(args.mean) works directly with several coordinates
      ##     but we want to be able to handle errors for each coordinate
      if args.mean is not None:
        for aaa in args.mean:
          try:
            dsred = dsred.mean(aaa)
          except ValueError:
            print("Error: Dimension {0} not in file for data variable {1}".format(aaa,vv))
            print("------------------------")
            print(dsred.dims)
            quit()

      ## plot
      dsred.plot()
      plt.show()


