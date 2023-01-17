import torch
import numpy as np
import torchvision
import sys
import os
os.system("")
BATCHSIZE=1000
Datanumber=1023
DatasetPathMaker=[]
for i in range(Datanumber+1):
    DatasetPathMaker.append(i)
trans = torchvision.transforms.ToTensor()
print("DatasetMaker終了")
np.save('D:\\a.npy', np.array(str(1)))
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, path):
        self.paths= path
        self.paths_num = len(path)
        # self.label = np.load('D:\\CNNmahjongLabels\\'+str(path))

    def __len__(self):
        return self.paths_num

    def __getitem__(self,idx):
        datasetpath=self.paths[idx]
        out_data = np.load('D:\\CNNmahjongImageData\\'+str(datasetpath)+'.npy')
        out_data=trans(out_data)
        out_label = np.load('D:\\CNNmahjongLabels\\'+str(datasetpath)+'.npy')
        out_label = torch.tensor(out_label, dtype=torch.float32)
        return out_data, out_label

dataset = MyDataset(DatasetPathMaker)

trainloader = torch.utils.data.DataLoader(dataset, batch_size=BATCHSIZE,shuffle=True, num_workers=0,pin_memory=True)

for i in range(2):
    print()
print("Dataset.finish")