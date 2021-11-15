import regular_mesh_plotter as rmp
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

# creates a plot of the mesh tally
my_plot = rmp.plot_regular_mesh_dose_tally(
    tally=my_tally,  # the openmc tally object to plot, must be a 2d mesh tally
    filename="plot_regular_mesh_dose_tally.png",  # the filename of the picture file saved
    scale=None,  # LogNorm(),
    vmin=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot=0,
    required_units="picosievert / simulated_particle",
    source_strength=None,
    label="Effective dose [picosievert / simulated_particle]",
)

# displays the plot
my_plot.show()
