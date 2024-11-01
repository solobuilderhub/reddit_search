import ahocorasick

class KeywordSearch:
    def __init__(self, keywords):
        self._keywords = keywords
        self._A = ahocorasick.Automaton()
        for idx, keyword in enumerate(keywords):
            self._A.add_word(keyword, (idx, keyword))
        self._A.make_automaton()

    def search(self, text):
        found_keywords = {keyword: False for keyword in self._keywords}
        for end_index, (idx, keyword) in self._A.iter(text):
            found_keywords[keyword] = True
        return found_keywords

# Example usage
keywords = ["keyword1", "keyword2", "keyword3"]
text = "This is a sample text with keyword1 and keyword3."

searcher = KeywordSearch(keywords)
result = searcher.search(text)

print(result)  # Output: {'keyword1': True, 'keyword2': False, 'keyword3': True}