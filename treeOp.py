#!/usr/bin/python

import os, gzip
import cPickle as pickle
import Prefixes

def buildTree(path):
  return

def main():
  path = 'data.caida.org/'
  tree = Prefixes.Prefixes()
  #iterate through files
  for root, dirs, files in os.walk(path,topdown=True):
    dirs.sort()
    for stuff in sorted(files):
      if stuff.endswith('.gz'):

        print(stuff)
        _, _, date, _ = stuff.split('-')
        print(date)
        print(os.path.join(root,stuff))
        exit()
        with gzip.open('input.gz','rt') as f:
          for line in f:
            exit()
           

#      json_file = gzip.open(os.path.join(root,stuff))

if __name__ == "__main__":
  main()
