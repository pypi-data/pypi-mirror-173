#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Input Classification """


from functools import lru_cache

from baseblock import BaseObject, Enforcer, Stopwatch


class Classifier(BaseObject):
    """ Orchestrate Input Classification """

    prepositions = [
        'about', 'above', 'across', 'after', 'against', 'among', 'around', 'at', 'before', 'behind', 'below', 'beside', 'between',
        'by', 'down', 'during', 'for', 'from', 'in', 'inside', 'into', 'near', 'of', 'off', 'on', 'out', 'over', 'through', 'to',
        'toward', 'under', 'up', 'with'
    ]

    d_preps = {
        'about': {
            'what',
            'where',
            'how',
        },


    }

    def __init__(self) -> None:
        """ Change Log

        Created:
            23-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def classify(self,
                 input_text: str) -> None:
        """ Entry Point

        Args:
            input_text (str): An input string of any length or type

        Raises:
            ValueError: input must be a string

        Returns:

        """
        pass
