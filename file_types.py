import re

#Represents a neutronic input file
class neutronic_input():

    #If the file already exists
    def __init__(self, name): 
        self.name = name
        self.__find_U_and_Th()

    #Create a new input file with new values for U and Th
    def new_input(self, thorium, uranium):
        with open(self.name, 'r') as f:
            copy = f.readlines()
            for index, line in enumerate(copy):
                if index == 26:
                    copy[index] = "Th-232.09c      {:.3f}\n".format(thorium)
                elif index == 27:
                    copy[index] = "U-233.09c        {:.3f}\n".format(uranium)

        with open(self.name, 'w') as f:
            for line in copy:
                f.write(line)

        self.U = uranium
        self.Th = thorium

    #Get the values from U and Th from an existing input file
    def __find_U_and_Th(self):                            
        path_file = f"{self.name}"
        with open(path_file, 'r') as file:
            lines = file.readlines()
            self.Th = float(lines[26].split()[1])
            self.U  = float(lines[27].split()[1])

    #Create two new input files based on an existing one. In one of them 
    # the temperature changes, and, in the other one, the density changes.
    # density: -4.1249 -> -3.95    temperature: 1200 -> 900 
    def change_density_and_temperature(self):
        path_original = f"{self.name}"
        path_temp = f"{self.name}_temperature"
        path_density = f"{self.name}_density"
        with open(path_original, 'r') as original, open(path_temp, 'w') as temp, open(path_density, 'w') as density:
            for index, line in enumerate(original):
                if index == 22:
                    temp.write("mat fuel  -4.1249 tmp 1200.0 rgb 250 250 50\n")
                    density.write("mat fuel  -3.95 tmp 900.0 rgb 250 250 50\n")
                else:
                    temp.write(line)
                    density.write(line)
    

#Represents the neutronic output file
class neutronic_output():
    def __init__(self, name):
        self.name = name
        self.__find_variables()

    #Get some variables from the output file
    def __find_variables(self):
        path_file = f"{self.name}"
        with open(path_file, 'r') as file:

            for line in file:
                if re.search("ANA_KEFF", line):
                    print(line)
                    self.keff = float(line.split()[6])
                    self.keff_sd = float(line.split()[7])

            #self.KEFF            = float(lines[256].split()[6])
            #self.KEFF_SD         = float(lines[256].split()[7])
            #self.BETA_ZERO       = float(lines[282].split()[6])
            #self.BETS_ZERO_SD    = float(lines[282].split()[7])
            #self.GEN_TIME        = float(lines[300].split()[6])
            #self.GEN_TIME_SD     = float(lines[300].split()[7])
            #self.BETA_EFF        = float(lines[304].split()[6])
            #self.BETA_EFF_SD     = float(lines[304].split()[7])
