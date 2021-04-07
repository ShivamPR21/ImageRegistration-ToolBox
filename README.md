# Affine APP
Web work for Affine transformation for the images.

## Provided Transformations
- Translation
    - [1 0 t<sub>x</sub>]<br>
      [0 1 t<sub>y</sub>]
      
    
- Rotation
    - [cos sin 0]<br>
      [-sin cos 0]
      
- Skew
    - [1 v<sub>x</sub> 0]<br>
      [v<sub>y</sub> 1 0]
      
- Scale
    - [s<sub>x</sub> 0 0]<br>
      [0 s<sub>x</sub> 0]

## Process to Get the App Running

**Note:** *We can run the project as a standalone electron app or simply as a web app. The process to get this running 
as a web app is give here.*

### Get the toolbox and Install dependencies
```shell
$ gh repo clone ShivamPR21/ImageRegistration-ToolBox
$ cd ImageRegistration-ToolBox
$ git checkout tr_app

# Install Requirements
$ pip3 install pandas matlab seaborn opencv-python Flask Flask-WTF
```

### Run the Flask Server
```shell
# Make sure that you are in the project directory
$ python app.py
```

### Open the app in your browser
<p>Put the URL `http://localhost:5000` in your browser search bar and hit Enter.</p>

### Usage:
1. Select the file Imagery.L-3
2. Select Method for PCA analysis
3. Hit Start Analysis
4. Wait the Results window will load in few minutes based on the speed of your PC.
