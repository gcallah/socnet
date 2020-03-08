import sys
from push import push_to_slack

print ('Sending message \'' + sys.argv[1] + '\' to my channel...')
print (push_to_slack(sys.argv[1]))
