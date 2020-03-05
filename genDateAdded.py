#!/usr/bin/python

import os, zipfile
import cPickle as pickle

prev_drop={}
prev_edrop={}
curr_drop={}
curr_edrop={}
drop_data = {}
edrop_data = {}
def extract_zip(zip_file):
  global curr_drop
  global curr_edrop
  with zipfile.ZipFile(zip_file) as myzip:
    with myzip.open('blocklist-ipsets-master/spamhaus_drop.netset') as myfile:
      content = myfile.readlines()
      filter_list = [x.strip('\n') for x in content if not x.startswith('#')]
      curr_drop = set(filter_list)
    with myzip.open('blocklist-ipsets-master/spamhaus_edrop.netset') as myfile:
      content = myfile.readlines()
      filter_list = [x.strip('\n') for x in content if not x.startswith('#')]
      curr_edrop = set(filter_list)
  return


def main():
  global drop_data
  global edrop_data
  global prev_drop
  global prev_edrop
  global curr_drop
  global curr_edrop
  empty_count = 0
  directory = '/data/blocklist'
  for filename in sorted(os.listdir(directory)):
    if filename.endswith(".zip"):
      date = filename.rstrip('.zip').split("_")[2]
      zip_file = os.path.join(directory, filename)
      extract_zip(zip_file)
#      print(curr_drop)
#      print(curr_edrop)
      print(date)
      if not prev_drop:# or not prev_edrop:
        empty_count += 1
        if empty_count > 1:
          print("Error: more than 1 empty count")
          exit(1)
        prev_drop = curr_drop
        prev_edrop = curr_edrop
        continue
      #calculating the ones added to the blacklist
      added_drop = curr_drop - prev_drop
      added_edrop = curr_edrop - prev_edrop
      for ip in added_drop:
        if ip not in drop_data:
          drop_data[ip] = [date]
        else:
          drop_data[ip].append(date)
        if date not in drop_data:
          drop_data[date] = ["Add %s"%ip]
        else:
          drop_data[date].append("Add %s"%ip)

      for ip in added_edrop:
        if ip not in edrop_data:
          edrop_data[ip] = [date]
        else:
          edrop_data[ip].append(date)
        if date not in edrop_data:
          edrop_data[date] = ["Add %s"%ip]
        else:
          edrop_data[date].append("Add %s"%ip)

      #calculating the ones removed from the blacklist
      removed_drop =  prev_drop - curr_drop
      removed_edrop = prev_edrop - curr_edrop 
      for ip in removed_drop:
        if ip in drop_data:
          drop_data[ip].append(date)
        if date not in drop_data:
          drop_data[date] = ["Remove %s"%ip]
        else:
          drop_data[date].append("Remove %s"%ip)

      for ip in removed_edrop:
        if ip in edrop_data:
          edrop_data[ip].append(date)
        if date not in edrop_data:
          edrop_data[date] = ["Remove %s"%ip]
        else:
          edrop_data[date].append("Remove %s"%ip)
      prev_drop = curr_drop
      prev_edrop = curr_edrop
    else:
      continue
  print(drop_data)
  print(edrop_data)
  f1 = open( "droplist_data.pickle", "wb" )
  pickle.dump( drop_data, f1)
  f1.close()
  f2 = open( "edroplist_data.pickle", "wb" )
  pickle.dump( edrop_data, f2)
  f2.close()

if __name__ == "__main__":
  main()
