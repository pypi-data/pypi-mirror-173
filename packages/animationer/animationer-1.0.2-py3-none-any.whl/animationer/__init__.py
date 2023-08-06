import time as _time
import os as _os

def move(x, y):
    print("\033[%d;%dH" % (y, x), end="")

def playanimation(frames=["default animation", "DEFAULT ANIMATION"], fps=4, x=0, y=0, width=17, height=1, loop=1, experimental_autoheight=False):
    newframes = []
    if experimental_autoheight:
        realh = 0
        for f in frames:
            newlines = f.count("\n")
            if newlines > realh:
                realh = newlines
    else:
        realh = height
    for l in range(loop):
        for frame in frames:
            newframes.append(frame.replace("\n", "\n" + " "*x))
        for t in newframes:
            for i in range(realh+2):
                move(x, y+i-1)
                sizex, sizey = _os.get_terminal_size()
                print(" "*(width), end="")
            move(x, y)
            print("\r"+" "*x + t, end="")
            _time.sleep(1/fps)

if __name__ == "__main__":
    playanimation()
    playanimation()
    playanimation()
    playanimation()
    playanimation()
    playanimation()