# Generates a 4-layer 3D receptor grid for AERMOD input
# Each layer: 89x89 grid, 200m spacing
# X/Y from -8800 to +8800 m
# Center heights: 25.77, 84.85, 160.78, 257.64 m

layer_heights = [25.77, 84.85, 160.78, 257.64]
n_points = 89
spacing = 200.0
x0 = -8800.0
y0 = -8800.0

with open('receptors_4layer_grid.inp', 'w') as f:
    f.write('RE STARTING\n')
    f.write('   ELEVUNIT  METERS\n\n')
    f.write('** 4-layer 3D grid: 89x89 receptors per layer, 200m spacing, at heights **\n')
    f.write('** Layer 0: 25.77m, 1: 84.85m, 2: 160.78m, 3: 257.64m **\n\n')
    for z in layer_heights:
        for i in range(n_points):
            x = x0 + i * spacing
            for j in range(n_points):
                y = y0 + j * spacing
                line = (
                    '   DISCCART {x:8.2f} {y:8.2f} {z:7.2f} 0.0 0.0\n'
                    .format(x=x, y=y, z=z)
                )
                f.write(line)
    f.write('\nRE FINISHED\n') 