import animationer as anim
import os

os.system("clear")

frames = [
    """cool test
animation""","""cool test
animation""",
    """ colt8t
  aiatin""",
"""   cot
   ain""",
    """
""","""
""",
    """   cot
   ain""",
    """  colt8t
 aiatin"""
]

anim.playanimation(loop=4, frames=frames, width=9, height=2, x=0, y=0, fps=10)