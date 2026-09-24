"""Generate the 3-panel press-release figure for the UCSC announcement.

Panel 1: APF/Levy ThAr echelle frame in grey scale (cleaned, stretched)
Panel 2: the Claude logo
Panel 3: the same ThAr frame with every pixel colored by its wavelength

Wavelengths come from a PypeIt calibration run on the APF/Levy bin2 data
(ThAr arc + WideFlats). Produce those calibrations first, from this directory:

    conda run -n pypeit14 run_pypeit apf_levy_bin2.pypeit -c -r redux -o

then make the figure:

    conda run -n pypeit14 python make_pr_figure.py

The figure is illustrative: the coloring maps wavelength to an approximate
perceived RGB color, and it fades to deep violet / deep red at the ends of
the APF coverage (~3790-6910 A).
"""

import argparse
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.image import imread
from scipy.ndimage import distance_transform_edt, gaussian_filter, percentile_filter

from pypeit import slittrace, wavecalib, wavetilts
from pypeit.images.buildimage import ArcImage

HERE = os.path.dirname(os.path.abspath(__file__))


def wavelength_to_rgb(wave):
    """Approximate perceived RGB color for air wavelengths in Angstroms.

    Piecewise-linear visible-spectrum approximation (after Dan Bruton). Outside
    the ~3800-7000 A range the hue is held fixed and the brightness fades, so
    the UV end goes to deep violet and the red end to deep red.

    Args:
        wave (np.ndarray): Wavelengths in Angstroms (any shape).

    Returns:
        np.ndarray: RGB values in [0, 1], shape ``wave.shape + (3,)``.
    """
    w = np.clip(np.asarray(wave, dtype=float) / 10., 380., 750.)  # nm
    r = np.zeros_like(w)
    g = np.zeros_like(w)
    b = np.zeros_like(w)

    m = w < 440
    r[m], b[m] = (440 - w[m]) / (440 - 380), 1.
    m = (w >= 440) & (w < 490)
    g[m], b[m] = (w[m] - 440) / (490 - 440), 1.
    m = (w >= 490) & (w < 510)
    g[m], b[m] = 1., (510 - w[m]) / (510 - 490)
    m = (w >= 510) & (w < 580)
    r[m], g[m] = (w[m] - 510) / (580 - 510), 1.
    m = (w >= 580) & (w < 645)
    r[m], g[m] = 1., (645 - w[m]) / (645 - 580)
    m = w >= 645
    r[m] = 1.

    # Brightness fade toward the ends of the coverage
    wnm = np.asarray(wave, dtype=float) / 10.
    fade = np.ones_like(wnm)
    blue = wnm < 420
    fade[blue] = 0.35 + 0.65 * np.clip((wnm[blue] - 375) / (420 - 375), 0, 1)
    red = wnm > 650
    fade[red] = 0.45 + 0.55 * np.clip((710 - wnm[red]) / (710 - 650), 0, 1)

    rgb = np.stack([r, g, b], axis=-1) * fade[..., None]
    # Mild gamma so the mid-spectrum does not look washed out
    return rgb ** 0.8


def load_calibrations(calib_dir, setup='A_0_DET01'):
    """Load the processed arc image and build its wavelength image.

    Returns:
        tuple: (arc image, wavelength image, slit mask); all 2D arrays in the
        PypeIt frame (spectral axis along rows).
    """
    arc = ArcImage.from_file(os.path.join(calib_dir, f'Arc_{setup}.fits'),
                             chk_version=False)
    slits = slittrace.SlitTraceSet.from_file(
        os.path.join(calib_dir, f'Slits_{setup}.fits.gz'), chk_version=False)
    tilts = wavetilts.WaveTilts.from_file(
        os.path.join(calib_dir, f'Tilts_{setup}.fits'), chk_version=False)
    wv_calib = wavecalib.WaveCalib.from_file(
        os.path.join(calib_dir, f'WaveCalib_{setup}.fits'), chk_version=False)
    wv_calib.chk_synced(slits)

    slitmask = slits.slit_img()
    tilt_img = tilts.fit2tiltimg(slitmask)
    waveimg = wv_calib.build_waveimg(tilt_img, slits)
    return arc.image.astype(float), waveimg, slitmask


