#!/usr/bin/env python

from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import json 
import zipfile

# Utility functions

class SplitSilence ():

    def __init__ (self, filename, workid,windowduration = 0.1, stepduration=None, silencethreshold = 1e-6, ):
        self.FileName = filename
        self.windowDuration = windowduration
        self.stepDuration = stepduration 
        if self.stepDuration is None:
            self.stepDuration = self.windowDuration / 10.
        else:
            self.stepDuration = stepduration   
        self.WorkID = workid
        self.OutputFolder = "./audio/" + workid
        self.silenceThreshold = silencethreshold
        self.outputFilenamePrefix = os.path.splitext(os.path.basename(self.FileName))[0]


    def windows(self,signal, window_size, step_size):
        if type(window_size) is not int:
            raise AttributeError("Window size must be an integer.")
        if type(step_size) is not int:
            raise AttributeError("Step size must be an integer.")
        for i_start in range(0, len(signal), step_size):
            i_end = i_start + window_size
            if i_end >= len(signal):
                break
            yield signal[i_start:i_end]

    def energy(self,samples):
        return np.sum(np.power(samples, 2.)) / float(len(samples))

    def rising_edges(self,binary_signal):
        previous_value = 0
        index = 0
        for x in binary_signal:
            if x and not previous_value:
                yield index
            previous_value = x
            index += 1

    def Split(self):
        print ("Splitting {} where energy is below {}% for longer than {}s.".format(
            self.FileName,
            self.silenceThreshold * 100.,
            self.windowDuration
        ))

        # Read and split the file

        sample_rate, samples = input_data=wavfile.read(filename=self.FileName, mmap=True)
        max_amplitude = np.iinfo(samples.dtype).max
        max_energy = self.energy([max_amplitude])

        window_size = int(self.windowDuration * sample_rate)
        step_size = int(self.stepDuration * sample_rate)

        signal_windows = self.windows(
            signal=samples,
            window_size=window_size,
            step_size=step_size
        )

        window_energy = (self.energy(w) / max_energy for w in tqdm(
            signal_windows,
            total=int(len(samples) / float(step_size))
        ))

        window_silence = (e > self.silenceThreshold for e in window_energy)

        cut_times = (r * self.stepDuration for r in self.rising_edges(window_silence))

        # This is the step that takes long, since we force the generators to run.
        cut_samples = [int(t * sample_rate) for t in cut_times]
        cut_samples.append(-1)


        # We make sure that path exists for output
        try:
            os.mkdir(self.OutputFolder)
        except OSError:
            print ("Creation of the directory %s failed" % self.OutputFolder)
        else:
            print ("Successfully created the directory %s " % self.OutputFolder)

        cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]
        output_filename_prefix = os.path.splitext(os.path.basename(self.FileName))[0]
        for i, start, stop in tqdm(cut_ranges):
            output_file_path = "{}_{:03d}.wav".format(
                os.path.join(self.OutputFolder, output_filename_prefix),
                i
            )            
            wavfile.write(
                filename=output_file_path,
                rate=sample_rate,
                data=samples[start:stop]
            )
            
        ret = self.CompressWork()
        
        return ret
        
        
    def CompressWork (self):
        zippath = "./audio/"+ self.WorkID +".zip"
        zip_file = zipfile.ZipFile(zippath, 'w')
                    # ziph is zipfile handle
        for root, dirs, files in os.walk(self.OutputFolder):
            for file in files:
                zip_file.write(os.path.join(root,file))
                
        return zippath