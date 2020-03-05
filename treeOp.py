#!/usr/bin/python

import os, gzip
import cPickle as pickle
import Prefixes
import re

def buildTree(year,month,day):
  path = 'data.caida.org/'+year+'/'+month+'/'
  tree = Prefixes.Prefixes()
  pattern = '(%s%s%s)'%(year,month,day)
  for filename in sorted(os.listdir(path)):
    if re.search(pattern,filename):
      data = path+filename
      with gzip.open(data,'rt') as f:
        for line in f:
          ip, mask, _  = line.strip('\n').split('\t')
          tree.add_routable_prefix(ip,mask)
      return tree
  return None

def main():
  year = '2020'
  month = '02'
  day = '01'
  try: 
    buildTree(year,month,day)
  except OSError as e:
    print(e)
    print('Make sure the date is valid')
  

#      json_file = gzip.open(os.path.join(root,stuff))

if __name__ == "__main__":
  main()
