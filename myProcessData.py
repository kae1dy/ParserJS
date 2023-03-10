from func import parse_code

def myProcessTrainDataset(train_dataset):
    source_train = []
    target_train = []
    for data in train_dataset:
        data_group = data.split("\t")

        target = data_group[1]
        source = data_group[0]

        source_train.append(source)
        target_train.append(target)
    source_train = parse_code(source_train)
    return source_train, target_train


def myProcessTestDataset(source_test):
    new_source_test = []
    for data in source_test:
        new_data = data.split("code2comment :")[1]
        new_source_test.append(new_data)
    new_source_test = parse_code(new_source_test)
    return new_source_test