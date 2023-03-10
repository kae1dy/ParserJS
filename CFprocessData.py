import string

punctuations = string.punctuation.replace("\"", "")


def CFProcessTrainDataset(train_dataset):
    source_train = []
    target_train = []
    for data in train_dataset:
        data_group = data.split("\t")
        target = data_group[1]
        source = data_group[0].translate(str.maketrans({key: " {0} ".format(key) for key in punctuations}))
        source_train.append(source)
        target_train.append(target)
    return source_train, target_train


def CFProcessTestDataset(source_test):
    new_source_test = []
    for data in source_test:
        new_data = data.split("code2comment :")[1].translate(str.maketrans({key: " {0} ".format(key) for key in punctuations}))
        new_source_test.append(new_data)
    return new_source_test