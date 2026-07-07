class FeatureRegistry:
    def __init__(self):
        self.extractors = []
    def register(self, extractor):
        self.extractors.append(extractor)
    def get_all(self):
        return self.extractors