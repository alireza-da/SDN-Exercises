"""
Custom topology example
Three directly connected switches plus a host attached to each switch 
with a remote RYU SDN Controller (c0):
 
 c0
 RYU /|\ 192.168.1.6
 .........../.|.\.................
 Mininet / | \ 192.168.1.5
 / | \
 h1 --- s1 | s3 --- h3
 \ | /
 \ | /
 \ | /
 \|/
 s2 --- h2
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
# Ryu controller
ryu_ip = '127.0.0.1'
ryu_port = 6653
# Define remote RYU Controller
print('Ryu IP Addr:', ryu_ip)
print('Ryu Port:', ryu_port)
def customNet():
    "Create a customNet and add devices to it."
    net = Mininet( topo=None, build=False )

    # Add controller
    info( 'Adding controller\n' )
    net.addController( 'c0',
    controller=RemoteController,
    ip = ryu_ip,
    port = ryu_port
    )
    # Add hosts 
    info( 'Adding hosts\n' )
    h1, h2, h3 = [ net.addHost(h) for h in ('h1', 'h2', 'h3') ]

    # Add switches
    info( 'Adding switches\n' )
    s1, s2, s3 = [ net.addSwitch(s) for s in ('s1', 's2', 's3') ]
    # Add links
    info( 'Adding switch links\n' )
    for sa, sb in [ (s1, s2), (s2, s3) ]:
        net.addLink( sa, sb )
    for h, s in [ (h1, s1), (h2, s2), (h3, s3) ]:
        net.addLink( h, s )
    info( '*** Starting network ***\n')
    net.start()
    info( '*** Running CLI ***\n' )
    CLI( net )
    info( '*** Stopping network ***' )
    net.stop()
if __name__ == '__main__':
 setLogLevel( 'info' )
 customNet()
exit(0)
