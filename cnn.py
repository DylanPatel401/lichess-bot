import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

# Load data
loaded_data = np.load('state_action_pairs.npz')
states = loaded_data['states']
actions = loaded_data['actions']

# Normalize states (example using min-max normalization)
states_normalized = (states - np.min(states)) / (np.max(states) - np.min(states))

# Split data into training and validation sets
train_states, val_states, train_actions, val_actions = train_test_split(states_normalized, actions, test_size=0.2)

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(8, 8, 12)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4096, activation='softmax')  # Adjust output neurons as needed
])

model.compile(loss='categorical_crossentropy', optimizer='adam')

# Convert actions to one-hot encoding
train_actions_one_hot = tf.keras.utils.to_categorical(train_actions)
val_actions_one_hot = tf.keras.utils.to_categorical(val_actions)

model.fit(train_states, train_actions_one_hot, epochs=10, batch_size=32, validation_data=(val_states, val_actions_one_hot))