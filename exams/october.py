import matplotlib.pyplot as plt
import numpy as np

import entro
import image
import ac

moon = image.RawImage("./data/moon-u8be-3x2613x3900.raw", 3900, 2613, 3)
#moons = [moon.get_copy_quantized(step) for step in [1,2,5,15,20,25]]

max_errors = [0,1,2,5,10,15,20,25]


#for step in range(1, 256):
#    print(f"step : {step} -> mse {quant.mse(moon.data, moon.get_copy_quantized(step).data)}")


#steps = [1, 3 ,4, 7, 10, 13, 15, 16]

#for step in steps:
#    print(f"Entropy for step {step} : {entro.get_entropy_from_array(moon.get_copy_quantized(step).data)}")
#    moon.add_ppm_header("./data/moon_ppm_header.txt")
#    moon.get_copy_quantized(step).write(f"./data/moon-{step}.raw")
    
#Entropy for step 1 : 7.685360305867178
#Entropy for step 3 : 6.130101877644978
#Entropy for step 4 : 5.713416281845032
#Entropy for step 7 : 4.919205894286251
#Entropy for step 10 : 4.410206365821107
#Entropy for step 13 : 4.03489960742236
#Entropy for step 15 : 3.8369963678459045
#Entropy for step 16 : 3.7288791324830455


#steps = [1, 3 ,5]

#hists = []
#for step in steps:
#    d = moon.get_copy_quantized(step).data
#    values, counts = np.unique(d.ravel(), return_counts=True)
#    hist = dict(zip(values.tolist(), counts.tolist()))
#    plt.plot(hist.keys(), hist.values())

#plt.show()


#steps = [1, 5 ,11]

#hists = []
#for step in steps:
#    d = moon.get_copy_quantized(step).data
#    values, counts = np.unique(d.ravel(), return_counts=True)
#    hist = dict(zip(values.tolist(), counts.tolist()))
#    plt.plot(hist.keys(), hist.values())

#plt.show()

steps = [5, 10]
for step in steps:
    d = moon.get_copy_quantized(step).data
    _, counts = np.unique(d, return_counts=True)
    probabilities = counts / counts.sum()
    print(entro.get_entropy_from_array(ac.arithmetic_encode(d, probabilities)))