"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

import weakref


class SemanticAnalyzer:
    def __init__(self, parser):
        self.parser = weakref.ref(parser)

    def semantic_actions(self, action_symbol):
        pass
