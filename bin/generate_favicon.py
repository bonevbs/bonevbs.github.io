#!/usr/bin/env python3
"""Build site favicon from a Zernike polynomial surface on the unit disk."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img"

# OSA/ANSI standard: Z_n^m, n >= |m|, (n - |m|) even
ZERNKE_N = 4
ZERNKE_M = 4

# MATLAB parula (sRGB), piecewise-linear between anchor stops
_PARULA_STOPS: tuple[tuple[float, tuple[float, float, float]], ...] = (
    (0.000, (0.2422, 0.1504, 0.6603)),
    (0.031, (0.2470, 0.1553, 0.6728)),
    (0.063, (0.2539, 0.1649, 0.6860)),
    (0.094, (0.2610, 0.1777, 0.7067)),
    (0.125, (0.2679, 0.1916, 0.7283)),
    (0.156, (0.2741, 0.2064, 0.7518)),
    (0.188, (0.2801, 0.2199, 0.7749)),
    (0.219, (0.2803, 0.2333, 0.8014)),
    (0.250, (0.2803, 0.2782, 0.9221)),
    (0.281, (0.2758, 0.3218, 0.9357)),
    (0.313, (0.2689, 0.3636, 0.9165)),
    (0.344, (0.2600, 0.4039, 0.8948)),
    (0.375, (0.2440, 0.4354, 0.8800)),
    (0.406, (0.2237, 0.4695, 0.8642)),
    (0.438, (0.2044, 0.5025, 0.8484)),
    (0.469, (0.1855, 0.5328, 0.8331)),
    (0.500, (0.1551, 0.5902, 0.8068)),
    (0.531, (0.1300, 0.6246, 0.7855)),
    (0.563, (0.1078, 0.6549, 0.7656)),
    (0.594, (0.0872, 0.6816, 0.7464)),
    (0.625, (0.0773, 0.6903, 0.6647)),
    (0.656, (0.0695, 0.7088, 0.5771)),
    (0.688, (0.0619, 0.7238, 0.4922)),
    (0.719, (0.0660, 0.7366, 0.4248)),
    (0.750, (0.0690, 0.7487, 0.4996)),
    (0.781, (0.1144, 0.7512, 0.4243)),
    (0.813, (0.1673, 0.7488, 0.3587)),
    (0.844, (0.2250, 0.7412, 0.3046)),
    (0.875, (0.2918, 0.7295, 0.2588)),
    (0.906, (0.3840, 0.7073, 0.2165)),
    (0.938, (0.4960, 0.6789, 0.1802)),
    (0.969, (0.6624, 0.6163, 0.1280)),
    (1.000, (0.9769, 0.9839, 0.0805)),
)


def parula_cmap() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list("parula", list(_PARULA_STOPS), N=256)


def zernike_radial(n: int, m: int, rho: np.ndarray) -> np.ndarray:
    """Radial part R_n^|m|(rho) on the unit disk."""
    m = abs(m)
    if (n - m) % 2 != 0 or n < m:
        raise ValueError(f"invalid Zernike indices n={n}, m={m}")
    r = np.zeros_like(rho, dtype=float)
    for k in range((n - m) // 2 + 1):
        num = math.factorial(n - k)
        den = (
            math.factorial(k)
            * math.factorial((n + m) // 2 - k)
            * math.factorial((n - m) // 2 - k)
        )
        coeff = (-1) ** k * num / den
        r += coeff * rho ** (n - 2 * k)
    return r


def zernike(n: int, m: int, rho: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Zernike polynomial Z_n^m on polar grid (OSA/ANSI convention)."""
    radial = zernike_radial(n, m, rho)
    if m > 0:
        return radial * np.cos(m * phi)
    if m < 0:
        return radial * np.sin(-m * phi)
    return radial


def zernike_on_disk(n: int, m: int, n_radial: int = 140, n_azimuth: int = 280) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample Z_n^m on the unit disk (polar grid, circular boundary)."""
    rho = np.linspace(0.0, 1.0, n_radial)
    phi = np.linspace(0.0, 2.0 * np.pi, n_azimuth, endpoint=False)
    R, P = np.meshgrid(rho, phi, indexing="ij")
    X = R * np.cos(P)
    Y = R * np.sin(P)
    Z = zernike(n, m, R, P)
    peak = np.max(np.abs(Z))
    if peak > 0:
        Z /= peak
    return X, Y, Z


def render_surface_png(path: Path, size: int = 800, n: int = ZERNKE_N, m: int = ZERNKE_M) -> None:
    """Render Z_n^m on the unit disk; no axes."""
    X, Y, Z = zernike_on_disk(n, m)
    zmin, zmax = float(np.min(Z)), float(np.max(Z))

    fig = plt.figure(figsize=(size / 100, size / 100), dpi=100, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    norm = Normalize(vmin=zmin, vmax=zmax)
    ax.plot_surface(
        X,
        Y,
        Z,
        cmap=parula_cmap(),
        norm=norm,
        vmin=zmin,
        vmax=zmax,
        linewidth=0,
        antialiased=True,
        rstride=2,
        cstride=2,
        shade=False,  # flat shading: face color from Z only (no lighting)
    )
    ax.view_init(elev=32, azim=-52)
    ax.set_axis_off()
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_visible(False)
    ax.grid(False)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(zmin, zmax)
    ax.set_box_aspect((1, 1, 0.55))
    plt.subplots_adjust(0, 0, 1, 1, 0)
    fig.savefig(path, dpi=100, facecolor="white", transparent=False, pad_inches=0.02)
    plt.close(fig)


def to_favicon(master: Path) -> None:
    im = Image.open(master).convert("RGBA")
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 252 and g > 252 and b > 252:
                continue
            xs.append(x)
            ys.append(y)
    pad = 6
    x0, x1 = max(0, min(xs) - pad), min(w, max(xs) + pad)
    y0, y1 = max(0, min(ys) - pad), min(h, max(ys) + pad)
    crop = im.crop((x0, y0, x1, y1))
    cw, ch = crop.size
    side = max(cw, ch)
    square = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    square.paste(crop, ((side - cw) // 2, (side - ch) // 2))

    rgb = square.convert("RGB")
    size = 512
    rgb = rgb.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), radius=int(size * 0.22), fill=255)
    icon = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    icon.paste(rgb, (0, 0), mask)

    icon32 = icon.resize((32, 32), Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    icon32.save(OUT / "favicon.png")
    icon32.save(OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)])
    icon.save(OUT / "site-icon-512.png")
    print(f"Wrote {OUT / 'favicon.png'} (Z_{ZERNKE_N}^{ZERNKE_M})")


def main() -> None:
    master = OUT / "site-icon-source.png"
    render_surface_png(master)
    to_favicon(master)


if __name__ == "__main__":
    main()
