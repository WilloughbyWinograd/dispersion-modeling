import matplotlib.pyplot as plt
import pandas as pd
import imageio.v2 as imageio
import numpy as np
import io
from collections import defaultdict
from typing import List, Tuple, Dict

HALF_WIDTH = 1000.0
CENTER_X, CENTER_Y = 0.0, 0.0


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
            date = parts[10].strip()
            year, month, day, hour = date[:2], date[2:4], date[4:6], date[6:8]
            date = f"20{year}-{month}-{day} {hour}:00:00"
            data[date].append((x, y, conc, year, month, day, hour))
        except ValueError:
            print(f"Skipping line due to parsing error: {line.strip()}")
            continue

    return {date: pd.DataFrame(data[date], columns=['X', 'Y', 'CONC', 'YEAR', 'MONTH', 'DAY', 'HOUR']) for date in data}

def plot_timeseries(df: Dict[str, pd.DataFrame], output_gif: str = 'central_area_timeseries.gif',):   
    
    frames = []
    for date, frame_data in df.items():
        fig, ax = plt.subplots(figsize=(8, 8))
        x = np.arange(-8700, 8701, 200)
        y = np.arange(-8700, 8701, 200)
        scatter = ax.pcolormesh(x, y, frame_data["CONC"].values.reshape(88, 88), vmax=130, vmin=0, cmap='inferno', shading='auto')
        cbar = fig.colorbar(scatter, ax=ax, label='Concentration')

        ax.set_title(f'CaCO3 Dispersion - Time Step {date}')
        ax.set_xlabel('X Coordinate (m)')
        ax.set_ylabel('Y Coordinate (m)')
        ax.set_aspect('equal', adjustable='box')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150)
        buffer.seek(0)
        
        frames.append(imageio.imread(buffer))

        plt.close(fig)
        plt.clf()
    
    with imageio.get_writer(output_gif, mode='I', fps=5) as writer: # Adjust fps as needed
        for image_data in frames:
            writer.append_data(image_data)

    print(f"GIF saved to {output_gif}")


if __name__ == "__main__":
    frames_dfs = parse_to_df('../CACO3_100M_1HR.PST')
    plot_timeseries(frames_dfs, output_gif='central_area_timeseries.gif')