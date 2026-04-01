import spacy
import pytextrank
from collections import Counter
from transformers import pipeline

# Load SpaCy model and add TextRank pipeline component
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("textrank")


class Summarizer:
    def __init__(self, nlp):
        self.summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
        self.nlp = nlp

    # ─── Shared Utilities ───────────────────────────────────────────────

    def _clean_text(self, text):
        """Clean text and split into sentences using SpaCy."""
        cleaned_text = text.replace('\n', ' ').replace('\r', ' ')
        # Collapse multiple spaces
        cleaned_text = ' '.join(cleaned_text.split())
        doc = self.nlp(cleaned_text)
        sents = [sent.text for sent in doc.sents]
        return doc, sents

    def _get_word_weights(self, doc):
        """Get word importance weights via lemma frequency (used for analytics display)."""
        words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        if not words:
            return {}
        word_counts = Counter(words)
        max_count = max(word_counts.values())
        word_weights = {key: value / max_count for key, value in word_counts.items()}
        return word_weights

    def _get_sentence_weights_from_textrank(self, doc, sents):
        """
        Get sentence importance weights using TextRank scores.
        Maps pytextrank phrase scores back to sentences for the Source Analysis Map.
        """
        sentence_weights = {}

        # Get phrase scores from TextRank
        phrase_scores = {}
        for phrase in doc._.phrases:
            for chunk in phrase.chunks:
                phrase_scores[chunk.text.lower()] = phrase.rank

        # Score each sentence by how many high-ranked phrases it contains
        for idx, sent in enumerate(doc.sents):
            score = 0.0
            token_count = 0
            for token in sent:
                if not token.is_stop and not token.is_punct:
                    token_count += 1
                    lemma = token.lemma_.lower()
                    # Check if this token appears in any ranked phrase
                    for phrase_text, rank in phrase_scores.items():
                        if lemma in phrase_text:
                            score += rank
                            break
            # Normalize by sentence length to avoid bias toward long sentences
            if token_count > 0:
                sentence_weights[idx] = score / token_count
            else:
                sentence_weights[idx] = 0.0

        return sentence_weights

    # ─── Enhancement 1: TextRank Extractive ─────────────────────────────

    def summarize_text(self, text, n):
        """
        Extractive summarization using TextRank (graph-based ranking).
        
        TextRank builds a graph of sentences connected by similarity,
        then uses PageRank-style iteration to find the most important ones.
        Much better than naive word-frequency scoring.
        """
        doc, sents = self._clean_text(text)
        word_weights = self._get_word_weights(doc)
        sentence_weights = self._get_sentence_weights_from_textrank(doc, sents)

        # Use pytextrank's built-in summary extraction for the actual summary
        # Collect selected sentences with their original position index
        selected = []
        for sent in doc._.textrank.summary(limit_sentences=n):
            # Find the original index of this sentence in the document
            for idx, original_sent in enumerate(sents):
                if sent.text == original_sent and idx not in [s[0] for s in selected]:
                    selected.append((idx, sent.text))
                    break

        # Sort by original document position so the summary reads naturally
        selected.sort(key=lambda x: x[0])
        summary = " ".join([text for _, text in selected])

        return word_weights, sentence_weights, sents, summary

    # ─── Enhancement 2: Chunked Abstractive ─────────────────────────────

    def _split_into_chunks(self, text, max_words=900, overlap_words=100):
        """
        Split text into overlapping chunks to handle BART's 1024-token limit.
        
        Args:
            text: The full document text
            max_words: Maximum words per chunk (~900 words ≈ ~1024 tokens)
            overlap_words: Overlap between chunks to maintain context continuity
        
        Returns:
            List of text chunks
        """
        words = text.split()

        if len(words) <= max_words:
            return [text]

        chunks = []
        start = 0
        while start < len(words):
            end = start + max_words
            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            # Move forward by (max_words - overlap) for the next chunk
            start += max_words - overlap_words

            # If the remaining text is very short, merge it with the last chunk
            if start < len(words) and (len(words) - start) < overlap_words:
                last_chunk = " ".join(words[start:])
                chunks[-1] = chunks[-1] + " " + last_chunk
                break

        return chunks

    def abstractive_summarize(self, text, num_sentences, prompt=''):
        """
        Abstractive summarization with chunking support.
        
        For documents longer than ~900 words:
        1. Split into overlapping chunks
        2. Summarize each chunk independently
        3. Merge chunk summaries with a second pass
        
        This fixes the silent truncation bug where BART drops everything
        after its 1024-token context window.
        """
        # If a prompt is provided, prepend it to the text
        if prompt:
            text = f"{prompt} {text}"

        # Get analytics from full text (for Source Analysis Map)
        doc, sents = self._clean_text(text)
        word_weights = self._get_word_weights(doc)
        sentence_weights = self._get_sentence_weights_from_textrank(doc, sents)

        # Split into chunks
        chunks = self._split_into_chunks(text)

        # Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            # Calculate per-chunk length limits
            if len(chunks) == 1:
                max_len = num_sentences * 25
                min_len = max(30, num_sentences * 10)
            else:
                # For multi-chunk: each chunk gets a proportional share
                per_chunk_sentences = max(2, num_sentences // len(chunks) + 1)
                max_len = per_chunk_sentences * 25
                min_len = max(30, per_chunk_sentences * 10)

            result = self.summarization_pipeline(
                chunk, max_length=max_len, min_length=min_len, do_sample=False
            )
            chunk_summaries.append(result[0]['summary_text'])

        # If we had multiple chunks, do a merge pass
        if len(chunks) > 1:
            combined = " ".join(chunk_summaries)
            final_max_len = num_sentences * 25
            final_min_len = max(30, num_sentences * 10)

            # Only do merge pass if combined text is long enough to warrant it
            if len(combined.split()) > final_max_len:
                final_result = self.summarization_pipeline(
                    combined,
                    max_length=final_max_len,
                    min_length=final_min_len,
                    do_sample=False
                )
                summary = final_result[0]['summary_text']
            else:
                summary = combined
        else:
            summary = chunk_summaries[0]

        return word_weights, sentence_weights, sents, summary

    # ─── Enhancement 3: Hybrid Pipeline ──────────────────────────────────

    def hybrid_summarize(self, text, num_sentences):
        """
        Hybrid summarization: Extractive → Abstractive pipeline.
        
        1. TextRank extractive selects top 2×N sentences (over-select for coverage)
        2. Those sentences are fed to the abstractive model for polishing
        
        This produces the highest quality summaries:
        - Extractive ensures the most important FACTS are included
        - Abstractive ensures the output reads naturally (like a human wrote it)
        """
        # Get analytics from full text (for Source Analysis Map)
        doc, sents = self._clean_text(text)
        word_weights = self._get_word_weights(doc)
        sentence_weights = self._get_sentence_weights_from_textrank(doc, sents)

        # Step 1: Extractive — over-select with TextRank (2× target sentences)
        extractive_count = min(num_sentences * 2, len(sents))
        extractive_sents = []
        for sent in doc._.textrank.summary(limit_sentences=extractive_count):
            extractive_sents.append(sent.text)

        extractive_text = " ".join(extractive_sents)

        # Step 2: Abstractive — polish the extractive selection
        # The extractive text is already shorter, so chunking is rarely needed
        max_len = num_sentences * 25
        min_len = max(30, num_sentences * 10)

        # Handle edge case where extractive output is very short
        if len(extractive_text.split()) < min_len:
            # Text is too short for abstractive, return extractive as-is
            return word_weights, sentence_weights, sents, extractive_text

        result = self.summarization_pipeline(
            extractive_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        summary = result[0]['summary_text']
        return word_weights, sentence_weights, sents, summary