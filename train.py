# script for training model(s)

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np
from utils import ProgressBar
import time
from datetime import timedelta

### Data Preparation ###

# Paths to Training Data
DECRYPTED_DIR = "Training/decrypted"
ENCRYPTED_DIR = "Training/encrypted"

# Function to load files
def load_data(num_files):
    encrypted_texts = []
    decrypted_texts = []
    pb = ProgressBar(title="Loading Training Data: ", total=num_files, size=50)
    for i in range(1, num_files + 1):
        pb.update(i)
        file_id = f"tr_{i:05d}"
        dec_file = os.path.join(DECRYPTED_DIR, f"{file_id}.dec")
        enc_file = os.path.join(ENCRYPTED_DIR, f"{file_id}.enc")

        # Read decrypted text
        with open(dec_file, "r") as df:
            decrypted_texts.append(df.read().strip())

        # Read encrypted text
        with open(enc_file, "r", errors='ignore') as ef:
            encrypted_texts.append(ef.read().strip())

    return encrypted_texts, decrypted_texts

start_time = time.time()
# Load data
num_files = 10000  # Adjust as needed
encrypted_data, decrypted_data = load_data(num_files)

print("Formatting Data...")
# Tokenize encrypted and decrypted texts
tokenizer = Tokenizer(char_level=True)  # Character-level tokenizer
tokenizer.fit_on_texts(encrypted_data + decrypted_data)

# Convert text to sequences
encrypted_seq = tokenizer.texts_to_sequences(encrypted_data)
decrypted_seq = tokenizer.texts_to_sequences(decrypted_data)

# Pad sequences to ensure equal lengths
max_len = max(max(len(seq) for seq in encrypted_seq), max(len(seq) for seq in decrypted_seq))
X = pad_sequences(encrypted_seq, maxlen=max_len, padding='post')
y = pad_sequences(decrypted_seq, maxlen=max_len, padding='post')

# Convert to numpy arrays (done in pad_sequences)
#X = np.array(encrypted_seq)
#y = np.array(decrypted_seq)

# Reshape 'y' to fit the LSTM output
y = y.reshape((y.shape[0], y.shape[1], 1))

# Vocabulary size for embedding
vocab_size = len(tokenizer.word_index) + 1


### MODEL ARCHITECTURE ###
print("Defining Model...")
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=128, input_length=max_len),
    LSTM(128, return_sequences=True),  # Sequence-to-sequence processing
    Dense(vocab_size, activation='softmax')  # Output layer predicts characters
])

#Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()


#Train the Model
print("Starting Training...")
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)

#Model Evaluation and Prediction
print("Training Complete!")

# add code to get name from user / check for overwrite
model.save("models/deepkey1.keras")
print("Model Save Sucessfully!")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Script Finished in {str(timedelta(seconds=int(elapsed_time)))}")