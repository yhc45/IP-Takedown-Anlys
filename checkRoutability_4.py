#!/usr/bin/python

import cPickle as pickle
import ipaddress
from treeOp import buildTree
from datetime import datetime, date, timedelta
import random

def daterange (start_date, end_date):
  for n in range(int((end_date-start_date).days)):
    yield start_date + timedelta(n)



def main():
  start_date = date(2019,6,5)
  end_date = date(2020,2,26)
  edrop_route = {}
  edrop_counter = 0
  weird_counter = 0
  diff_time = 0
  diff_amount = 0
  diff_weird_counter = 0
  occurred = set()
  with open("edroplist_data.pickle", "rb") as f:
    edrop_data = pickle.load(f)
  ip_list = [x for x in edrop_data if x[-3] == '/']
  ip_list = ip_list[len(ip_list)//2:]
  for p_date in daterange(start_date,end_date):
    day = p_date.strftime('%d')
    month = p_date.strftime('%m')
    year = p_date.strftime('%Y')
    date_str = p_date.strftime('%Y-%m-%d')
    try: 
      tree = buildTree(year,month,day)
    except OSError as e:
      print(e)
      print('failed to access date %s'%date_str)
      print('Make sure the date is valid')
      continue

    print(date_str)
    for x in ip_list:
      counter = 0
      if x not in occurred:
        for u_ip in random.sample(list(ipaddress.IPv4Network(unicode(x, "utf-8"))),100):
          ip = str(u_ip)
          if not tree.check_prefix_is_routable(ip):
            counter += 1
        if counter != 0:
          if date_str not in edrop_route:
            edrop_route[date_str] = [x]
            occurred.add(x)
            edrop_counter += 1
          else:
            edrop_route[date_str].append(x)
            occurred.add(x)
            edrop_counter += 1
             
          date_added = datetime.strptime(edrop_data[x][0],"%Y-%m-%d").date()
          diff = p_date - date_added
          if p_date < date_added:
            # blocked before it is added to bllack list
            diff_weird_counter += 1
          else:
            diff_time += diff.total_seconds()
            diff_amount +=1
          if counter != 100:
            weird_counter += 1
  f1 = open( "edroproute_2.pickle", "wb" )
  pickle.dump( edrop_route, f1)
  f1.close()

  avg_day = diff_time/86400/diff_amount
  print("edrop_part2")
  print("edrop_counter: " + str(edrop_counter))
  print(edrop_route)
  print("weird_counter " + str(weird_counter))
  print("avg_hour " + str(avg_day))
  print("diff_weird_counter " + str(diff_weird_counter))

if __name__ == "__main__":
  main()
