Example Testbed File
====================

.. code-block:: yaml

    # Example
    # -------
    #
    #   an example two router testbed

    extends: base_tb_config.yaml

    testbed:
        name: sampleTestbed
        alias: topologySampleTestbed
        credentials:
            default:
                username: admin
                password: CSCO12345^
            enable:
                password: "%ASK{user specified prompt}"
        servers:
            filesvr:
                server: ott2lab-tftp1
                address: 223.255.254.254
                path: ""
                credentials:
                    default:
                        username: rcpuser
                        password: 123rcp!
                    sftp:
                        username: sftpuser
                        password: "%ENC{w6DDmsOUw6fDqsOOw5bDiQ==}"
                    ftp:
                        username: ftpuser
                        password: "%ASK{}"

            ntp:
                server: 102.0.0.102
        custom:
            owner: john
            contacts: mai@domain.com
            mobile: "%ASK{enter owner mobile phone number}"

    devices:
        ott-tb1-n7k4:
            os: nxos
            type: Nexus 7000
            alias: device-1
            credentials:
                default:
                    username: admin
                    password: abc123
                enable:
                    password: "%ASK{}"
            connections:
                a:
                  protocol: telnet
                  ip: 10.85.84.80
                  port: 2001
                b:
                  protocol: telnet
                  ip: 10.85.84.80
                  port: 2003
                vty:
                  protocol: telnet
                  ip: 5.19.27.5
                  credentials:
                    default:
                        username: mgtuser
                        password: mgtpw
            clean:
                pre_clean: |
                          switchname %{self}
                          license grace-period
                          feature telnet
                          interface mgmt0
                              ip addr %{self.connections.vty.ip}/24
                          no shut
                          vrf context management
                              ip route 101.0.0.0/24 5.19.27.251
                              ip route 102.0.0.0/24 5.19.27.251
                post_clean: |
                          switchname %{self}
                          license grace-period
                          feature telnet
                          interface mgmt0
                              ip addr %{self.connections.vty.ip}/24
                          no shut
                          vrf context management
                              ip route 101.0.0.0/24 5.19.27.251
                              ip route 102.0.0.0/24 5.19.27.251
            custom:
                SUP1: Supervisor Module-1X
                SUP2: Supervisor Module-1X

        ott-tb1-n7k5:
            os: nxos
            type: Nexus 7000
            alias: device-2
            connections:
                a:
                  protocol: telnet
                  ip: 10.85.84.80
                  port: 2006
                b:
                  protocol: telnet
                  ip: 10.85.84.80
                  port: 2009
                vty:
                  protocol: telnet
                  ip: 5.19.27.6
            clean:
                pre_clean: |
                            switchname %{self}
                            license grace-period
                            feature telnet
                            interface mgmt0
                                ip addr %{self.connections.vty.ip}/24
                            vrf context management
                                ip route 101.0.0.0/24 5.19.27.251
                                ip route 102.0.0.0/24 5.19.27.251
                post_clean: |
                          switchname %{self}
                          license grace-period
                          feature telnet
                          interface mgmt0
                              ip addr %{self.connections.vty.ip}/24
                          no shut
                          vrf context management
                              ip route 101.0.0.0/24 5.19.27.251
                              ip route 102.0.0.0/24 5.19.27.251
            custom:
                SUP1: Supervisor Module-1X
                SUP2: Supervisor Module-1X

    topology:
        ott-tb1-n7k4:
            interfaces:
                Ethernet4/1:
                    alias: device1-intf1
                    link: rtr1-rtr2-1
                    type: ethernet
                Ethernet4/2:
                    alias: device1-intf2
                    link: rtr1-rtr2-2
                    type: ethernet
                Ethernet4/6:
                    link: ethernet-1
                    type: ethernet
                Ethernet4/7:
                    link: ethernet-1
                    type: ethernet
                Ethernet4/45:
                    link: ethernet-2
                    type: ethernet
                Ethernet4/46:
                    link: ethernet-2
                    type: ethernet

        ott-tb1-n7k5:
            interfaces:
                Ethernet5/1:
                    alias: device2-intf1
                    link: rtr1-rtr2-1
                    type: ethernet
                Ethernet5/2:
                    alias: device2-intf2
                    link: rtr1-rtr2-2
                    type: ethernet


