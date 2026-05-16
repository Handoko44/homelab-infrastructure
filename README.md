
# 🌐 Homelab Server Infrastructure
![Uptime](https://img.shields.io/badge/Status-Online-success?style=for-the-badge&logo=proxmox)
![Location](https://img.shields.io/badge/Location-KalimantanTengah-blue?style=for-the-badge)
![VPN](https://img.shields.io/badge/VPN-WireGuard-green?style=for-the-badge&logo=wireguard)
```mermaid
graph TD
    %% Styling
    classDef internet fill:#f9f,stroke:#333,stroke-width:2px;
    classDef home_router fill:#2e64fe,color:#fff,stroke:#333,stroke-width:2px;
    classDef campus_router fill:#c0392b,color:#fff,stroke:#333,stroke-width:2px;
    classDef server fill:#f39c12,color:#fff,stroke:#333,stroke-width:2px;
    classDef lxc fill:#e1f5fe,stroke:#01579b,stroke-width:1px;
    classDef tunnel fill:#27ae60,color:#fff,stroke:#1e8449,stroke-width:2px,stroke-dasharray: 5 5;

    %% External Networks
    Internet((INTERNET)):::internet --- Modem[Modem ISP<br/>192.168.1.1]

    %% Campus Infrastructure
    subgraph Campus_Site [OFFICE]
        RB1100{MikroTik RB1100AHx4}:::campus_router
        Campus_SRV[Work Lab Server Infrastructure]:::server
        RB1100 --- Campus_SRV
    end

    %% Site-to-Site Tunnel
    Modem --- RB750{MikroTik RB750<br/>192.168.1.4}:::home_router
    RB750 -.-> WG_Tunnel((WireGuard Tunnel<br/>Site-to-Site VPN)):::tunnel
    WG_Tunnel -.-> RB1100

    %% Home Infrastructure
    subgraph Home_Site [HOME LAB - NETWORKLABS]
        direction TB
        RB750 --- AP[Eth4: Access Point<br/>10.40.0.1/24]
        RB750 --- Eth3[Eth3: SERVER<br/>10.30.0.1/24]:::server

        subgraph Proxmox_Hypervisor [HP 8470W - PROXMOX VE]
            Eth3 --- PVE[PVE Node<br/>Local: 10.30.0.253]:::server
            
            subgraph LXC_Containers [LXC Containers]
                PVE --- CT100[SERVER-LOKAL]:::lxc
                PVE --- CT102[CasaOS]:::lxc
                PVE --- CT103[Docker Engine]:::lxc
                PVE --- CT106[Web Server]:::lxc
                PVE --- CT105[Homepage Dashboard]:::lxc
            end

            subgraph Virtual_Machines [VMs]
                PVE --- VM104[TrueNAS Core]
                PVE --- VM107[Kali Linux Lab]
            end
        end
    end

    %% Integration Note
    Note[Integrasi Jalur Data:<br/>Backup & Management Site-to-Site via WireGuard]
    Note -.-> WG_Tunnel
