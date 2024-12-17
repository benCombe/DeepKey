# load model and use for testing/predictions

import os
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import pad_sequences
import numpy as np

class DeepKey:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found as: {model_path}")
        print("Loading Model...")
        self.model = load_model(model_path)
        print("Model loaded successfully!")

    def preprocess_input(self, input_text, tokenizer, max_len):
        """
        Preprocesses input text to match the model's input format.
        input_text: Text to preprocess.
        tokenizer: Tokenizer used during training.
        max_len: Maximum length of input sequences.
        """
        sequence = tokenizer.texts_to_sequences([input_text])
        padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
        return np.array(padded_sequence) # Preprocessed input as a NumPy array.

    def predict(self, input_text, tokenizer, max_len):
        """
        Predicts the output for a given input text.
        input_text: Encrypted text to decrypt/predict.
        tokenizer: Tokenizer used during training.
        max_len: Maximum sequence length.
        """
        # Preprocess input
        processed_input = self.preprocess_input(input_text, tokenizer, max_len)

        # Get predictions
        predictions = self.model.predict(processed_input)
        predicted_indices = np.argmax(predictions, axis=-1)

        # Decode the predictions back to text
        return self.decode_sequence(predicted_indices[0], tokenizer) # Predicted decrypted text.

    @staticmethod
    def decode_sequence(sequence, tokenizer):
        """
        Decodes a sequence of indices into readable text.
        sequence: Sequence of character indices.
        tokenizer: Tokenizer used during training.
        """
        reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
        return ''.join([reverse_word_index.get(idx, '') for idx in sequence if idx > 0]) # Decoded text string

