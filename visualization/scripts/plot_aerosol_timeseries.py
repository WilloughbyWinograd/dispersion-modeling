import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
from pyproj import CRS, Transformer
import matplotlib.dates as mdates

def parse_pst(filename):
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
            data[date].append((x, y, conc))
        except Exception:
            continue
    return data

def get_center_avg_and_total_mass(data, grid_spacing=100.0, center_radius=150.0):
    times = []
    center_avgs = []
    total_masses = []
    cell_area = grid_spacing ** 2  # m^2
    for date, vals in data.items():
        arr = np.array(vals)
        x, y, conc = arr[:,0], arr[:,1], arr[:,2]
        mask = (np.abs(x) <= center_radius) & (np.abs(y) <= center_radius)
        center_avg = conc[mask].mean() if np.any(mask) else np.nan
        total_mass_ug = np.sum(conc * cell_area)
        total_mass_kg = total_mass_ug * 1e-9
        times.append(date)
        center_avgs.append(center_avg)
        total_masses.append(total_mass_kg)
    return times, center_avgs, total_masses

def parse_sfc_winds(filename):
    wind_speeds = []
    wind_times = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(' ') or line.startswith('*') or not line.strip():
                continue
            parts = line.split()
            if len(parts) < 16:
                continue
            # Date/time fields: year, month, day, hour
            year, month, day, hour = parts[0], parts[1], parts[2], parts[4]
            date = f"20{year.zfill(2)}-{month.zfill(2)}-{day.zfill(2)} {hour.zfill(2)}:00:00"
            try:
                wind_speed = float(parts[15])
                # Filter: set to NaN if <=0 or >100 m/s
                if wind_speed <= 0 or wind_speed > 100:
                    wind_speed = np.nan
            except Exception:
                wind_speed = np.nan
            wind_times.append(date)
            wind_speeds.append(wind_speed)
    return wind_times, wind_speeds

def plot_timeseries(times, center_avgs, total_masses, wind_times, wind_speeds, output_png='aerosol_timeseries.png'):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    # Fix '24:00:00' to '00:00:00' of next day
    times_fixed = []
    for t in times:
        if t.endswith('24:00:00'):
            base = pd.to_datetime(t[:10]) + pd.Timedelta(days=1)
            times_fixed.append(base.strftime('%Y-%m-%d 00:00:00'))
        else:
            times_fixed.append(t)
    times_dt = pd.to_datetime(times_fixed)
    wind_times_fixed = []
    for t in wind_times:
        if t.endswith('24:00:00'):
            base = pd.to_datetime(t[:10]) + pd.Timedelta(days=1)
            wind_times_fixed.append(base.strftime('%Y-%m-%d 00:00:00'))
        else:
            wind_times_fixed.append(t)
    wind_times_dt = pd.to_datetime(wind_times_fixed)
    # Align wind speed to PST times
    wind_speed_aligned = []
    wind_dict = dict(zip(wind_times_dt, wind_speeds))
    for t in times_dt:
        wind_speed_aligned.append(wind_dict.get(t, np.nan))
    # Panel 1: Center region avg
    axs[0].plot(times_dt, center_avgs, marker='o')
    axs[0].set_title('Aerosol Concentration at Center Region (μg/m³)')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Avg Aerosol (μg/m³)')
    # Panel 2: Total mass
    axs[1].plot(times_dt, total_masses, marker='o')
    axs[1].set_title('Total Aerosol Mass in Domain (kg)')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Aerosol Mass (kg)')
    # Panel 3: Wind speed (aligned)
    axs[2].plot(times_dt, wind_speed_aligned, marker='o')
    axs[2].set_title('Wind Speed at Center (m/s)')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Wind Speed (m/s)')
    axs[2].set_ylim(0, 20)
    # Set x-ticks every 6 hours and format as 'month-day hour'
    tick_locator = mdates.HourLocator(interval=6)
    tick_formatter = mdates.DateFormatter('%m-%d %H:%M')
    for ax in axs:
        ax.xaxis.set_major_locator(tick_locator)
        ax.xaxis.set_major_formatter(tick_formatter)
        ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig(output_png, dpi=150)
    print(f"Saved to {output_png}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Plot aerosol concentration, total mass, and wind speed timeseries from PST and SFC files.")
    parser.add_argument('--input', type=str, default='runs/CACO3_100M_1HR.PST', help='PST file path')
    parser.add_argument('--sfc', type=str, default='AERMOD/modesto-city-23258/2022.SFC', help='SFC file path')
    parser.add_argument('--output_png', type=str, default='aerosol_timeseries.png', help='Output PNG file')
    parser.add_argument('--grid_spacing', type=float, default=100.0, help='Grid spacing in meters')
    parser.add_argument('--center_radius', type=float, default=150.0, help='Radius for center region (m)')
    args = parser.parse_args()

    data = parse_pst(args.input)
    times, center_avgs, total_masses = get_center_avg_and_total_mass(data, grid_spacing=args.grid_spacing, center_radius=args.center_radius)
    wind_times, wind_speeds = parse_sfc_winds(args.sfc)
    plot_timeseries(times, center_avgs, total_masses, wind_times, wind_speeds, output_png=args.output_png) 