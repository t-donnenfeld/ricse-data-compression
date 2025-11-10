import image_processing.image as im
import entropy_coders.ac as ac
import analysis.entro as entro
import image_processing.quant


# Compare the rate-distortion performance of (a) a uniform quantizer + a memoryless entropy coder of your choice, and (b) a real image compressor, ideally a standard.
# You may use the Geo_Sample image of the materials, or create your own corpus.
# Analyze these results looking at the original data entropy.
# Consider a wireless transmission system for earphones, e.g., bluetooth or zigbee, and the sample piano-s16le-2channels.raw file of the materials.
# Assuming this sample is representative, what is the highest quality at which we can transmit audio in real time (considering the transmission speed of your system)?

def main():
    geo_original = im.RawImage("./data/Geo_Sample-u16be-242x1024x256.raw", 1024, 256, 242, sample_size=2)
    print(f"Original entropy is : {entro.get_entropy_from_array(geo_original.data)}")
    #Original entropy is : 9.399728459154403
    quant_step = 5
    quant_steps = [1,5,20,100,1000]

    geo_quant = geo_original.__copy__()
    geo_quant.data = image_processing.quant.quantize_midtread_mid(geo_quant.data, quant_step)
    ac.array_encode(geo_quant.data)

if __name__ == '__main__':
    main()
