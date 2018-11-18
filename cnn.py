from keras import layers, models

from loader import prepare_fit_data


X, Y = prepare_fit_data()

model = models.Sequential()
model.add(layers.Conv2D(32, (5, 5), activation='relu', input_shape=X.shape[1:]))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(32, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Flatten())
model.add(layers.Dropout(.2))
model.add(layers.Dense(500, activation='tanh'))
model.add(layers.Dense(2, activation='softmax'))

model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, Y, validation_split=0.2, epochs=100)

import pdb; pdb.set_trace()

model.save('cnn_tanh.h5')
