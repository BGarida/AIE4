class SentenceTextSplitter:
    def init(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert chunk_size > chunk_overlap, "Chunk size must be greater than chunk overlap"
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_into_sentences(self, text: str) -> List[str]:
        # This regex splits on sentence-ending punctuation followed by whitespace or end of string
        return re.split(r'(?<=[.!?])\s+|\Z', text)
    def split_single_text(self, text: str) -> List[str]:
        sentences = self.split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            if current_chunk_size + sentence_size > self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    # Keep the last part for overlap
                    overlap_size = 0
                    while overlap_size < self.chunk_overlap and current_chunk:
                        overlap_size += len(current_chunk[-1])
                        current_chunk = current_chunk[-1:]
                    current_chunk_size = overlap_size
                else:
                    # If a single sentence is longer than chunk_size, we need to split it
                    chunks.append(sentence[:self.chunk_size])
                    current_chunk = [sentence[self.chunk_size:]]
                    current_chunk_size = len(current_chunk[0])

            current_chunk.append(sentence)
            current_chunk_size += sentence_size

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
    def split(self, text: Union[str, List[str]]) -> List[str]:
        if isinstance(text, str):
            return self.split_single_text(text)
        elif isinstance(text, list):
            return self.split_texts(text)
        else:
            raise TypeError("Input must be a string or a list of strings")

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split_single_text(text))
        return chunks