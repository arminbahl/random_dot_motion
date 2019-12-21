from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from multiprocessing import Process
import numpy as np
import os
import sys

dot_motion_coherence_shader = [
    """ #version 140

        uniform sampler2D p3d_Texture0;
        uniform mat4 p3d_ModelViewProjectionMatrix;

        in vec4 p3d_Vertex;
        in vec2 p3d_MultiTexCoord0;
        uniform int number_of_dots;
        uniform float size_of_dots;
        
        out float dot_color;

        void main(void) {
            vec4 newvertex;
            float dot_i;
            float dot_x, dot_y;
            float maxi = 10000.0;
            vec4 dot_properties;

            dot_i = float(p3d_Vertex[1]);
            dot_properties = texture2D(p3d_Texture0, vec2(dot_i/maxi, 0.0));

            dot_x = dot_properties[2];
            dot_y = dot_properties[1];
            dot_color = dot_properties[0];

            newvertex = p3d_Vertex;

            if (dot_x*dot_x + dot_y*dot_y > 1/1.4*1/1.4 || dot_i > number_of_dots) { // only plot a certain number of dots in a circle
                newvertex[0] = 0.0;
                newvertex[1] = 0.0;
                newvertex[2] = 0.0;
            } else {
                newvertex[0] = p3d_Vertex[0]*size_of_dots+dot_x;
                newvertex[1] = 0.75;
                newvertex[2] = p3d_Vertex[2]*size_of_dots+dot_y;
            }

            gl_Position = p3d_ModelViewProjectionMatrix * newvertex;
        }
    """,

    """ #version 140
        in float dot_color;
        //out vec4 gl_FragColor;

        void main() {
            gl_FragColor = vec4(dot_color, dot_color, dot_color, 1);
        }
    """
]

class MyApp(ShowBase):
    def __init__(self, shared):

        self.shared = shared

        loadPrcFileData("",
                        """fullscreen 0
                           win-origin 100 100
                           win-size 800 800
                           sync-video 0
                           undecorated 1
                           load-display pandagl""")

        ShowBase.__init__(self)

        ############
        # Update the lense
        self.disableMouse()
        self.setBackgroundColor(0, 0, 0, 1)

        ############
        # Compile the motion shader
        self.compiled_dot_motion_shader = Shader.make(Shader.SLGLSL, dot_motion_coherence_shader[0], dot_motion_coherence_shader[1])

        filepath = os.path.join(os.path.split(__file__)[0], "circles.bam")
        self.circles = self.loader.loadModel(Filename.fromOsSpecific(filepath))
        self.circles.reparentTo(self.render)
        self.circles.setShaderInput("number_of_dots", self.shared.stimulus_properties_number_of_dots.value)
        self.circles.setShaderInput("size_of_dots", self.shared.stimulus_properties_size_of_dots.value)

        self.dummytex = Texture("dummy texture")
        self.dummytex.setup2dTexture(10000, 1, Texture.T_float, Texture.FRgb32)
        self.dummytex.setMagfilter(Texture.FTNearest)

        ts1 = TextureStage("part2")
        ts1.setSort(-100)

        self.circles.setTexture(ts1, self.dummytex)
        self.circles.setShader(self.compiled_dot_motion_shader)

        self.dots_position = np.empty((1, 10000, 3)).astype(np.float32)
        self.dots_position[0, :, 0] = 2*np.random.random(10000).astype(np.float32) - 1 # x
        self.dots_position[0, :, 1] = 2*np.random.random(10000).astype(np.float32) - 1 # y
        self.dots_position[0, :, 2] = np.random.randint(0, 3, 10000).astype(np.float32)*0 + 1  # 0 will be black, 1, will be white, 2 will be hidden

        memoryview(self.dummytex.modify_ram_image())[:] = self.dots_position.tobytes()

        self.last_time = 0
        self.shared.stimulus_properties_update_requested.value = 1

        self.task_mgr.add(self.update_stimulus, "update_stimulus")

    def update_stimulus(self, task):

        #######
        # Listen to the commands coming from the gui
        if self.shared.running.value == 0:
            sys.exit()

        if self.shared.window_properties_update_requested.value == 1:
            self.shared.window_properties_update_requested.value = 0

            props = WindowProperties()
            props.setSize(self.shared.window_properties_height.value, self.shared.window_properties_width.value)
            props.setOrigin(self.shared.window_properties_x.value, self.shared.window_properties_y.value)

            self.win.requestProperties(props)

            self.lens = PerspectiveLens()
            self.lens.setFov(90, 90)
            self.lens.setNearFar(0.001, 1000)
            self.lens.setAspectRatio(self.shared.window_properties_height.value /
                                     self.shared.window_properties_width.value)

            self.cam.node().setLens(self.lens)

        if self.shared.stimulus_properties_update_requested.value == 1:
            self.shared.stimulus_properties_update_requested.value = 0

            random_vector = np.random.randint(100, size=10000)
            self.coherent_change_vector_ind = np.where(random_vector < self.shared.stimulus_properties_coherence_of_dots.value)

        #######
        # Continously update the dot stimulus
        dt = task.time - self.last_time
        self.last_time = task.time

        ######
        # Update the shader variables
        self.circles.setShaderInput("number_of_dots", self.shared.stimulus_properties_number_of_dots.value)
        self.circles.setShaderInput("size_of_dots", self.shared.stimulus_properties_size_of_dots.value)

        #####
        self.dots_position[0, :, 0][self.coherent_change_vector_ind] += np.cos(self.shared.stimulus_properties_direction_of_dots.value*np.pi/180) * \
                                                                        self.shared.stimulus_properties_speed_of_dots.value * \
                                                                        dt
        self.dots_position[0, :, 1][self.coherent_change_vector_ind] += np.sin(self.shared.stimulus_properties_direction_of_dots.value*np.pi/180) * \
                                                                        self.shared.stimulus_properties_speed_of_dots.value * \
                                                                        dt

        # Randomly redraw dot with a short lifetime
        k = np.random.random(10000)
        if self.shared.stimulus_properties_lifetime_of_dots.value == 0:
            ind = np.where(k >= 0)
        else:
            ind = np.where(k < dt / self.shared.stimulus_properties_lifetime_of_dots.value)[0]

        self.dots_position[0, :, 0][ind] = 2 * np.random.random(len(ind)).astype(np.float32) - 1  # x
        self.dots_position[0, :, 1][ind] = 2 * np.random.random(len(ind)).astype(np.float32) - 1  # y
        self.dots_position[0, :, 2][ind] = np.random.randint(0, 2, len(ind)).astype(np.float32)*0 + 1  # 0 will be black, 1, will be white,  # y

        # Wrap them
        self.dots_position[0, :, 0] = (self.dots_position[0, :, 0] + 1) % 2 - 1
        self.dots_position[0, :, 1] = (self.dots_position[0, :, 1] + 1) % 2 - 1

        memoryview(self.dummytex.modify_ram_image())[:] = self.dots_position.tobytes()

        return task.cont


class StimulusModule(Process):
    def __init__(self, shared):
        Process.__init__(self)

        self.shared = shared

    def run(self):
        app = MyApp(self.shared)
        app.run()