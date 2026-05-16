from diagrams import Cluster, Diagram, Edge
from diagrams.generic.network import Router, Switch, Firewall
from diagrams.generic.compute import Rack
from diagrams.generic.os import Ubuntu, Debian
from diagrams.generic.storage import Storage

with Diagram("Home Lab Topology", show=False, filename="homelab_topology", direction="TB"):
    internet = Internet("Internet")
    modem = Router("Modem ISP\n192.168.1.1")
    
    mikrotik = Router("MikroTik RB750\n10.30.0.1")

    with Cluster("Proxmox VE (HP 8470W)"):
        proxmox = Rack("Hypervisor")
        
        with Cluster("LXC Containers"):
            adguard = Ubuntu("AdGuard Home")
            casaos = Ubuntu("CasaOS")
            web_srv = Debian("Web Server")
            
        with Cluster("Virtual Machines"):
            truenas = Storage("TrueNAS")
            kali = Linux("Kali Linux")

    internet >> modem >> mikrotik >> proxmox
    proxmox >> adguard
    proxmox >> casaos
    proxmox >> web_srv
    proxmox >> truenas
    proxmox >> kali
