import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Animation:
    def __init__(self, data, description=None):
        self.fig = plt.figure(facecolor="white")
        self.im = None
        self.data = data
        self.description = description

    def init(self):
        self.max_length = None
        frame = self.data[0]
        self.im = plt.imshow(frame)
        self.title = plt.title(self.description)
        return (self.im,)

    def update(self, frame_no):
        frame = self.data[frame_no]
        self.im.set_data(frame)
        return (self.im,)

    def play(self):
        self.max_length = len(self.data)
        self.ani = FuncAnimation(
            self.fig,
            self.update,
            frames=self.max_length,
            init_func=self.init,
            blit=True,
            interval=20,
        )
        plt.show()

    @classmethod
    def play_sample(cls, data, description=None):
        animation = cls(data, description=description)
        animation.play()
