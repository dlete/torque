Read this file when you want to modify. When you have not worked on this project for a long time. 


## How to activate the Python virtual environment
```bash
source <path_to_virtual_environment_root>/bin/activate
```

## How to run the development server
Once you have enabled the Python environment
```bash
cd <django_root>
python manage.py runserver 0.0.0.0:3000 --settings=torque.settings_development
```

## How to Git
### Update the `master` branch. 
Before changes in the code, before anything:
```bash
git pull
```

### Create a branch to make the changes
Any changes, make them in a branch other than master. 
```bash
git checkout -b <working_branch_name>
```

### Add changes to the branch and commit
Add files to the branch
```bash
git add --all
```
or 
```bash
git add -A
```

Commit 
```bash
git commit -m "add .gif of Rita dancing"
```


## How to add .gif, photos
This is a three step process:
* Upload the files
* Instruct Django to copy the files to the Django static directory
* Reload the webserver

#### Upload the files
Copy the .gif or .jpg (or whatever extension) files to the `core` app, to the `core/static/gif/` directory.
```bash
<django_root>/core/static/gif/
```

#### Move .gif/pictures to the `static` directory
Collect all the static files from all the apps and put them in the `static` directory. 
```bash
python manage.py collectstatic
```





