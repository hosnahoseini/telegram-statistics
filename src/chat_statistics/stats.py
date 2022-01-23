import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, sent_tokenize, word_tokenize
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
        stop_words = set(map(str.strip, stop_words))
        self.stop_words = set(map(self.normalizer.normalize,stop_words))


    @staticmethod
    def rebuild_msg(sub_messages):
        msg_text = ''
        for sub_msg in sub_messages:
            if isinstance(sub_msg, str):
                msg_text += sub_msg
            elif 'text' in sub_msg:
                msg_text += sub_msg['text']

        return msg_text
    
    
    def get_top_users(self, top_n: int=10) -> dict:
        """Get top users in replying questions

        Returns:
            [type]: dict of top users
        """
        # check messages for questions
        is_question = defaultdict(bool)
        for msg in self.chat_data['messages']:
            if not msg.get('text'):
                continue

            if not isinstance(msg['text'], str):
                msg['text'] = self.rebuild_msg(msg['text'])

            sentences = sent_tokenize(msg['text'])
            for sentence in sentences:
                if ('?' not in sentence) and ('؟' not in sentence):
                    continue
                is_question[msg['id']] = True
                break

        # get top users based on replying to questions from others
        logger.info("Getting top users...")
        users = []
        for msg in self.chat_data['messages']:
            if not msg.get('reply_to_message_id'):
                continue
            if is_question[msg['reply_to_message_id']] is False:
                continue
            users.append(msg['from'])

        top_users = dict(Counter(users).most_common(top_n))

        return top_users

    

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
        text_content = text_content[:1000]
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
    stats = ChatStatistics(json_file=DATA_DIR / 'result.json')
    stats.generate_wordcloud(DATA_DIR)
    print(stats.get_top_users(top_n=10))
    print("Done")
