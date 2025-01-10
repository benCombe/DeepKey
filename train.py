# script for training model(s)

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, GRU, Dense, Dropout, BatchNormalization, Bidirectional
import numpy as np
import matplotlib.pyplot as plt
from utils import ProgressBar
import time
import csv
from datetime import timedelta
from DeepKey import DeepKey

### Data Preparation ###

# Paths to Training Data
DECRYPTED_DIR = "Training/decrypted"
ENCRYPTED_DIR = "Training/encrypted"

# Function to load files
def load_data(num_files, enc_type="rsa"):
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
        if enc_type != "xor":
            with open(enc_file, "r", errors='ignore') as ef:
                encrypted_texts.append(ef.read().strip())
        else:
            with open(enc_file, "rb") as ef:
                encrypted_bytes = ef.read()
                # Convert bytes to a string representation for tokenization
                encrypted_text = ''.join(format(byte, '02x') for byte in encrypted_bytes)
                encrypted_texts.append(encrypted_text)


    return encrypted_texts, decrypted_texts

start_time = time.time()
# Load data
num_files = 1000  # Adjust as needed
encrypted_data, decrypted_data = load_data(num_files, enc_type="rsa") # change encryption type

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
    LSTM(256, return_sequences=True), # Sequence-to-sequence processing
    LSTM(256, return_sequences=True),
    Dense(vocab_size, activation='relu'),
    Dense(vocab_size, activation='softmax')  # Output layer predicts characters
])

#Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()


#Train the Model
print("Starting Training...")
history = model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)



dk = DeepKey(model=model, tokenizer=tokenizer, max_len=max_len)

#Model Evaluation and Prediction
print("Training Complete!")

# add code to get name from user / check for overwrite
dk.save("models/deepkey_rsa1.model")
print("Model Save Sucessfully!")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Script Finished in {str(timedelta(seconds=int(elapsed_time)))}")

training_loss = history.history['loss']
training_accuracy = history.history['accuracy']
validation_loss = history.history.get('val_loss', [])
validation_accuracy = history.history.get('val_accuracy', [])

csv_file = "training_metrics.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    header = ['Epoch', 'Training Loss', 'Training Accuracy', 'Validation Loss', 'Validation Accuracy']
    writer.writerow(header)
    
    # Write the data for each epoch
    for epoch in range(len(training_loss)):
        row = [
            epoch + 1,  # Epoch number
            training_loss[epoch],
            training_accuracy[epoch],
            validation_loss[epoch] if validation_loss else None,
            validation_accuracy[epoch] if validation_accuracy else None
        ]
        writer.writerow(row)

print(f"Training metrics saved to {csv_file}")

# Plot Loss
plt.figure(figsize=(10, 5))
plt.plot(training_loss, label='Training Loss')
if validation_loss:
    plt.plot(validation_loss, label='Validation Loss')
plt.title('Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot Accuracy
plt.figure(figsize=(10, 5))
plt.plot(training_accuracy, label='Training Accuracy')
if validation_accuracy:
    plt.plot(validation_accuracy, label='Validation Accuracy')
plt.title('Accuracy Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()