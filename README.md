
# Moodle Plugin for Microsoft Teams #
---

### User manual (using a local development Moodle environment)
---
**Instructions**  
1. Setting up the development environment (Apache + PHP + MySQL)  
    We used [MAMP](https://www.mamp.info/en/windows/) as the local server environment because it provided all the instalation requirements. However, you can choose any of the possible instalation requirements (suited for your machine specifications) as listed by [Moodle](https://docs.moodle.org/dev/Setting_up_development_environment).
    
2. Python Application requirements
    ```
    pip install O365
    ```
3. Install the plugin  
  To install the plugin clone or download this repository, compress the folder, and proceed as instructed 
 [here](https://docs.moodle.org/38/en/Installing_plugins).
   
4. Integration  
   In order for the plugin to process user requests you need to configure the Gearman server as prompted by their [documentation](http://gearman.org/getting-started/). Additionaly, you need to configure the [PHP PECL extension](https://www.php.net/manual/en/book.gearman.php) for Gearman and the [python gearman library](https://pypi.org/project/gearman/). 
   In order for the changes from the Moodle UI to take place you need to run the *integration_layer.py* to enable the Gearman server to listen for requests sent from the client application.
    ```
    python integration_layer.py
    ```
5. Visualization dashboard  (dashboard folder)
   For using the dashboard you need to install all the dependencies listed in the *requirements.txt* file.  
    ```
    pip install -r requirements.txt
    ```
   Additionally, you need to configure a folder (i.e. data) with this open-source [dataset](https://www.kaggle.com/freecodecamp/all-posts-public-main-chatroom) and change the path in the *data_wrapper.py* file to match the local path of your saved dataset.


### Deployment manual  
---
**Instructions**  
1. The plugin should be deployed on UCL's Moodle version
2. The python application should be deployed on a remote server
