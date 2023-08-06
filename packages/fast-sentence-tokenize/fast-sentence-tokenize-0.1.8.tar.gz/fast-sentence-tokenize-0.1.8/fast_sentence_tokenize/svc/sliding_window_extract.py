#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Simple Sliding Window N-Gram Extractor """


from typing import List

from baseblock import BaseObject, Enforcer


class SlidingWindowExtract(BaseObject):
    """ Simple Sliding Window N-Gram Extractor """

    def __init__(self):
        """ Change Log

        Created:
            26-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _extract(self,
                 tokens: List[str],
                 gram_level: int) -> list:

        results = []
        total_tokens = len(tokens)

        for i in range(total_tokens):

            buffer = []

            x = 0
            while x < gram_level:

                pos = x + i
                if pos < total_tokens:
                    buffer.append(tokens[pos])

                x += 1

            if len(buffer) == gram_level:
                results.append(buffer)
                buffer = []

        return results

    def process(self,
                tokens: List[str],
                gram_level: int,
                skip_gram: bool = False) -> list:
        """ Extract Bigrams

        Args:
            tokens (List[str]): the incoming tokens
            gram_level (int): the gram level to extract at
            skip_gram (bool, False): skip every other gram. Defaults to False.

        Returns:
            list: a list of bigrams (or skipgrams)
        """

        if not skip_gram:
            return self._extract(tokens=tokens, gram_level=gram_level)

        tokens_even = []
        tokens_odd = []

        for i in range(len(tokens)):
            if i % 2 != 0:
                tokens_odd.append(tokens[i])
            else:
                tokens_even.append(tokens[i])

        grams_odd = self._extract(tokens=tokens_odd, gram_level=gram_level)
        grams_even = self._extract(tokens=tokens_even, gram_level=gram_level)

        return grams_odd + grams_even
