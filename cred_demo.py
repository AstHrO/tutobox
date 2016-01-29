#!/usr/bin/env python

from moviepy.editor import *
from moviepy.video.tools.credits import credits1

# Load the mountains clip, cut it, slow it down, make it look darker
clip = (VideoFileClip('tmp/output.avi', audio=False))
           

# Generate the credits from a text file
credits = credits1('settings/credits.txt',3*clip.w/4,gap=10,fontsize=20,color="white")
scrolling_credits = credits.set_pos(lambda t:('center',-10*t)).set_start(3).crossfadein(1)
titre = TextClip(txt="Tuto XXX", color="white",bg_color="black",fontsize=20).set_pos((80,15))
logo = ImageClip("settings/logo.png").set_pos((0,0)).resize(height=50)

final = CompositeVideoClip([clip,logo,scrolling_credits,titre])
                            
final.subclip(0,20).write_videofile("output/logo.mp4",fps=20)