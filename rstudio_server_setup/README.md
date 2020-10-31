# Setting up an **RStudio Server** on AWS

## Setting up the infrastructure

1. Create a **VPC** (CIDR: 10.0.0.0/16)

2. Create a **Public Subnet** (CIDR: 10.0.0.0/24)

3. Create an **Internet Gateway** and attach it to the VPC

4. Create and/or edit the **Route Table**

    | Public Subnet Route Table | |
    | --- | --- |
    | Destination | Target |
    | 10.0.0.0/16 | local |
    | 0.0.0.0/0 | IGW |

## Launching the EC2 instance

1. In the **Public Subnet**, launch an **EC2 instance** (e.g., Amazon Linux 2 AMI)

2. If necessary, allocate a new **Elastic IP address** and associate it to the EC2 instance

3. Edit the Security Group of the EC2 instance (*RStudio Server uses port 8787*)

    |Security Group | | | | 
    | --- |--- | --- | --- |
    | | Ports | Protocol | Source |
    | Inbound | 22 | SSH | 0.0.0.0/0 |
    | | 8787 | TCP | 0.0.0.0/0 |
    | Outbound | all | all | 0.0.0.0/0 |

## Installing R and RStudio Server Interactively

1. Connect to the instance via ssh

    ```
    PS> ssh -i KeyPair.pem ec2-user@<public_ec2_ip_address>
    ```

2. Update package manager `yum`

    ```
    $ sudo yum update
    ```

3. Install R

    ```
    $ sudo amazon-linux-extras install R3.4
    ```

4. Download and install Rstudio Server (for CentOS 6-7 with Amazon Linux 2 AMI), following
   [installation instructions](https://rstudio.com/products/rstudio/download-server/redhat-centos/)

    ```
    $ wget https://download2.rstudio.org/server/centos6/x86_64/rstudio-server-rhel-<version>.rpm
    $ sudo yum install rstudio-server-rhel-<version>.rpm
    ```

5. Add username and password

    ```
    $ sudo useradd my_username
    $ sudo passwd my_username
    ```

6. Connect to RStudio via a Web Browser with the URL `<public_ec2_ip_address>:8787`

## Installing R and RStudio Server while launching the EC2 instance

1. Include the script below at launch of the EC2 instance
   (step *Configure Instance*, option *Advanced Details*)<br/>
   **DO NOT FORGET THE `-y` FOR AUTOMATIC CONFIRMATION**

    ```
    #!/bin/bash
    sudo yum update -y
    sudo amazon-linux-extras install R3.4 -y
    wget https://download2.rstudio.org/server/centos6/x86_64/rstudio-server-rhel-1.2.5019-x86_64.rpm
    sudo yum install rstudio-server-rhel-1.2.5019-x86_64.rpm -y
    sudo useradd my_username
    echo my_username:my_password | sudo chpasswd
    ```
