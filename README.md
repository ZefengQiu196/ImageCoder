# ImageCoder

**ImageCoder** is a web-based open-source image annotation tool for researchers in scientific disciplines to annotate images whose initial category codes may not be well defined and/or are influenced by experts' knowledge.

### How to run

ImageCoder is designed to be a web-based annotation program that supports multiple coders to work together. The whole program is built using Flask (python-based) with the SQLite as a back-end database (for the development). D3.js, Fabric.js, and Bootstrap.js are adopted to implement the front-end user interface.

To run the program, please make sure you have the following environment ready on your machine:

* python 3.8+
* flask 2.0+
* all packages in the requirement.txt

You can create a virtual env using conda and install all requirements using pip as follows:

```
conda create -n imagecoder python=3.8
conda activate imagecoder
cd <ImageCoder DIR>
pip install -r requirements.txt
```

1. cd to the ImageCoder directory:

```
cd <ImageCoder DIR>
```

2. run the program from a command prompt (e.g., powershell on Windows or terminal on a Mac/Linux)

```
python run.py

// you will see the following outputs from your terminal
 * Serving Flask app 'doc_anno_suite' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 998-708-343
```

By default, the program uses port 8000. You can open your web browser and enter the URL in the address field to access the program.

```
http://localhost:8000/
```

You can change the default port by updating the ./run.py file.

3. register the admin account

You will need to create an admin account when you first load the program. Next, you can use your registered account to log in to the program.

Please note that the sign-up function is only provided for the admin account. For future users, you can add them through the admin interface. By default, the password of all annotators is 123.

4. Set up your annotation project

You can access the admin (data management) interface through the following URL:

```
http://localhost:8000/admin
```

You could set up a new project from this interface or export the current annotation results to .csv files. 

Please click the question mark for more details about the inputs.

You can find several test cases under the './testcases' folder.

5. Testing

For testing purpose, you can login the system using the following username and password:

* username: RL
* password: 12345


### For developers

**Note**: The disagreement resolution page is not finished yet. There could be some unpredictable behaviors within the program.


* Root path:
  * run.py: set up how to run the program.
  * site.db: the sqlite database file, you can open it using the DB browser for SQLite.
* doc_anno_suite
  * models.py: defines the database schema.
  * database.py: defines the configuration of the database. You can update the path or the password (if existed) from this file.
  * config.py: some configurations, you can ignore this file in most cases.
  * templates folder: contains all HTML files for the program
  * static folder: contains all static resources for the program, including the js files, css stylesheets, datasets, and the images.
    * javascripts: you should update all javascripts codes here.
  * main folder: contains the routes for the entry point to the program.
  * annotations folder: this is the main back-end part of the program:
    * routes.py: defines all routes for the annotation interface
    * utils.py: defines some constants about the program
    * dbutils.py: defeins all database CRUD operations. If you need to add database APIs that relate to the annotation database, you should work here.
  * management folder: this folder is mainly used for controling the behavior of the admin page. In particular, it defines how to upload / delete / backup the project.
  * users folder: defines the user authentication functionalities.
    * form.py: defines the user input (e.g., login and register) events
    * routes.py: defines all routes for the login and register interfaces.


### Deployment

To deploy the program on a public server such as AWS. You can upload your program to the server and update the run.py file as follows:

```
app.run(host='0.0.0.0', port = 8000, debug=True)
```

Next, cd to the root of the program folder and use the following command to run the program:

```
nohup python run.py > log.txt 2>&1 &
```

Please note that the above deployment is a quick implementation and only applicable for a small group (<10 users) set-up. If you have many annotators for your project, please consider deploying your program using servers such as Nginx or apache. The [video](https://www.youtube.com/watch?v=goToXTC96Co&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=14) introduces how to deploy the flask program using Nginx from scratch.

### Licence

DocAnnoSuite is released under the MIT License (refer to the [LICENSE](https://github.com/LiruiErnest/ImageCoder.Release/blob/main/LICENSE) file for details).


### Contact

Contact [Rui Li](https://web.cse.ohio-state.edu/~li.8950/) or [Zefeng Qiu](qiu.573@osu.edu) for any queries or feedback related to this application.

### Acknowledgements

This work was partly supported by NSF OAC-1945347, NIST
MSE-10NANB12H181, NSF CNS-1531491, NSF IIS-1302755 and
the FFG ICT of the Future program via the ViSciPub project (no.
867378).
