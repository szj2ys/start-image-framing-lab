# Two FFmpeg start-image recipes

These examples accept a **single JPEG with square pixels**, already oriented as intended. They produce one 720 × 1280 PNG. Use a new output filename: `-n` refuses to overwrite an existing one. FFmpeg support depends on the installed build.

## Fit the entire JPEG and add solid padding

```sh
ffmpeg -hide_banner -loglevel error -nostdin -n -f image2pipe -c:v mjpeg -i "square.jpg" -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=black" -frames:v 1 -update 1 "fit.png"
```

## Fill the destination with a centred crop

```sh
ffmpeg -hide_banner -loglevel error -nostdin -n -f image2pipe -c:v mjpeg -i "square.jpg" -vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280" -frames:v 1 -update 1 "crop.png"
```

The explicit input format and decoder keep the recipe compatible with the limited FFmpeg build used for this lab. Do not use that JPEG decoder setting for a PNG, WebP or HEIC source. On a full FFmpeg build, input autodetection is another option, but it was not the command tested here.

## Check the files

Run `framing_lab.py` to reproduce both commands on the included synthetic fixture. It checks the exported dimensions and coloured markers, not just the process exit code. For your own photo, inspect the silhouette, label and proportions in addition to checking file format and size.

PNG may exceed your destination service's upload limit. Select an appropriate export format and compression level for that service rather than assuming these example PNGs are ready for every model. Consult the actual provider route's current requirements; an app may impose a lower cap than the model's own API.

## Primary documentation

- [FFmpeg scale filter](https://ffmpeg.org/ffmpeg-filters.html#scale): aspect-preserving increase/decrease controls.
- [FFmpeg pad filter](https://ffmpeg.org/ffmpeg-filters.html#pad): output size, placement and fill colour.
- [FFmpeg crop filter](https://ffmpeg.org/ffmpeg-filters.html#crop): output window and placement.
- [FFmpeg command reference](https://ffmpeg.org/ffmpeg.html): input/output options, stream handling and overwrite controls.
- [FFmpeg image2 output](https://ffmpeg.org/ffmpeg-formats.html#image2-1): image output and single-filename update behavior.

Documentation was checked on 1 November 2026. The included result records the executable build actually used. These commands do not upload a file or call an AI service.
