import matplotlib.pyplot as plt
import pandas as pd
import imageio.v2 as imageio
import numpy as np
import io
from collections import defaultdict
from typing import Dict
import argparse
import contextily as ctx  # Added for basemap
from pyproj import CRS, Transformer
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import os


def parse_to_df(filename: str) -> Dict[str, pd.DataFrame]:
    with open(filename, 'r') as f:
        lines = f.readlines()

    data = defaultdict(list)
    for line in lines:
        if line.startswith('*') or not line.strip():
            continue
        parts = line.split()
        try:
            x = float(parts[0])
            y = float(parts[1])
            conc = float(parts[2])
            # Use ZELEV from column 6 (index 5)
            zelev = float(parts[5])
            date = parts[10].strip()
            year, month, day, hour = date[:2], date[2:4], date[4:6], date[6:8]
            date = f"20{year}-{month}-{day} {hour}:00:00"
            data[date].append((x, y, zelev, conc, year, month, day, hour))
        except ValueError:
            print(f"Skipping line due to parsing error: {line.strip()}")
            continue

    # Only keep rows where zelev == 84.85 (layer 1)
    result = {}
    for date in data:
        df = pd.DataFrame(data[date], columns=['X', 'Y', 'ZELEV', 'CONC', 'YEAR', 'MONTH', 'DAY', 'HOUR'])
        df = df[df['ZELEV'] == 84.85]
        result[date] = df
    return result


def plot_timeseries(df: Dict[str, pd.DataFrame], output_gif: str = 'visualization/outputs/map_of_aerosol_plume.gif'):
    # Define the custom Lambert Conformal Conic projection
    lcc_crs = CRS.from_proj4(
        "+proj=lcc +lat_1=30 +lat_2=40 +lat_0=37.37 +lon_0=-120.81 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    )
    wgs84_crs = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(lcc_crs, wgs84_crs, always_xy=True)

    # Calculate the lat/lon bounds for the grid corners
    x_min, x_max = -8800, 8800
    y_min, y_max = -8800, 8800
    frames = []
    # Create a custom colormap: 0 is fully transparent, then dark gray to light gray
    levels = np.arange(10, 140, 10)  # 10, 20, ..., 130
    n_bins = len(levels) - 1
    colors = [(0, 0, 0, 0)]  # RGBA for <10 (fully transparent)
    for i in range(1, n_bins + 1):
        gray = 0.2 + 0.75 * (i / n_bins)  # from dark gray (0.2) to light gray (0.95)
        colors.append((gray, gray, gray, 1))
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(levels, cmap.N)

    for date, frame_data in df.items():
        # Reproject X/Y to Web Mercator
        x_vals = np.sort(frame_data["X"].unique())
        y_vals = np.sort(frame_data["Y"].unique())
        X, Y = np.meshgrid(x_vals, y_vals)
        X_flat, Y_flat = X.flatten(), Y.flatten()
        X_ll, Y_ll = transformer.transform(X_flat, Y_flat)
        X_ll = X_ll.reshape(X.shape)
        Y_ll = Y_ll.reshape(Y.shape)
        Z = frame_data.sort_values(["Y", "X"])["CONC"].values.reshape(y_vals.shape[0], x_vals.shape[0])

        # Get extent in Web Mercator
        x_ll_min, x_ll_max = X_ll.min(), X_ll.max()
        y_ll_min, y_ll_max = Y_ll.min(), Y_ll.max()

        fig, ax = plt.subplots(figsize=(8, 8))
        # Set axis limits to the grid bounds in meters
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        # Set ticks every 2000 meters
        ax.set_xticks(np.arange(x_min, x_max + 1, 2000))
        ax.set_yticks(np.arange(y_min, y_max + 1, 2000))
        # Add satellite basemap (contextily) in meters
        lcc_crs = CRS.from_proj4(
            "+proj=lcc +lat_1=30 +lat_2=40 +lat_0=37.37 +lon_0=-120.81 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        )
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs=lcc_crs.to_string(), alpha=1.0)
        # Overlay the concentration data as a contour map (in model coordinates)
        contour = ax.contourf(
            X,
            Y,
            Z,
            levels=np.arange(10, 140, 10),
            cmap=ListedColormap([(0, 0, 0, 0)] + [(0.2 + 0.75 * (i / 12),) * 3 + (1,) for i in range(1, 13)]),
            norm=BoundaryNorm(np.arange(10, 140, 10), 13),
            extend='max',
            alpha=0.5
        )
        # Make the colorbar smaller
        cbar = fig.colorbar(contour, ax=ax, label='Concentration', ticks=np.arange(10, 140, 10), fraction=0.035, pad=0.04)
        # Get the unique height for this frame
        if 'ZELEV' in frame_data.columns and not frame_data.empty:
            height = frame_data['ZELEV'].iloc[0]
        else:
            height = 'unknown'
        # Fix '24:00:00' to '00:00:00' of next day
        date_fixed = date
        if date.endswith('24:00:00'):
            base = pd.to_datetime(date[:10]) + pd.Timedelta(days=1)
            date_fixed = base.strftime('%Y-%m-%d 00:00:00')
        # Format time for title (month-day hour:minute)
        time_fmt = pd.to_datetime(date_fixed).strftime('%m-%d %H:%M')
        ax.set_title(f'Map of CaCO3 Aerosol Plume at {height} m, {time_fmt}', fontsize=14, fontweight='bold')
        ax.set_xlabel('X (meters)', fontsize=12)
        ax.set_ylabel('Y (meters)', fontsize=12)
        ax.set_aspect('equal', adjustable='box')
        ax.tick_params(axis='both', labelsize=11)
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        frames.append(imageio.imread(buffer))
        plt.close(fig)
        plt.clf()

    # Save GIF with height in filename in outputs directory
    if 'height' in locals() and height != 'unknown':
        output_dir = 'visualization/outputs'
        os.makedirs(output_dir, exist_ok=True)
        output_gif = os.path.join(output_dir, f'map_of_aerosol_plume_{height}m.gif')
    with imageio.get_writer(output_gif, mode='I', fps=5) as writer:
        for image_data in frames:
            writer.append_data(image_data)

    print(f"GIF saved to {output_gif}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CaCO3 dispersion timeseries GIF.")
    parser.add_argument(
        "--input",
        type=str,
        default="../runs/CACO3_100M_1HR.PST",
        help="Path to the PST file (default: ../runs/CACO3_100M_1HR.PST)"
    )
    parser.add_argument(
        "--output_gif",
        type=str,
        default="central_area_timeseries.gif",
        help="Output GIF filename (default: central_area_timeseries.gif)"
    )
    args = parser.parse_args()

    frames_dfs = parse_to_df(args.input)

    # Print statistics for all concentration values to help choose a scale
    all_conc = np.concatenate([df['CONC'].values for df in frames_dfs.values()])
    print('Concentration statistics:')
    print('  min:', np.min(all_conc))
    print('  max:', np.max(all_conc))
    print('  mean:', np.mean(all_conc))
    print('  95th percentile:', np.percentile(all_conc, 95))
    print('  99th percentile:', np.percentile(all_conc, 99))
    print('  99.9th percentile:', np.percentile(all_conc, 99.9))

    plot_timeseries(frames_dfs, output_gif=args.output_gif)