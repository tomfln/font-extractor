# Font Extractor

Tired of manually extracting fonts after downloading a bunch?

Here's how to use font-extractor to do it for you:

1. download all the fonts you want
2. move the .zip files into a folder ("fonts" in this example)
3. run font-extractor: `py fontextract.py ./fonts`
4. copy the resulting "out" folder to where you wanna store the fonts
5. use a program like [FontBase](https://fontba.se) to import the folder and activate all fonts on your pc

## Features

### Font Formats
font-extractor will prefer OTF files by default, but you can choose to prefer TTF by passing `--prefer-ttf`

### Web Fonts
by default, all web fonts are copied to a sub-folder `web` in the font's directory. You can disable this by passing `--no-web`

### Font Licenses
font licenses (.txt) are copied to the resulting font folder so you can keep track of them.


## License
This Project is licensed under the MIT License
