"""Create an original framing fixture and verify actual FFmpeg output pixels."""
import argparse
import datetime
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


FILTERS = {
    'fit': 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=black',
    'crop': 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280',
}


def make_fixture(path: Path) -> None:
    image = Image.new('RGB', (1200, 1200), (230, 230, 230))
    draw = ImageDraw.Draw(image)
    draw.rectangle((120, 400, 1079, 799), fill=(35, 150, 60))
    draw.rectangle((120, 400, 239, 799), fill=(220, 40, 40))
    draw.rectangle((960, 400, 1079, 799), fill=(40, 60, 220))
    draw.rectangle((580, 580, 619, 619), fill=(250, 220, 30))
    image.save(path, quality=95, subsampling=0)


def run_recipe(ffmpeg: str, source: Path, target: Path, mode: str) -> dict:
    args = [
        ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n',
        '-f', 'image2pipe', '-c:v', 'mjpeg', '-i', str(source),
        '-vf', FILTERS[mode], '-frames:v', '1', '-update', '1', str(target),
    ]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError(f'{mode} export failed: {result.stderr.strip()}')
    if not target.is_file():
        raise RuntimeError(f'{mode} exited successfully but created no image')
    return {'filter': FILTERS[mode], 'returncode': result.returncode}


def inspect(path: Path) -> dict:
    with Image.open(path) as opened:
        image = opened.convert('RGB')
        if image.size != (720, 1280):
            raise RuntimeError(f'{path.name} has unexpected dimensions: {image.size}')
        red = blue = 0
        for r, g, b in image.get_flattened_data():
            red += r > 150 and r > 2 * g and r > 2 * b
            blue += b > 150 and b > 2 * r and b > 2 * g
        return {
            'format': opened.format,
            'pixels': list(image.size),
            'red_marker_pixels': red,
            'blue_marker_pixels': blue,
            'top_pixel_rgb': list(image.getpixel((360, 20))),
            'bottom_pixel_rgb': list(image.getpixel((360, 1260))),
            'bytes': path.stat().st_size,
        }


def verify(output: Path, ffmpeg: str) -> dict:
    version = subprocess.run([ffmpeg, '-version'], capture_output=True, text=True, timeout=15)
    if version.returncode:
        raise RuntimeError('FFmpeg version check failed')
    source = output / 'square-markers.jpg'
    make_fixture(source)
    results = {}
    for mode in FILTERS:
        target = output / f'{mode}.png'
        recipe = run_recipe(ffmpeg, source, target, mode)
        results[mode] = {**recipe, **inspect(target)}
    fit, crop = results['fit'], results['crop']
    checks = {
        'fit_dimensions': fit['pixels'] == [720, 1280],
        'crop_dimensions': crop['pixels'] == [720, 1280],
        'fit_keeps_both_edge_markers': fit['red_marker_pixels'] > 1000 and fit['blue_marker_pixels'] > 1000,
        'crop_removes_both_edge_markers': crop['red_marker_pixels'] == 0 and crop['blue_marker_pixels'] == 0,
        'fit_adds_black_padding': max(fit['top_pixel_rgb'] + fit['bottom_pixel_rgb']) <= 3,
        'crop_has_no_black_padding': min(crop['top_pixel_rgb'] + crop['bottom_pixel_rgb']) >= 180,
    }
    report = {
        'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'ffmpeg': version.stdout.splitlines()[0],
        'input_pixels': [1200, 1200],
        'fixture': 'Original synthetic calibration image; not a product photo or an AI result.',
        'geometry': {'fit_padding_top_and_bottom_px': 280, 'crop_source_x_interval': [262.5, 937.5], 'crop_source_width_retained_percent': 56.25},
        'outputs': results,
        'checks': checks,
        'passed': all(checks.values()),
    }
    (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if not report['passed']:
        raise RuntimeError('Pixel checks failed; inspect result.json and the exported files')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default='ffmpeg', help='FFmpeg executable name or absolute path')
    parser.add_argument('--out', type=Path, default=Path('lab-output'), help='New output directory; existing paths are refused')
    args = parser.parse_args()
    if args.out.exists():
        parser.error('Output directory already exists; choose a new --out path')
    args.out.mkdir(parents=True)
    try:
        result = verify(args.out, args.ffmpeg)
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps({'passed': result['passed'], 'checks': len(result['checks']), 'output': str(args.out)}))


if __name__ == '__main__':
    main()
