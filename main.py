import torch
import torch.nn as nn
import torch.optim as optim
import numpy
from Dataset import trainloader
from Dataset import Datanumber
from Dataset import BATCHSIZE
import sys
import os
# 時間
import time
#########
os.system("")
WEIGHT_DECAY = 0.005
LEARNING_RATE = 0.01
EPOCH = int(Datanumber/BATCHSIZE)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, stride=2)
        self.conv1 = nn.Conv2d(1, 16, 1)
        self.conv2 = nn.Conv2d(16, 32, 1)
        self.fc1 = nn.Linear(8*8*32, 500)
        self.fc2 = nn.Linear(500, 34)
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

device = torch.device("cpu")
net = Net().float()
net = net.to(device)
nn.init.xavier_uniform_(nn.Linear(8*8*32,500).weight)
nn.init.xavier_uniform_(nn.Linear(500,34).weight)
nn.init.kaiming_uniform_(nn.Linear(8*8*32,500).weight)
nn.init.kaiming_uniform_(nn.Linear(500,34).weight)
nn.init.constant_(nn.Linear(8*8*32,500).bias, 0)
nn.init.constant_(nn.Linear(500,34).bias, 0)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.SGD(net.parameters(), lr=LEARNING_RATE, momentum=0.9, weight_decay=WEIGHT_DECAY)
for i in range(2):
    print()
print("学習開始   動作環境："+str(device))
start=time.time()
for epoch in range(EPOCH):
    net.train()
    for (inputs, labels) in trainloader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = net(inputs.to(torch.float32))
        labels=labels.to(torch.float32)
        loss = criterion(outputs, labels)
        if torch.isnan(loss):
            print("NanHappen")
            break

        loss.backward()
        optimizer.step()
        del loss
        torch.cuda.empty_cache()
    if epoch == 0:
        print("")
        print("")
        print("")
    sys.stdout.write("\033[1A\033[2K\033[1A\033[2K")
    sys.stdout.flush()
    print(str((epoch / EPOCH) * 100) + "%完了")
    average = (time.time() - start) / (epoch + 1)
    print("残り時間：" + str(int((average * (EPOCH - epoch + 1)) / 60)) + "分")

for i in range(3):
    print()
model_path = 'Dataset数_406144.pth'
torch.save(net.to(device).state_dict(), model_path)
print("SAVE.finish      name="+model_path)