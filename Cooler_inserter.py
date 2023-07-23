from pcpartpicker import API
import itertools

#open the pcpartpicker API
api = API()
cpu_cooler_data = api.retrieve("cpu-cooler")
values = cpu_cooler_data.values()
#put the pcpart object into a more readable format
flattened_values = itertools.chain(*values)

for element in flattened_values:
    print(element)