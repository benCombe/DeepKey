# load model and use for testing/predictions

import os
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import pad_sequences
import numpy as np

class DeepKey:
    def __init__(self, model=None, tokenizer=None, max_len=None):
        self.model = model
        self.tokenizer = tokenizer
        self.max_len = max_len

    def preprocess_input(self, input_text):
        sequence = self.tokenizer.texts_to_sequences([input_text])
        padded_sequence = pad_sequences(sequence, maxlen=self.max_len, padding='post')
        return np.array(padded_sequence) # Preprocessed input as a NumPy array.

    def predict(self, input_text):
        # Preprocess input
        processed_input = self.preprocess_input(input_text)

        # Get predictions
        predictions = self.model.predict(processed_input)
        predicted_indices = np.argmax(predictions, axis=-1)

        # Decode the predictions back to text
        return self.decode_sequence(self=self,sequence=predicted_indices[0]) # Predicted decrypted text.

    @staticmethod
    def decode_sequence(self, sequence):
        reverse_word_index = {v: k for k, v in self.tokenizer.word_index.items()}
        return ''.join([reverse_word_index.get(idx, '') for idx in sequence if idx > 0]) # Decoded text string
    
    def predict_from_file(self, enc_file_path):
        if not os.path.exists(enc_file_path):
            raise FileNotFoundError(f"Encrypted file not found at: {enc_file_path}")

        # Load the encrypted file content
        with open(enc_file_path, "rb") as ef:
            encrypted_text = ef.read().decode("utf-8", errors="ignore")  # Decode as UTF-8 for processing

        # Make the prediction
        return self.predict(encrypted_text)
    

    def save(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)
        print(f"DeepKey instance saved successfully to {file_path}")

    @staticmethod
    def load(file_path):
        with open(file_path, "rb") as file:
            deepkey_instance = pickle.load(file)
        print("DeepKey instance loaded successfully!")
        return deepkey_instance
    
    def model_summary(self):
        return self.model.summary()

