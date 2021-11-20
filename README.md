# Google Maps / Google My Business Scraper 🌎📊

This is script is a scraping script developed with Python and its automation library Selenium. **Consists of reading a list of keywords, searching them in the Google Maps search, and getting its data and cover image**.

The script goes one by one searching for the keyword, and storing the data in a list, to finally export it to an Excel file located in the folder specified by the user when running the script.

In the presentation video I show the script running without hiding the Chrome window, and it can be seen quite clear the process that the script follows.

However, although I have added [that version](build/maps_scraper_juaristech_windowed_demo.exe) in the build folder, the final version and the one it is in the source code, works without showing the Chrome window, because it works with 5 simultaneous threads to increase the speed and obtain the results faster.

For now the script works only for Spanish and English languages, however, I can add more languages in the future.

[![Google Maps Scraper](https://juaristech.com/wp-content/uploads/2021/11/google-maps-scraper-result.jpg)](https://juaristech.com/google-maps-scraper "JuarisTech")

## How to Run It

To execute this script you need to run it in the command prompt.

```bash
google_maps_scraper_juaristech.exe
```

Then, some questions will appear, which are necessary to run the script:

1. You will need to type "ES" for Spanish or "EN" for English.

    ```bash
    [1] Introduce the language, (ES o EN): 
    ```
2. You will need to specify the folder to save the output Excel and images. For example: *D:\Projects\Spain\Madrid\output\\*

    ```bash
    [2] Introduce the path to save the images:
    ```

3. To finish, you need to specify where is located the *.txt* file with the keywords to search. For example: *D:\Projects\Spain\Madrid\places.txt*

    ```bash
    [3] Introduce the path of the keywords txt file:
    ```

Then the script starts to work, and when it finished, the Excel file would appear in the output folder.

---

For any doubts about how to use the program, you can read the article of our web or see the demo video.

- Explanatory article: https://juaristech.com/google-maps-scraper
- Demo video: https://youtu.be/XX-u-eNkRFs

## Requirements

The used requirements are specified in the requierements.txt file. If you want to execute the *.py* script from python, you can install the dependencies with the next command:

```bash
pip install -r requirements.txt
```

## Contact

- Website: [JuarisTech](https://juaristech.com/)
- Email: admin@juaristech.com

