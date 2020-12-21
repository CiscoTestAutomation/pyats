#### Contribute to documentation


To contribute, you need to fork the repository, do your modifications and create a new pull request. 

> Here we are using the pyATS docs as an example; Same steps could be applied to other packages

  - Go to the [pyATS Github repository](https://github.com/CiscoTestAutomation/pyats)
  
  - On the top right corner, click ```Fork```. (see https://help.github.com/en/articles/fork-a-repo)

<img width="421" alt="Screen Shot 2020-12-21 at 2 37 19 PM" src="https://user-images.githubusercontent.com/30438439/102815289-1e75e700-439a-11eb-92bc-e424ddce9758.png">

  - Clone the repository by running ```git clone https://github.com/<your_github_username>/pyats```
  
  - ```cd pyats/docs```
  
  > :warning: **Please make sure you have the full pyats package installed via pip install pyats[full].**

  - Use ```make install_build_deps```  to install all of the build dependencies
  
  - Run ```make docs``` to generate documentation in HTML

  - Wait until you see ```Done``` in your terminal
  
  - The documentation is now built and stored under the directory 
  ```pyats/docs/__build__```

  - Run ```make serve``` to view the documentation on your browser

  - Please create a PR after you have made your changes (see [commit your changes](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#commit-your-changes) & [open a PR](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#open-a-pull-request))


#### How to contribute to the pyATS community

- For detail on contributing to pyATS, please follow the [contribution guidelines](https://pubhub.devnetcloud.com/media/pyats-development-guide/docs/contribute/contribute.html#)
