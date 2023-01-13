# template_matching_algorithm

## Description
This is a Python library that performs template matching (implemented for [Seimitsu lab 2022](https://www.pemayfes.t.u-tokyo.ac.jp/2022/pc/)).

We won the first prize in [May festival](http://www.pe.t.u-tokyo.ac.jp/news/2022/20220516.html).

You can watch a [youtube video](https://www.youtube.com/watch?v=VJ_TkAnpTyI) of this robot performimg this library.

This library enables to detect
- an oblique image
- an image whose size is different from a template

<img src="https://user-images.githubusercontent.com/88654010/175755785-63e54176-6f85-454d-9a23-cc61202d1845.jpg" width="60%">

## Algorithm
1. Detect edges of a camera image
2. Find contours, curves joining all of the continuous points
3. Exclude contours whose area inside is below a certin level
4. Approximate shapes of the contours
5. Exclude all contours which don't have four vertexes
6. Transform the perspective of the image into that of a template (perspective transform)
7. Threshold the image
8. Evaluate correlation coefficient between the thresholded image and templates

## Requirement
- opencv-python
- opencv-contrib-python
- numpy

## Future work
1. Calculate essemtial matrix by use of 5-point algorithm (Nister)
2. Estimate self-position

## License
The source code is licensed MIT, see LICENSE.
