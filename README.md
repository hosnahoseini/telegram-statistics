# Telegram Statistics
Export Statistics for a Telegram Group Chat

## How to Run
### Telegram Statistics and Word Cloud
The `src/stats.py` file contains the main function to export telegram chat word cloud and the number of questions people have responded to.

To generate word cloud and get stats, in main repo directory, run the following command in your terminal to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/stats.py --chat_json path_to_telegram_chat_export  --output_dir path_to_save_output_images --mask mask_image_path
```
to generate a word cloud of json data in `DATA_DIR/word_cloud.png`. Top users bar chart is also generated in output_dir as `top_users.png` where the height of the bar is the number of questions answered by the user. You can also mask your word cloud with a mask image by passing the mask image path as `--mask` argument. See [here](https://github.com/amueller/word_cloud) for some examples.
