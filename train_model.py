from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications.resnet import ResNet50
from tensorflow.keras.optimizers import Adam
import pandas as pd


labels = pd.read_csv('./archive/labels.csv')


def load_train():
    train_datagen = ImageDataGenerator(
        rescale=1/255.,
        horizontal_flip=True,
        rotation_range=15,
        shear_range=0.1,
        zoom_range=0.1
    )
    test_datagen = ImageDataGenerator(rescale=1/255.)
    train_datagen_flow = train_datagen.flow_from_dataframe(
        directory='./archive/train_data',
        dataframe=labels,
        x_col='file_name',
        y_col='real_age',
        target_size=(224, 224),
        batch_size=16,
        subset='training',
        class_mode='raw',
        seed=12345
    )
    test_datagen_flow = test_datagen.flow_from_dataframe(
        directory='./archive/test_data',
        dataframe=labels,
        x_col='file_name',
        y_col='real_age',
        target_size=(224, 224),
        batch_size=16,
        class_mode='raw',
        seed=12345
    )
    return train_datagen_flow, test_datagen_flow


def create_model(input_shape):
    model = Sequential()
    model.add(ResNet50(
        input_shape=input_shape,
        weights='imagenet',
        include_top=False
    ))
    model.add(GlobalAveragePooling2D())
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='relu'))
    model.compile(
        loss='mean_squared_error',
        optimizer=Adam(learning_rate=0.001),
        metrics=['mean_absolute_error'])

    return model


def train_model(
        model,
        train_data,
        test_data,
        batch_size=16,
        epochs=15,
        steps_per_epoch=None,
        validation_steps=None):

    model.fit(
        train_data,
        validation_data=test_data,
        batch_size=batch_size,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        verbose=1,
        shuffle=True
    )

    return model


train_datagen_flow, val_datagen_flow = load_train()
model = create_model((224, 224, 3))
model.summary()
model = train_model(
    model,
    train_datagen_flow,
    val_datagen_flow,
    batch_size=16,
    epochs=50,
    steps_per_epoch=None,
    validation_steps=None
)
model.save("age_detect.h5")
