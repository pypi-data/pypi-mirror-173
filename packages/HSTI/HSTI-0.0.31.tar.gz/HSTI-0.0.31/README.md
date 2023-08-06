This package contains functions used in data processing of hyperspectral images
captured using a scanning Fabry-Pérot interferometer (FPI). This includes transmission
simulations of the FPI itself.


-------------------
## Image handling

### HSTI.import_data_cube(path)

  _This function imports the hyperspectral thermal datacube from the raw output of the camera. The path that the function uses as input must be the one containing the 'images' directory._

### HSTI.import_image_acquisition_settings(path):

  _This function imports the image acquisition settings during the capturing event. The path that the function uses as input must be the one containing the 'images' directory._

### HSTI.export_data_cube(cube, folder_name)

  _This function takes an HSTI numpy array and exports it as individual .ppm images to a folder given by folder_name._

### HSTI.median_filter_cube(cube, kernel_size)

  _This function runs a median filter across the image plane. The size of the kernel must be defined._

-------------------
## Preprocessing

### HSTI.mean_center(cube, axis = 's')

  _This function subtracts the mean from the data, either the mean of each spectrum (axis = 's') or the mean of each band (axis = 'b')._

### HSTI.autoscale(cube, axis = 's')

  _This function subtracts the mean and scales with STD. Setting axis = 's' is the same as doing SNV (standard normal variate)._

### HSTI.norm_normalization(cube, order, axis = 's')

  _This function uses the norm of a given order for normalization. If axis = 's', then each spectrum is divided by its norm. If axis = 'b', then every band is divided by the norm of the entire band._

### HSTI.normalize(cube, axis = 's')

  _This function calculates the normalised cube. By setting axis = 's' each spectrum (pixel) will span from 0 to 1 and axis = 'b' normalizes each band individually._

### HSTI.remove_stuck_px(cube)

  _This function removes the dead pixels in the bolometer by replacing them with the average of their non-zero neighbors._

### HSTI.remove_outlying_px(cube, cut_off)

  _This function removes outlying pixel measurements of values higher than the cut off value._

### HSTI.msc(cube, ref_spec = None)

  __

### HSTI.normalize_cube(cube)

  __

### HSTI.debend(cube, central_mirror_sep)

  _This function takes a single HSTI as input and returns a new spectral bending corrected cube. This does however require a vector containing the mirror separation corresponding to each band in the cube._

### HSTI.baseline(cube)

  _This function subtracts the mean pixel value from every band in the datacube._

### HSTI.normalize_pixel(cube)

  _This function normalises the entire data cube by dividing all bands by the sum of the bands in each individual pixel._

### HSTI.subtract_band(cube, band)

  _This function subtracts the first band from the remaining bands in the datacube, effectively setting the first band to zero._

### HSTI.flatten()

  _This function flattens the datacube into a two-dimensional array._

### HSTI.inflate()

  _This function inflates the datacube into a three-dimensional array._

### HSTI.median_filter_cube(cube, kernel_size)

  __

### HSTI.targeted_median_filter(array, px_idx, kernel_size)

  __

### HSTI.conf95lim(x)

  __

### HSTI.hottelings(X)

  __

### HSTI.array2rgb(three_layer_cube)

  __

### HSTI.apply_NUC_cube(cube, sensor_temp, GSK, NUC_directory = 'default')

  _This function calculates and applies a NUC to the entire datacube. The NUC is dependent on the sensor temperature and the GSK settings of the camera. The NUC is calculated from camera specific calibration files from the accompanying NUC directory._

### HSTI.apply_NUC_image(image, sensor_temp, GSK, NUC_directory = 'default')

  _This function calculates and applies a NUC to a single image. The NUC is dependent on the sensor temperature and the GSK settings of the camera. The NUC is calculated from camera specific calibration files from the accompanying NUC directory._

-------------------

## Common analysis


### HSTI.fps(points, n_seeds)

  _Function which distributes n_seeds (a numper of points) equally within a lists of points to obtain furthest point sampling._

  _The function takes in a list of points. Every entry in the list contains both the x and y coordinate of a given point. It returns the coordinates of the selected sample points._


### HSTI.voronoi(array_2D, n_seeds)

  _This function accepts a 2-dimensional array (array_2D) and splits it up into N (n_seeds) subdomains. The partitioning is done based on furthest point sampling._

### HSTI.mse(lst1, lst2)

  _This function returns the mean square error (MSE) between two lists of same length._

### HSTI.r_sq(y_fit, y_meas)

  _This function returns the coefficeint of determination (R²) between fit values in list, y_fit, and measured data in list, y_meas._

### HSTI.PCA()

  __

#### .calculate_pca(self,matrix)

  _This function calculates the PCA of a two-dimensional input_

#### .apply_pca(self,matrix)

  _This function returns the PCA loadings_

### HSTI.least_squares_methods.GLS()

####

### HSTI.least_squares_methods.ALS()

####


-------------------
## FPI Simulation

### HSTI.fpi_sim(mirror_sep, lam, temp)

  _This function uses the Transfer Matrix Method (TMM) to simulate the transmittance, reflectance of the FPI at given mirror separation (mirror_sep) and wavelength (lam). temp is the substrate temperature since the refractive index of Germanium is temperature dependent. This function DOES NOT take broadening due to substrate bending into account. The functions returns the transmittance, the reflectance, as well as the numeric loss of the simulation._

### HSTI.fpi_sim_matrix(mirror_sep, lam, temperature)

  _The same as HSTI.fpi_sim(), but instead of single values, this function accepts vectors for mirror separation and wavelength. It then returns a 2D array of transmittance values of the FPIwhere each row represents a specific mirror separation while the each column indicates individual wavelengths. This function does take broadaning into account, but only returns the transmittance matrix. Since no loss is included in the model, the reflectance can be found by subtracting the transmittance matrix from a similar-sized matrix of ones._

### HSTI.fpi_sim_matrix_angular(mirror_sep, lam, temperature, angle_in_deg)

  _This function is similar to HSTI.fpi_sim_matrix(), but also takes the angle between the incoming ray and the FPI as an argument._


-------------------

# Contact

  _For bug reports or other questions please contact mani@newtec.dk or alj@newtec.dk._
