# Installing and connecting to a **Jupyter Notebook** on a remote EC2 Instance

## Connecting to Jupyter Notebook

0. In a **Public Subnet** of a **VPC**, launch an EC2 instance
(for instance: `Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-04b9e92b5572fa0d1`)

1. Check python version `ls -l /usr/bin/python*`

2. Install `pip` and then `jupyter`

    ```
    $ sudo apt-get update
    $ sudo apt-get install python3-pip
    $ pip3 install --user jupyter
    ``` 

3. To connect to a Jupyter Notebook, we need to edit the **security group** of the instance

    |Security Group | | | | |
    | --- |--- | --- | --- | --- |
    | | Type | Ports | Protocol | Source |
    | Inbound | SSH | 22 | TCP | \<my_public_ip\>/32 |
    | | Custom TCP Rule | 8888 | TCP | \<my_public_ip\>/32 |

4. In the remote host (the EC2 instance), we run Jupyter Notebook in the background,
   allowing any distant machine (IP address `0.0.0.0`) to connect to it

    ```
    $ nohup jupyter notebook --ip=0.0.0.0 &
    ```
 
5. We can now connect to the notebook by typing in a browser (on the local machine):
   `<ec2_public_ip>:8888`
   (the token may be read in `nohup.out`)

6. To stop the notebook

    ```
    $ jupyter notebook stop
    ```

## Installing a new Virtual Environment

1. First we install `pew` virtual environment manager

    ```
    $ pip3 install --user pew
    ```

2. We then create a new virtual environment and install a new kernel
   (the command `python3 -m ipykernel...` must be executed within the new environment)

    ```
    $ pew new mypyenv
    $ pip3 install --user ipykernel
    $ python3 -m ipykernel install --user --name=mypyenv
    ```

3. To list the kernels available in Jupyter Notebook and remove `pymyenv` kernel

    ```
    $ jupyter kernelspec list
    $ jupyter kernelspec uninstall mypyenv
    ```

