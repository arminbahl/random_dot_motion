# Random dot motion - Control Center
Welcome!

This set of python files provides a simple and easy-to-use toolbox for displaying random dot motion stimuli. It comes with a convenient 
graphical user interface where important stimulus features, such as coherence or dot lifetime, can be setup in real-time.

The display of visual stimuli is based on the python-friendly gaming engine [Panda3d](https://www.panda3d.org/). 
I use vertex shaders to move dots around and Windows 10. While Panda3D generally supports on all platforms, 
I did not manage to use shaders on platforms others than windows. Please let me know if you get it to run on Linux or MacOS.

## Installation
Install the latest Python 3. I am using the Anaconda distribution.

To install Anaconda, download the installer from the [Anaconda website](https://www.anaconda.com/distribution/#download-section).
Then go to the Anaconda Prompt and create a new environment:

    conda create --name py37 --channel conda-forge python=3.7
    conda activate py37
    conda install -c conda-forge scipy pyqt
    pip install panda3d
    
Get the source code from the repository and start the graphical user interface:

    git clone https://github.com/arminbahl/random_dot_motion
    cd random_dot_python
    python start_gui.py

This should give you two windows, one displaying the visual stimulus and one that controls stimulus features.

If you have any questions or suggestions, please let me know: [arminbahl@fas.harvard.edu](mailto:arminbahl@fas.harvard.edu)

## References
1.	Bahl, A., and Engert, F. (2020). Neural circuits for evidence accumulation and decision making in larval zebrafish. Nat. Neurosci. 23, 94–102.
2.	Newsome, W.T., and Paré, E.B. (1988). A selective impairment of motion perception following lesions of the middle temporal visual area (MT). J. Neurosci. 8, 2201–2211.