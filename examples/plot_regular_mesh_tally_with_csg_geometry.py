import openmc

import openmc_geometry_plot  # extends openmc.Geometry class with plotting functions
import regular_mesh_plotter  # extends openmc.Mesh class with plotting functions
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

# MATERIALS

mat_1 = openmc.Material()
mat_1.add_element("Li", 1)
mat_1.set_density("g/cm3", 0.45)

my_materials = openmc.Materials([mat_1])

# GEOMETRY

# surfaces
inner_surface = openmc.Sphere(r=200)
outer_surface = openmc.Sphere(r=400, boundary_type="vacuum")

# cells
inner_region = -inner_surface
inner_cell = openmc.Cell(region=inner_region)

outer_region = -outer_surface & +inner_surface
outer_cell = openmc.Cell(region=outer_region)
outer_cell.fill = mat_1

my_geometry = openmc.Geometry([inner_cell, outer_cell])


# SIMULATION SETTINGS

# Instantiate a Settings object
my_settings = openmc.Settings()
my_settings.batches = 10
my_settings.inactive = 0
my_settings.particles = 5000
my_settings.run_mode = "fixed source"

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((100, 0, 0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = source


my_tallies = openmc.Tallies()

mesh = openmc.RegularMesh().from_domain(
    my_geometry,  # the corners of the mesh are being set automatically to surround the geometry
    dimension=[20, 20, 20],
)
mesh_filter = openmc.MeshFilter(mesh)

mesh_tally_1 = openmc.Tally(name="mesh_tally")
mesh_tally_1.filters = [mesh_filter]
mesh_tally_1.scores = ["absorption"]
my_tallies.append(mesh_tally_1)

model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)
sp_filename = model.run()

statepoint = openmc.StatePoint(sp_filename)

# extracts the mesh tally by name
my_mesh_tally = statepoint.get_tally(name="mesh_tally")

# gets a 2d slice of data to later plot
data_slice = mesh.slice_of_data(dataset=my_mesh_tally.mean, view_direction="x")

# this section adds a contour line according the the material ids
material_ids = my_geometry.get_slice_of_material_ids(view_direction="x")


plot_1 = plt.imshow(
    data_slice,
    extent=mesh.get_mpl_plot_extent(view_direction="x"),
    interpolation=None,
    norm=LogNorm(
        vmin=1e-12,  # trims out the lower section of the colors
        vmax=max(data_slice.flatten()),
    ),
)
cbar = plt.colorbar(plot_1)
cbar.set_label(f"absorption per source particle")

# gets unique levels for outlines contour plot and for the color scale
levels = np.unique([item for sublist in material_ids for item in sublist])

plt.contour(
    material_ids,
    origin="upper",
    colors="k",
    linestyles="solid",
    levels=levels,
    linewidths=2.0,
    extent=my_geometry.get_mpl_plot_extent(view_direction="x"),
)
xlabel, ylabel = my_geometry.get_axis_labels(view_direction="x")
plt.xlabel(xlabel)
plt.ylabel(ylabel)


plt.show()
# plt.savefig("mesh_with_geometry.png")
