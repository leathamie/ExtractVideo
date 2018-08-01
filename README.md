# Video splitter with ffmpeg
Both script create some video extracts, you can split videos into regular segments (with or without overlap) or follow a file that contains the cutting times.
## create_extracts_from_files.py
Small functions that cut out functions, they can be used for inspiration (for example to process text files that output motion detect), but each function only works in a very specific frame.
## create_extracts_with_overlap.py
Allows to cut videos into regular clips, it is designed to cut a large number of videos so waits in parameter a video folder and the path to the output folder. You can optionally specify:
- the duration of the extracts in seconds'-d', the default value is 4 seconds
- the overlap (in seconds)'-o' : by default 1 second
- the beginning of the cutting (in seconds)'-s': from when the cutting starts, by default we ignore the first 2 minutes of the video. (120 sec)
- the end of the cutting -e : by default we go to the end of the video
- a.cha"-cha'  file folder: videos in the CHILDES free corpus often have.cha files associated with the same name with speech transcription. If an.cha file is specified then the splitting will be done according to the beginning and the end of the transcription.

