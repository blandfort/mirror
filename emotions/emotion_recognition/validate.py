import torch
from collections import Counter

from training import transform
from dataset import FERPlus
from networks import NetworkBasic
from config import MODEL_PATH, DATA_DIR


testset = FERPlus(DATA_DIR, train=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=True, num_workers=2)


print("Loading the network ...")
net = NetworkBasic(in_c=1, nl=32, out_f=len(FERPlus.classes))
net.load_state_dict(torch.load(MODEL_PATH))
net.eval()

print("Running evaluation ...")
correct = 0
labelcount = Counter()  # To get baseline accuracy
predictcount = Counter()  # To get output baseline
for i, data in enumerate(testloader, 0):
    # get the inputs; data is a list of [inputs, labels]
    inputs, labels = data

    labelcount.update(list(labels.numpy()))

    # forward + backward + optimize
    outputs = net(inputs)
    _, predicted = torch.max(outputs.data, 1)

    predictcount.update(list(predicted.numpy()))

    correct += (predicted == labels).float().sum()

accuracy = 100 * correct / len(testset)
print("Accuracy = %0.2f%%" % accuracy)

print("\nMost common classes (gives baseline accuracy):")
for c_ix,count in labelcount.most_common():
    print("- %s: %0.2f%%" % (testset.classes[c_ix], 100 * count * 1./len(testset)))

print("\nMost common predictions:")
for c_ix,count in predictcount.most_common():
    print("- %s: %0.2f%%" % (testset.classes[c_ix], 100 * count * 1./len(testset)))
