# Moodle Plugin for Microsoft Teams #
---

### User manual (using a local development Moodle 
---
**Instructions**  
1. Setting up the development environment (Apache + PHP + MySQL)  
    We used [MAMP](https://www.mamp.info/en/windows/) as the local server environment because it provided all the instalation requirements. However, you can choose any of the possible instalation requirements (suited for your machine specifications) as listed by [Moodle](https://docs.moodle.org/dev/Setting_up_development_environment).
    
2. Install the plugin  
   To install the plugin clone or download this repository, compress the folder, and proceed as instructed [here](https://docs.moodle.org/38/en/Installing_plugins)
   
3. Integration  
   In order for the plugin to process user requests you need to configure the Gearman server as prompted by their [documentation](http://gearman.org/getting-started/). Additionaly, you need to configure the PHP PECL extension for Gearman and the (python gearman library)[https://pypi.org/project/gearman/].
   
4. Visualization dashboard  
   For using the dashboard you need to install all the dependencies listed in *requirements.txt* and additionally to configure a folder comprising this open-source [dataset](https://www.kaggle.com/freecodecamp/all-posts-public-main-chatroom) and change the path in the data_wrapper.py file to match the local path of your saved dataset.



### Deployment manual  
---
**Instructions**  
1. The plugin should be deployed on UCL's Moodle version
2. The python application should be deployed on a remote server for efficiency purposes


### License
---

2016 Alexandru Elisei <alexandru.elisei@gmail.com>, David Mudrák <david@moodle.com>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
