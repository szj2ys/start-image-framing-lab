# Calculate what the crop removes

Start with source dimensions `Ws × Hs` and destination dimensions `Wt × Ht`. These formulas assume square pixels, no rotation transform, and a centred placement.

## Fit

The scale factor is the smaller of `Wt / Ws` and `Ht / Hs`.

```text
fit_scale = min(Wt / Ws, Ht / Hs)
rendered_width = Ws * fit_scale
rendered_height = Hs * fit_scale
left_and_right_padding = (Wt - rendered_width) / 2
top_and_bottom_padding = (Ht - rendered_height) / 2
```

For 1200 × 1200 into 720 × 1280, the factor is 0.6. The image becomes 720 × 720, leaving 280 pixels above and below. The original image's whole width remains present. That says nothing about whether a label remains readable after scaling down.

## Fill by cropping

The scale factor is the larger of those ratios.

```text
crop_scale = max(Wt / Ws, Ht / Hs)
visible_source_width = Wt / crop_scale
visible_source_height = Ht / crop_scale
source_left = (Ws - visible_source_width) / 2
source_top = (Hs - visible_source_height) / 2
```

The square example scales by 1280/1200. Its visible source width is 675 pixels; the source's left 262.5 and right 262.5 pixels fall outside the centred frame. The full source height remains visible.

## Separate subject coverage from image coverage

A photograph contains both the subject and its surroundings. Losing 43.75% of the photo's width is not the same as losing 43.75% of the product.

Suppose the essential subject spans x = 120 through 1080, a width of 960. Its overlap with the centred crop is 675 pixels. The crop therefore retains about 70.31% of this subject's horizontal extent, even though it retains 56.25% of the photo's width. These are example calculations, not image-recognition results.

For a rectangular subject boundary `[left, top, right, bottom]`, compare each edge with the visible source rectangle. If the subject's width exceeds the visible source width, sliding the crop cannot preserve its entire width. Repositioning helps only when the required region can fit inside the crop.

## Try a genuinely different starting picture

A landscape arrangement may fit poorly in a portrait frame even with padding. If the product becomes too small, photograph it with the final orientation in mind or use a closer source crop that removes unnecessary surroundings before fitting.

Do not stretch the original to the destination dimensions to conceal the mismatch. A wider handle or thinner package changes the depicted proportions. Similarly, padding cannot supply a missing back view, correct an obscured label or create factual evidence of product performance.

Use the exported picture as the decision surface. Compare it at the size your viewer will see, not only while zoomed in on a large screen. If two treatments both retain the important parts, choose based on composition and readability rather than assuming a larger image file is more accurate.
