import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np

#TODO wrap this thing up as package, so that .networks is used
from networks import NetworkBasic
#from .networks import NetworkBasic
from dataset import FERPlus


transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])


#TODO put paths to configuration files
DATA_DIR = '/home/john/code/webcam/FERPlus/data'
MODEL_PATH = '/home/john/code/webcam/models/own.pt'


if __name__=='__main__':
    # Following https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html

    # Load the datasets
    print("Loading the datasets ...")
    trainset = FERPlus(DATA_DIR, train=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=2)

    testset = FERPlus(DATA_DIR, train=False, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=True, num_workers=2)


    # Initialize the network
    print("Initializing the network ...")
    net = NetworkBasic(in_c=1, nl=32, out_f=len(FERPlus.classes))

    if os.path.isfile(MODEL_PATH):
        print("Loading model state ...")
        net.load_state_dict(torch.load(MODEL_PATH))
        net.train()
        #NOTE: Would be cleaner to also store optimizer state (see https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-a-general-checkpoint-for-inference-and-or-resuming-training)

    # Define the optimizer
    print("Setting up the optimizer ...")
    criterion = nn.CrossEntropyLoss()
    #optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    optimizer = optim.Adam(net.parameters(), lr=0.0001, weight_decay=1e-6)


    # Training
    print("Starting training ...")
    try:
        for epoch in range(20):  # loop over the dataset multiple times

            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 2000 == 1999:    # print every 2000 mini-batches
                    print('[epoch %d, step %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0

            # Validate at end of each epoch
            correct = 0
            for i, data in enumerate(testloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data

                # forward + backward + optimize
                outputs = net(inputs)
                _, predicted = torch.max(outputs.data, 1)

                correct += (predicted == labels).float().sum()
            accuracy = 100 * correct / len(testset)
            print("        validation accuracy: %0.2f%%" % accuracy)

        print('Finished training.')
    except (KeyboardInterrupt, SystemExit):
        print("Training interrupted.")
        raise
    finally:
        print("Saving model state ...")
        torch.save(net.state_dict(), MODEL_PATH)
        print("Model saved.")

