# load_localization_to_db.py

load_localization_to_db.py is a script for converting pre-calculated localization results from the [VIS30K](https://ieee-dataport.org/open-access/ieee-vis-figures-and-tables-image-dataset) format to imageCoder's database format.


## Usage

To run the program, please make sure you have the following environment ready on your machine:

* python 3.8+
* pandas

You can run the script through the following command:

```
$ python load_localization_to_db.py -h  
Usage: python load_localization_to_db.py [options]

Examples:

$ python load_localization_to_db.py -m ./meta/ -u ./users.csv -i ./images.csv -s label_schema.csv

$ python load_localization_to_db.py 
By default, load_localization_to_db uses the following paths:
meta_path = './meta/'
user_path = './users.csv'
image_path = './images.csv'
schema_path = './label_schema.csv'

The output file (annotations.csv) will be stored under the same folder.

Options:
-m: the path to the meta files
-u: the path to the users.csv
-i: the path to the images.csv
-s: the path to the label_schema.csv

```

After converting the localization results to the database format, you can zip the following files into a zip file and upload it to the ImageCoder.

* users.csv
* images.csv
* label_schema.csv
* annotation.csv


# extract_db_to_localization.py

extract_db_to_localization.py is a script for exporting annotated results from the imageCoder's database format to [VIS30K](https://ieee-dataport.org/open-access/ieee-vis-figures-and-tables-image-dataset) format.

## Usage

To run the program, please download the update-to-date annotation results from:
http://ec2-3-136-85-137.us-east-2.compute.amazonaws.com:8000/admin by clicking the "export annotation results" button.

Next, unzip the result.zip file and run the script through the following commands:

```
$ python extract_db_to_localization.py -h  
Usage: python extract_db_to_localization.py [options]

Examples:

$ python extract_db_to_localization.py -a ./annotations.csv -u ./users.csv -i ./images.csv -s label_schema.csv

$ python extract_db_to_localization.py 

By default, extract_db_to_localization uses the following paths:
annotation_path = './annotations.csv'
user_path = './users.csv'
image_path = './images.csv'
schema_path = './label_schema.csv'

Please note that the four files above should come from the result.zip file you downloaded from the data management page, not the files you prepared for the load_localization_to_db script!

The output meta files will be stored under the same folder.

Options:
-a: the path to the annotations.csv
-u: the path to the users.csv
-i: the path to the images.csv
-s: the path to the label_schema.csv

```

### Licence

ImageCoder is released under the MIT License (refer to the [LICENSE](https://github.com/LiruiErnest/ImageCoder.Release/blob/main/LICENSE) file for details).
