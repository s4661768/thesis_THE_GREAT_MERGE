

import pyvisa
import numpy as np
import tqdm
import os
import time
import plotly.graph_objects as go
import concurrent.futures


class Oscilloscope:
    """Class to acquire data from an oscilloscope
    """
    def __init__(self, output_folder="OscilloscopeData", sources=[1, 2, 3], source_names=["Source1", "Source2", "Source3"]):
        self.folder_name = output_folder # folder to save the data
        self.sources = sources # sources to acquire data from
        self.source_names = source_names # names of the sources
        
        # connect to the oscilloscope
        self.rm = pyvisa.ResourceManager() # create a resource manager
        resources = self.rm.list_resources() # list available resources
        # resource_name = resources[0] # select the first resource
        resource_name = 'USB0::0x0957::0x179A::MY51350273::INSTR'
        self.scope = self.rm.open_resource(resource_name) # open the resource
        

    def create_folder(self):
        """Create the folder to save the data
        """
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def configure_oscilloscope(self):
        """Configure the oscilloscope to acquire data
        """
        print(self.scope.query("*IDN?"))
        self.scope.write(":WAV:FORM BYTE") # set the waveform format to byte because it is the fastest
        self.scope.write(":WAVeform:POINts:MODE MAXimum") # set the waveform points mode to maximum to get the maximum number of points

    def query_waveform_data(self, channel):
        """Query the waveform data from the oscilloscope

        Args:
            channel (int): channel to acquire data from

        Returns:
            numpy.array: array containing the waveform data
        """
        self.scope.write(f":WAV:SOUR CHAN{channel}")
        self.scope.write(":WAV:DATA?")
        waveform_data = self.scope.read_raw()
        waveform_values = np.frombuffer(waveform_data, dtype=np.uint8)
        return waveform_values

    def write_data_to_file(self, i, time_values, waveform_values):
        """Write the data to a file

        Args:
            i (int): index of the file
            time_values (numpy.array): array containing the time values
            waveform_values (list): list containing the waveform values
            source_names (list): list containing the names of the sources
            plot (bool): whether to plot the data
            
        """
        file_name = f"{self.folder_name}\\{i}.npy"
        data_to_save = np.column_stack((time_values, *waveform_values))
        data_to_save = data_to_save[1000:-1000]
        np.save(file_name, data_to_save)
    
    def acquire_data(self, nb_acquisitions=1, buffer_size=100):
        """Acquire data from the oscilloscope
        
        Args:
            nb_acquisitions (int): number of acquisitions
            buffer_size (int): size of the buffer
            save (bool): whether to save the data
            plot (bool): whether to plot the data
        """
        self.create_folder()
        self.configure_oscilloscope()
        data_buffer = []
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in tqdm.tqdm(range(nb_acquisitions), desc="Acquiring data"):
                    # wait random time between 0 and 0.1 seconds
                    time_to_wait = np.random.rand() / 100
                    # sleep so that the frequency of the acquisition constant which could introduce a bias
                    time.sleep(time_to_wait)
                    self.scope.write(':STOP')# Stop the oscilloscope
                    # Acquire data from each source
                    waveform_values = [self.query_waveform_data(source) for source in self.sources]
                    # Get the time increment
                    time_increment = float(self.scope.query(":WAV:XINC?"))
                    self.scope.write(':RUN') # Run the oscilloscope
    
                    time_values = np.arange(len(waveform_values[0])) * time_increment
                    data_buffer.append((i, time_values, waveform_values, self.source_names))
    
                    if len(data_buffer) >= buffer_size:
                        # Submit the write tasks to the thread pool
                        futures = [executor.submit(self.write_data_to_file, *data) for data in data_buffer]
                        # Create a progress bar for the file writing process
                        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Writing files"):
                            pass
                        data_buffer = []
    
                # Write remaining data in buffer to file
                futures = [executor.submit(self.write_data_to_file, *data) for data in data_buffer]
                for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Writing remaining files"):
                    pass
    
            self.scope.close()
        except KeyboardInterrupt:
            self.scope.close()
        except Exception as e:
            print(e)
            self.scope.close()
 
        

def plot_from_npy(file_name):
    """Plot data from a .npy file
    
    Args:
        file_name (str): file path
    """
    data = np.load(file_name)
    fig = go.Figure()
    #compute sampling frequency
    dt = np.gradient(data[:,0])
    mean_dt = np.mean(dt)
    fs = 1 / mean_dt
    # convert to kHz or MHz
    if fs < 1e3:
        fs = fs
        units = "Hz"
    elif fs < 1e6:
        fs = fs / 1e3
        units = "kHz"
    elif fs >= 1e6:
        fs = fs / 1e6
        units = "MHz"
    elif fs >= 1e9:
        fs = fs / 1e9
        units = "GHz"
    fig.update_layout(title=f"Sampling frequency: {fs:.2f} {units}")
    
    for i in range(1, data.shape[1]):
        fig.add_trace(go.Scatter
        (
            x=data[:,0],
            y=data[:,i],
            name="Source" + str(i)
        ))
    fig.show()
    

if __name__ == "__main__":
    output_folder="OscilloscopeData"
    # sources=[1, 2, 3] 
    # source_names=["Source1", "Source2", "Source3"]
    sources = [1]
    source_names = ["Source1"]    
    
    start_time = time.time()
    oscilloscope = Oscilloscope( 
                                output_folder=output_folder,
                                sources=sources,
                                source_names=source_names
                                )
    oscilloscope.acquire_data(
                                nb_acquisitions=100, # how many samples (screenshots) to take
                                buffer_size=100 # how many samples to buffer before writing to disk. watch out for memory usage
                                )
    dt = time.time() - start_time
    print("Total time: ", time.strftime("%H:%M:%S", time.gmtime(dt)))
    
    plot_from_npy(f"{output_folder}\\0.npy")
    
