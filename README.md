## Prerequisites

* yum install publican pandoc

## Usage

* cd into ```[gitbook directory]```
* run ```[this script directory]/auto.sh```
* cd into ```[gitbook directory]/docbook/docbook``` to see the publican output
* compile publican source, for example: ```publican build --formats=html,pdf --langs=zh-CN --brand_dir=/usr/share/publican/Common_Content/eayun```

## Appendix

### auto.sh

run this script under a gitbook directory, and the converted docbook will sit in ./docbook/docbook

### con.py

convertion script from gitbook to docbook, this script is used by **auto.sh**

### chapter.docbook && default.docbook

template file used by pandoc which is invoked by **con.py**

### im.py

pre modification to gitbook scource before converting to docbook, this script is used by **auto.sh**

### xmlmod.py

additional modification to the converted docbook source, this script is used by **auto.sh**

### FileTranslations

if the gitbook source contains chinese file name and directory, add the chinese names in this file for translation, because docbook seems not supporting utf-8 file paths
