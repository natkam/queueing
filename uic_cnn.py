from keras import layers, models

from loader import prepare_uic_data

X, Y = prepare_uic_data()
X = X.reshape(*X.shape, 1)

model = models.Sequential()
model.add(layers.Conv2D(32, (5, 5), activation='relu', input_shape=X.shape[1:]))
model.add(layers.MaxPooling2D())
model.add(layers.Conv2D(32, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D())
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(.2))
model.add(layers.Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
model.fit(X, Y, validation_split=.2, epochs=10)
model.save('uic_cnn.h5')
