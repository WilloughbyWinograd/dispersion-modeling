import numpy as np
import matplotlib.pyplot as plt

pst_file = '../runs/CACO3_100M_1HR.PST'
output_png = 'caco3_central_100m_timeseries_24h.png'
center_x, center_y = 0.0, 0.0
half_width = 1000.0  # meters
max_hours = 24


# Helper to parse a data line

def parse_data_line(line):
    try:
        parts = line.strip().split()
        if len(parts) < 11:
            return None
        x = float(parts[0])
        y = float(parts[1])
        conc = float(parts[2])
        date = parts[10]  # e.g., 22080701
        return x, y, conc, date
    except Exception:
        return None


def main():
    hour_dates = []
    hour_data = {}
    with open(pst_file, 'r') as f:
        for line in f:
            # Skip header and blank lines
            if line.startswith('*') or not line.strip():
                continue
            parsed = parse_data_line(line)
            if not parsed:
                continue
            x, y, conc, date = parsed
            # Only consider central area
            if abs(x - center_x) > half_width or \
               abs(y - center_y) > half_width:
                continue
            # Track unique hours by date
            if date not in hour_dates:
                if len(hour_dates) >= max_hours:
                    break
                hour_dates.append(date)
            # Assign hour index
            hour_idx = hour_dates.index(date)
            if hour_idx not in hour_data:
                hour_data[hour_idx] = []
            hour_data[hour_idx].append(conc)
    # Compute average per hour
    avg_conc = [np.mean(hour_data[i]) if i in hour_data else 0
                for i in range(max_hours)]
    # Plot
    t = np.arange(max_hours)
    plt.figure(figsize=(10, 5))
    plt.plot(t, avg_conc, marker='o',
             label='Central Area (±1,000m) Avg, 100m Elevation')
    plt.xlabel('Hour Index')
    plt.ylabel('Concentration (µg/m³ or model units)')
    plt.title(
        'Average Hourly CaCO₃ Concentration in Central 2,000m × 2,000m Area\n'
        'at 100m Elevation (First 24 Hours)'
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"Saved time series plot as {output_png}")


if __name__ == "__main__":
    main() 