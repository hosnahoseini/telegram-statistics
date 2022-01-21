# Telegram Statistics
Export Statistics for a Telegram Group Chat

## How to Run
### Telegram Statistics and Word Cloud
The `src/stats.py` file contains the main function to export telegram chat word cloud.
To generate word cloud, in main repo directory, run the following command in your terminal to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/stats.py --json_file path_to_telegram_chat_export  --output_dir path_to_save_output_images
```
to generate a word cloud of json data in `DATA_DIR/wordcloud.png`.