# Verification and limits

The `examples/` directory contains actual output from running `framing_lab.py`, not illustrative replacements. The input is deliberately synthetic: a grey square, a wide green rectangle, red and blue ends, and a yellow centre marker. It contains no customer image, person, trademark or third-party photograph.

The script's report records its UTC run time and FFmpeg version. Its six assertions inspect both decoded output images: dimensions, marker colours, and top/bottom padding. The thresholds distinguish large colour blocks, not photographic colour fidelity.

The repository is intended to teach composition checks. It does not infer subject boundaries, identify products, score beauty, recognize labels, predict model acceptance or benchmark AI output.

## Website checks, separate from this lab

On 1 November 2026, a logged-out browser session tested imgmov's public resize utility with a separate synthetic 1200 × 1200 image. Crop, blurred fit and solid fit each downloaded a 720 × 1280 JPEG. The standalone last-frame utility exported the website's sample ending as a 704 × 704 PNG at 5.13 seconds. Those observations do not establish all-device compatibility or a successful AI generation.

That browser displayed an API Offline notice while the local utilities remained usable. This repository does not claim that imgmov generation, sign-in or payment services were available. The local FFmpeg exercise needs none of those services.

## Not covered

HDR and tone mapping; ICC/profile preservation; EXIF orientation; alpha/transparency; non-square pixels; HEIC; corrupt files; rotated video metadata; every FFmpeg/Pillow version; browser/mobile compatibility; and AI generation, pricing or commercial-rights review. The experiment uses only a JPEG source and PNG outputs. Do not generalize its marker counts to product photos or its output bytes to other pictures.

To report a reproduction problem, include your FFmpeg version, Python/Pillow versions, command, error output and the synthetic run's `result.json`. Keep access tokens, customer files and private paths out of public reports.
