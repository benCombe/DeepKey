from DeepKey import DeepKey

dk = DeepKey.load("models/deepkey1.model")

for i in range(1, 11):
    dec_file = f"Testing/decrypted/te_{i:05d}.dec"
    enc_file = f"Testing/encrypted/te_{i:05d}.enc"

    prediction = dk.predict_from_file(enc_file)
    print(f"Prediction:\n{prediction}")

    with open(dec_file, 'r') as file:
        expected = file.read().strip()
        print("Expected:")
        print(expected)

    print("-" * 50)