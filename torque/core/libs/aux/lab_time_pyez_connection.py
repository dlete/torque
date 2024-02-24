'''
Measures how long does it take for a connection to be established.
'''
# https://groups.google.com/forum/#!topic/junos-python-ez/bG8OnBhkEKE

#Parameters for connecting to device
host = sys.argv[1]
user = 'root'
password = getpass()

from jnpr.junos import Device
start = time.time()
print("Making connection to device at", start)

dev = Device(host, user=user, password=password)
dev.open(gather_facts=False)

stop = time.time()
print("Connection made at", stop)
print("Total time to connect:", stop-start)

dev.close()
