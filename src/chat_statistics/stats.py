import json
from collections import Counter
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    """Generate chat statistics from a telegram chat json file
    """
    def __init__(self, json_file: Union[str, Path]):
        """
        Args:
            json_file (Union[str, Path]): path to telegram json file
        """
        # load chat data
        logger.info(f"loading chat data from {json_file}")
        with open(json_file) as f:
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()

        # load stop words
        logger.info("loading stop words")
        stop_words = open(DATA_DIR / 'stop_words.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize,stop_words))

    def generate_wordcloud(self, output_dir: Union[str, Path], width: int=1000, height: int=800):
        """Generate word cloud of chats

        Args:
            output_dir (Union[str, Path]): output file path
            width (int): width
            hight (int): higth
        """
        logger.info("loading text")
        text_content = ''

        for msg in self.chat_data['messages']:
            
            try:
                if type(msg['text']) is str:
                    token = word_tokenize(msg['text'])
                    token = list(filter(lambda item:item not in self.stop_words,token))
                    text_content += f" {' '.join(token)}"
                elif type(msg['text']) is list:
                    for sub_msg in msg['text']:
                        if type(sub_msg) is str:
                            text_content += f" {sub_msg}"
                        else:
                            text_content += f" {sub_msg['text']}"
            except KeyError:
                pass

        # normalize final text
        text_content = text_content[:50000]
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)

        logger.info(f"generating word cloud")
        # Generate a word cloud image
        wordcloud = WordCloud(
            font_path=str(DATA_DIR / 'B Homa_0.ttf'),
             background_color='white',
             width=1000,
             height=800
             ).generate(text_content)

        logger.info(f"saving word cloud to {output_dir}")
        wordcloud.to_file(Path(output_dir) / 'wordcloud.png')


if __name__ == "__main__":
    stats = ChatStatistics(json_file=DATA_DIR / 'ee_aut.json')
    stats.generate_wordcloud(DATA_DIR)
    print("Done")