def clean_arc(image, box=(61, 3), pct=20., smooth=4.):
    """Remove the scattered-light / continuum background and clip negatives.

    The APF orders abut one another, so there are no clean inter-order pixels.
    Instead, because ThAr lines are sparse along each order, the background
    is a running low percentile along the dispersion direction (axis 0),
    lightly smoothed.
    """
    bkg = percentile_filter(image, pct, size=box, mode='nearest')
    bkg = gaussian_filter(bkg, smooth)
    return np.clip(image - bkg, 0., None)


def stretch(image, soften, vmax_pct):
    """asinh stretch to [0, 1]."""
    vmax = np.percentile(image[image > 0], vmax_pct)
    image = np.clip(image, 0., vmax)
    return np.clip(np.arcsinh(image / soften) / np.arcsinh(vmax / soften), 0., 1.)


def orient(arr, waveimg):
    """Put the spectral axis along x, red orders at the top, blue to the right.

    ``arr`` may carry trailing (e.g. RGB) axes.
    """
    out = np.swapaxes(arr, 0, 1)
    wv = np.swapaxes(waveimg, 0, 1)
    good = wv > 0
    # Rows: red on top (row 0 is drawn at the top with origin='upper')
    rows = np.where(good.any(axis=1))[0]
    if np.median(wv[rows[0]][good[rows[0]]]) < np.median(wv[rows[-1]][good[rows[-1]]]):
        out, wv, good = out[::-1], wv[::-1], good[::-1]
    # Columns: wavelength increasing left to right within an order
    irow = rows[len(rows) // 2]
    cols = np.where(good[irow])[0]
    if wv[irow, cols[0]] > wv[irow, cols[-1]]:
        out = out[:, ::-1]
    return out


def logo_symbol(logo_file, pad=0.04):
    """Recolor the Claude logo tile: orange symbol on a transparent background.

    The tile is a light symbol on an orange square. The symbol's opacity is
    taken from how far each pixel lies from the orange toward the light color,
    which keeps the anti-aliased edges; the symbol is filled with the tile's
    orange. The result is cropped to the symbol plus a small pad.

    Returns:
        np.ndarray: RGBA image in [0, 1].
    """
    im = imread(logo_file).astype(float)
    if im.max() > 1.:
        im /= 255.
    im = im[..., :3]
    orange = np.median(im[:10, :10].reshape(-1, 3), axis=0)
    light = np.percentile(im.reshape(-1, 3), 99, axis=0)
    # Project each pixel onto the orange -> light line
    axis = light - orange
    alpha = np.clip(((im - orange) @ axis) / (axis @ axis), 0., 1.)

    rgba = np.zeros(im.shape[:2] + (4,))
    rgba[..., :3] = orange
    rgba[..., 3] = alpha

    rows = np.where((alpha > 0.5).any(axis=1))[0]
    cols = np.where((alpha > 0.5).any(axis=0))[0]
    npad = int(pad * im.shape[0])
    r0, r1 = max(rows[0] - npad, 0), min(rows[-1] + npad + 1, im.shape[0])
    c0, c1 = max(cols[0] - npad, 0), min(cols[-1] + npad + 1, im.shape[1])
    return rgba[r0:r1, c0:c1]


def pypeit_on_light(logo_file, sat_cut=0.1, alpha_cut=0.15):
    """Key the PypeIt logo (white text + colored curve on black) for a light page.

    The black background becomes transparent. Unsaturated (white / grey)
    pixels, i.e. the text and its anti-aliased edges, become black, with
    opacity set by their brightness. Saturated pixels, i.e. the colored
    spectrum curve, keep their color. The result is cropped to the content.

    Returns:
        np.ndarray: RGBA image in [0, 1].
    """
    im = imread(logo_file).astype(float)
    if im.max() > 1.:
        im /= 255.
    rgb = im[..., :3]
    vmax = rgb.max(axis=-1)
    sat = np.where(vmax > 0, (vmax - rgb.min(axis=-1)) / np.clip(vmax, 1e-6, None), 0.)
    w_text = 1. - np.clip(sat / sat_cut, 0., 1.)       # 1 = text, 0 = curve

    a_curve = np.clip(vmax / alpha_cut, 0., 1.)
    alpha = w_text * vmax + (1. - w_text) * a_curve
    curve_rgb = np.clip(rgb / np.clip(a_curve, 1e-6, None)[..., None], 0., 1.)

    rgba = np.zeros(rgb.shape[:2] + (4,))
    rgba[..., :3] = (1. - w_text)[..., None] * curve_rgb   # text -> black
    rgba[..., 3] = alpha

    rows = np.where((alpha > 0.5).any(axis=1))[0]
    cols = np.where((alpha > 0.5).any(axis=0))[0]
    return rgba[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


def two_panel_figure(grey, color, args, height_in=4., fill=0.9,
                     gap_in=0.25, margin_in=0.15):
    """Before/after figure: grey spectrum (left), wavelength-colored (right).

    The figure is ``height_in`` tall; its width follows from the aspect ratio
    of the spectra so the panels fill it with no wasted space.
    """
    panel_h = fill * height_in
    panel_w = panel_h * grey.shape[1] / grey.shape[0]
    width_in = 2 * margin_in + 2 * panel_w + gap_in
    fig = plt.figure(figsize=(width_in, height_in), facecolor=args.bg)
    y0 = (1. - fill) / 2.
    for x_in, img, kw in [(margin_in, grey, dict(cmap='gray', vmin=0., vmax=1.)),
                          (margin_in + panel_w + gap_in, color, {})]:
        ax = fig.add_axes([x_in / width_in, y0, panel_w / width_in, fill])
        ax.imshow(img, interpolation='antialiased', **kw)
        ax.set_axis_off()
    fig.savefig(args.outfile, dpi=args.dpi, facecolor=args.bg)
    print(f'Wrote {args.outfile} ({width_in:.2f} x {height_in:.2f} in)')


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--calib_dir', default=os.path.join(HERE, 'redux', 'Calibrations'),
                        help='PypeIt Calibrations directory')
    parser.add_argument('--logo', default=os.path.join(HERE, 'claude_logo.jpeg'),
                        help='Claude logo image')
    parser.add_argument('--pypeit_logo',
                        default=os.path.join(HERE, 'PypeIt_color_white_txt_black_background.png'),
                        help='PypeIt logo image (white text on black); shown '
                             'under the Claude logo. Pass "none" to omit it')
    parser.add_argument('--outfile', default=None,
                        help='Output PNG [default: pr_figure.png, or '
                             'pr_figure_2panels.png with --two_panel]')
    parser.add_argument('--two_panel', action='store_true',
                        help='Before/after version: only the grey and color '
                             'spectra, side by side (no arrows or logos)')
    parser.add_argument('--spec_frac', type=float, default=0.4,
                        help='Fraction of each order (centered) to show along the '
                             'dispersion direction; <1 enlarges the lines')
    parser.add_argument('--soften', type=float, default=150.,
                        help='asinh softening (counts); smaller brings up faint lines')
    parser.add_argument('--vmax_pct', type=float, default=99.8,
                        help='Percentile of positive pixels mapped to full brightness')
    parser.add_argument('--bg', default='white', help='Figure background color')
    parser.add_argument('--logo_tile', action='store_true',
                        help='Show the original logo tile (light symbol on an '
                             'orange square) instead of the orange symbol')
    parser.add_argument('--dpi', type=int, default=300)
    args = parser.parse_args()
    if args.outfile is None:
        args.outfile = os.path.join(
            HERE, 'pr_figure_2panels.png' if args.two_panel else 'pr_figure.png')

    image, waveimg, _ = load_calibrations(args.calib_dir)
    # Fill the small gaps between adjacent traced orders (within the span of
    # calibrated orders on each spectral row) with the nearest wavelength
    cal = waveimg > 0
    spat = np.arange(cal.shape[1])
    lo = np.where(cal.any(axis=1), np.argmax(cal, axis=1), cal.shape[1])
    hi = cal.shape[1] - 1 - np.argmax(cal[:, ::-1], axis=1)
    on_order = (spat[None, :] >= lo[:, None]) & (spat[None, :] <= hi[:, None])
    _, inds = distance_transform_edt(~cal, return_indices=True)
    waveimg = np.where(on_order, waveimg[tuple(inds)], 0.)

    clean = clean_arc(image)
    clean[~on_order] = 0.   # only the wavelength-calibrated orders are shown
    inten = stretch(clean, args.soften, args.vmax_pct)

    # Color panel: intensity x wavelength color
    rgb = wavelength_to_rgb(np.where(on_order, waveimg, 5500.)) * inten[..., None]

    # Orient all layers together: grey, R, G, B, wavelength
    stack = orient(np.dstack([inten, rgb, waveimg]), waveimg)

    # Crop to the calibrated orders (spatial) and the central spec_frac
    # of each order (dispersion)
    nspec = stack.shape[1]
    ncrop = int(round(nspec * (1 - args.spec_frac) / 2))
    stack = stack[:, ncrop:nspec - ncrop]
    rows = np.where((stack[..., 4] > 0).all(axis=1))[0]
    stack = stack[rows[0]:rows[-1] + 1]
    grey = stack[..., 0]
    color = stack[..., 1:4]

    if args.two_panel:
        two_panel_figure(grey, color, args)
        return

    # ------------------------------------------------------------------
    # Figure: 12 x 4 in, three horizontal panels with arrows between them
    fig = plt.figure(figsize=(12., 4.), facecolor=args.bg)
    aspect = grey.shape[0] / grey.shape[1]   # height / width of the spectra
    show_pypeit = args.pypeit_logo.lower() != 'none'
    logo_w = 0.17 if show_pypeit else 0.15   # middle column width
    # Spectra as tall as possible (<=86% of the figure) while leaving
    # room for the logo, >=7% gaps for the arrows and 2% outer margins
    margin = 0.02
    spec_w = min(0.86 * 4. / 12. / aspect, (1. - logo_w - 2 * margin - 2 * 0.07) / 2.)
    height = spec_w * aspect * 12. / 4.
    gap = (1. - 2 * margin - 2 * spec_w - logo_w) / 2.
    y0 = (1. - height) / 2.

    x1 = margin
    x2 = x1 + spec_w + gap
    x3 = x2 + logo_w + gap
    ax1 = fig.add_axes([x1, y0, spec_w, height])
    ax3 = fig.add_axes([x3, y0, spec_w, height])

    # Middle column: Claude symbol, with the PypeIt logo stacked beneath it;
    # the stack is centered vertically on the spectra
    claude = imread(args.logo) if args.logo_tile else logo_symbol(args.logo)
    logo_axes = []
    if show_pypeit:
        pypeit = pypeit_on_light(args.pypeit_logo)
        claude_w = 0.75 * logo_w                          # figure fractions
        claude_h = claude_w * 12. / 4. * claude.shape[0] / claude.shape[1]
        pyp_h = logo_w * 12. / 4. * pypeit.shape[0] / pypeit.shape[1]
        vgap = 0.05
        ytop = 0.5 + (claude_h + vgap + pyp_h) / 2.
        ax2 = fig.add_axes([x2 + (logo_w - claude_w) / 2., ytop - claude_h, claude_w, claude_h])
        ax2b = fig.add_axes([x2, ytop - claude_h - vgap - pyp_h, logo_w, pyp_h])
        ax2b.imshow(pypeit, interpolation='antialiased')
        logo_axes.append(ax2b)
    else:
        logo_h = logo_w * 12. / 4.
        ax2 = fig.add_axes([x2, 0.5 - logo_h / 2., logo_w, logo_h])
    ax2.imshow(claude, interpolation='lanczos')
    logo_axes.append(ax2)

    ax1.imshow(grey, cmap='gray', vmin=0., vmax=1., interpolation='antialiased')
    ax3.imshow(color, interpolation='antialiased')
    for ax in [ax1, ax3] + logo_axes:
        ax.set_axis_off()

    # Arrows: grey -> Claude -> color
    arrow_kw = dict(transform=fig.transFigure, arrowstyle='-|>', mutation_scale=22,
                    lw=2.5, color='white' if args.bg == 'black' else 'black')
    pad = 0.012
    x_ends = [(x1 + spec_w + pad, x2 - pad), (x2 + logo_w + pad, x3 - pad)]
    for xa, xb in x_ends:
        fig.patches.append(FancyArrowPatch((xa, 0.5), (xb, 0.5), **arrow_kw))

    fig.savefig(args.outfile, dpi=args.dpi, facecolor=args.bg)
    print(f'Wrote {args.outfile}')


if __name__ == '__main__':
    main()
