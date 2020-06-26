# PictureCreator
 
Currently any images that are not 80 * 80 will be resized to 240 * 240

Times of different versions:

        Time before adding IMAGES_USED dict: 115.4655818939209 (on 19-13)
        Time after adding IMAGES_USED dict: 112.70291018486023 (on 19-13)

        Without threading on picture 0-14: 36.986820220947266
        With threading on picture 0-14: 37.82171297073364 (threading library)
        With threading on picture 0-14: 5.732244968414307 (concurrent.futures library)
        
        Concurrent.futures:
            10-17:
                Before (linear): 41.8779718875885
                After (async): 13.810746908187866
            19-13:
                Before: 112.70291018486023
                After: 11.00510859489441
                
Example:

![arceus_orig](/images/original_image.png)

Goes to

![arceus](/images/final_image.png)
