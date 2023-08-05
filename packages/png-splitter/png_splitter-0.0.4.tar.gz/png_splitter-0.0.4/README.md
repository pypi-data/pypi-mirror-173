# png_splitter

## Split a png into smaller images.
A simple package that is able to split a full image like a sprite sheet.

⚠️ `This package only works if the background of the png is invisible, otherwise, it will have unexpected results` ⚠️

For example, the following image:
<p align="center">
<img width="75%" src="https://github.com/andrefpoliveira/png_splitter/blob/master/image.png"/>
</p>

Creates 10 smaller images:
<p float="left" align="center">
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/0.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/1.png" width="80" /> 
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/2.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/3.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/4.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/5.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/6.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/7.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/8.png" width="80" />
  <img src="https://github.com/andrefpoliveira/png_splitter/blob/master/splitted/9.png" width="80" />
</p>

### How to Install
```
pip install png_splitter
```

All you have to do is:
```py
png_splitter.split_image("image.png", "images_folder")
```
