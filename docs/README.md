### Build Documentation Locally

#### Prerequisites

> :warning: **Please make sure you have the full pyats package installed via ```pip install pyats[full]```.**


To build the docs locally on your machine. Please follow the instructions below 

  - Go to the [pyATS Github repository](https://github.com/CiscoTestAutomation/pyats)
  
  - Click the green button says ```Code```
  
  - Copy the **HTTPS** URL (ends with ```.git```) of the project
  
  - In your terminal, clone the repo using the command shown below: 
    ```shell
    git clone https://github.com/CiscoTestAutomation/pyats.git
    ```

  - ```cd pyats/docs```
  
  - Use ```make install_build_deps```  to install all of the build dependencies
  
  - Run ```make docs``` to generate documentation in HTML

  - Wait until you see ```Done``` in your terminal
  
  - The documentation is now built and stored under the directory 
  ```pyats/docs/__build__```

  - Run ```make serve``` to view the documentation on your browser