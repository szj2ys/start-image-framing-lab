# Start-image handoff worksheet

Copy this worksheet into your project notes. Leave an unknown field unknown. Do not include confidential filenames or customer media in a public issue.

## Source and intent

- Source filename or internal asset ID:
- Permission to edit/use it confirmed by:
- Source dimensions, format and orientation:
- Destination tool and provider route:
- Intended output shape:
- Important subject parts that must remain visible:
- Approximate subject rectangle in source pixels:

## Two-file comparison

| Check | Crop export | Fit export |
| --- | --- | --- |
| Filename | | |
| Exact output pixels | | |
| File type and bytes | | |
| Whole required silhouette visible? | | |
| Label/identity details readable? | | |
| Proportions match the source? | | |
| Padding is acceptable as visible scenery? | Not applicable | |
| Subject clear at expected viewing size? | | |
| Current destination input requirements checked? | | |

## Decision

- Chosen file and reason:
- Rejected version and the actual defect:
- Need a different source composition? Why:
- Reviewer and review date:

## After a generation test

Record this separately from input preparation. A correct input file does not establish that the generated clip is correct.

- Product identity or colour changed?
- Label, handle, lid or corners changed?
- Added padding became distracting motion or scenery?
- Important parts left the frame during motion?
- Commercial-use and delivery requirements checked for the selected service?
- Keep, revise one input variable, or reject?

For an existing video's continuation frame, extract and inspect that frame first, then apply this geometry worksheet. The [imgmov last-frame utility](https://imgmov.com/extract-last-frame-from-video) is one browser option; the separate [frame-timing lab](https://github.com/szj2ys/video-frame-extraction-lab) explains duration and frame-index pitfalls. This repository does not re-test either workflow.
