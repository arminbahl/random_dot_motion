# Random dot motion - Control Center
This set of python files provides a simple easy-to-use toolbox for displaying random dot motion stimuli. It comes with a convenient 
graphical user interface where important stimulus features, such as coherence or dot lifetime, can be setup in real-time.

The display of visual stimuli is based on the python-friendly gaming engine [Panda3d] (https://www.panda3d.org/). 
I use vertex shaders to move dots around and Windows 10. While Panda3D generally supports on all platforms, 
I did not manage to use shaders on platforms others than windows. Please let me know if you get it to run on Linux or MacOS.

#### Installation
Install the latest Python 3. I am using the [Anaconda] (https://www.anaconda.com/distribution/#download-section) distribution.

Go to the Anaconda Prompt and create a new environment:

    conda create --name py37 --channel conda-forge python=3.7
    conda activate py37
    conda install -c conda-forge scipy pyqt
    pip install panda3d
    
Get the source code from the repository:

    git clone https://github.com/arminbahl/random_dot_motion
    