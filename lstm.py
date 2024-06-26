import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

data = pd.read_csv("Amazon.csv")
data = data['Close'].values.reshape(-1,1)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

train_data = scaled_data[:int(0.8*len(scaled_data))]
test_data = scaled_data[int(0.8*len(scaled_data)):]

def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequence = data[i:i+seq_length]
        sequences.append(sequence)
    return np.array(sequences)

seq_length = 10
X_train = create_sequences(train_data, seq_length)
y_train = train_data[seq_length:]
X_test = create_sequences(test_data, seq_length)
y_test = test_data[seq_length:]

# Early Stopping ve Model Checkpoint geri çağırımlarını tanımlama
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
model_checkpoint = ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)

# Model oluşturma ve eğitme
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(150, input_shape=(seq_length, 1), return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(150, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(150, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(150),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.1, callbacks=[early_stopping, model_checkpoint])

# Tahminler yapma
predictions = model.predict(X_test)

# Tahminleri gerçek verilerle karşılaştırma
plt.figure(figsize=(14, 7))
plt.plot(scaler.inverse_transform(y_test), label='Gerçek Veri')
plt.plot(scaler.inverse_transform(predictions), label='Tahminler')
plt.title('Google Hisse Senedi Kapanış Fiyatı Tahminleri')
plt.xlabel('Zaman')
plt.ylabel('Kapanış Fiyatı')
plt.legend()
plt.show()
