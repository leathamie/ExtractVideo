# Video splitter with ffmpeg
Both script create some video extracts that launch themselves from the command line, you can split videos into regular segments (with or without overlap) or follow a file that contains the cutting times.
## Prerequisites
These scripts work with python 3 and ffmpeg 2.8.14 on ubuntu 16.04
## create_extracts_from_files.py
Small functions that cut out functions, they can be used for inspiration (for example to process text files that output motion detect), but each function only works in a very specific frame.


```
python create_extracts_from_files.py '/data/011100_7.22_8.6.txt' '/data/011100_7.22_8.6.mp4' '/data'
```

Arguments are processed in this order: file path with durations, video path to trim, output folder for cut videos.

## create_extracts_with_overlap.py
Allows to cut videos into regular clips, it is designed to cut a large number of videos so waits in parameter a video folder and the path to the output folder. You can optionally specify:

- the duration of the extracts in seconds'-d', the default value is 4 seconds
- the overlap (in seconds)'-o' : by default 1 second
- the beginning of the cutting (in seconds)'-s': from when the cutting starts, by default we ignore the first 2 minutes of the video. (120 sec)
- the end of the cutting -e : by default we go to the end of the video
- a.cha"-cha'  file folder: videos in the CHILDES free corpus often have.cha files associated with the same name with speech transcription. If an.cha file is specified then the splitting will be done according to the beginning and the end of the transcription.

Get details with -h in command line:

```
>>> python create_extracts_with_overlap.py -h
    usage: create_extracts_with_overlap.py [-h] [-i INPUT] [-o OUTPUT]
                                           [-d DURATION] [-ov OVERLAP] [-s START]
                                           [-e END] [-cha CHA]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            Video(s) folder path
      -o OUTPUT, --output OUTPUT
                            Videos extracts folder path
      -d DURATION, --duration DURATION
                            Exracts duration in seconds (default : 5sec)
      -ov OVERLAP, --overlap OVERLAP
                            Extracts overlap in seconds (default : 1.0)
      -s START, --start START
                            start of cutting in seconds (default: 0)
      -e END, --end END     start of cutting in seconds (default: file length)
      -cha CHA, --cha CHA   if a cha folder file is specified, the begin and the
                            and of the cutting will match with the corresponding
                            cha file
```

example of minimum input in command line:

```
python create_extracts_with_overlap.py -i'data/videos' -o'data/extracts'
```


