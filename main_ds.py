import os
import xml.etree.ElementTree as ET
import sys
import time
import copy
import numpy as np
os.system("")

# haiのint変換+４で割って重複削除
def IntChanger(x):
    hai=x
    hai = hai.split(",")
    hai = [int(n) for n in hai]
    hai = [int(n/4) for n in hai]
    return hai

# 試合を分ける
def DivideGame(x):
    root=x
    data_memo=[]
    data = []
    N_memo = []
    N=[]
    hai0=[]
    hai1=[]
    hai2=[]
    hai3=[]
    for child in root:
        if child.tag == "INIT":
            hai0_memo=IntChanger(child.attrib["hai0"])
            hai1_memo=IntChanger(child.attrib["hai1"])
            hai2_memo=IntChanger(child.attrib["hai2"])
            hai3_memo=IntChanger(child.attrib["hai3"])
        elif child.tag == "N":
            N_memo.append(copy.deepcopy(child.attrib))
            data_memo.append("N" + str(len(N_memo) - 1))
        elif child.tag=="AGARI" or child.tag=="RYUUKYOKU":
            # 親配列への継承と子配列の初期化
            data.append(copy.deepcopy(data_memo))
            N.append(copy.deepcopy(N_memo))
            hai0.append(copy.deepcopy(hai0_memo))
            hai1.append(copy.deepcopy(hai1_memo))
            hai2.append(copy.deepcopy(hai2_memo))
            hai3.append(copy.deepcopy(hai3_memo))
            data_memo=[]
            N_memo=[]
            hai0_memo=0
            hai1_memo=0
            hai2_memo=0
            hai3_memo=0
        elif not (child.tag == "SHUFFLE" or child.tag == "GO" or child.tag == "UN" or child.tag=="DORA" or child.tag == "TAIKYOKU" or child.tag == "REACH"):
            data_memo.append(copy.deepcopy(child.tag))
    return data,N,hai0,hai1,hai2,hai3


# 文字の一桁から三桁をintへ
def NumberOfDigits(x):
    TAGlist=x
    number=0
    if len(TAGlist) == 2:
        number=int(TAGlist[1])
    elif len(TAGlist) == 3:
        number=int(TAGlist[1]) * 10 + int(TAGlist[2])
    elif len(TAGlist) == 4:
        number=int(TAGlist[1]) * 100 + int(TAGlist[2])*10 +int(TAGlist[3])
    return int(number/4)
def NumberOfDigitsN(x):
    TAGlist=x
    number=0
    if len(TAGlist) == 2:
        number=int(TAGlist[1])
    elif len(TAGlist) == 3:
        number=int(TAGlist[1]) * 10 + int(TAGlist[2])
    elif len(TAGlist) == 4:
        number=int(TAGlist[1]) * 100 + int(TAGlist[2])*10 +int(TAGlist[3])
    return int(number)


# 各人の捨て牌、引き牌の記録
def abandoned(x,y):
    data=x
    N=y
    # ↓インデックスごとに[一人目、二人目、三人目、四人目]
    DisposeHai=[[],[],[],[]]
    DrawHai = [[],[],[],[]]
    # 直近の捨て牌、副露が起きた時に引き牌として設定する
    MostRecent=0
    MostDraw=0
    for i in range(len(data)):
        # TAG=文字列
        # TAGList=文字列を一つ一つの文字に切り分けたもの
        TAG = data[i]
        TAGlist = []
        for i2 in TAG:
            TAGlist.append(copy.deepcopy(i2))
        # D～G=捨て牌
        if TAGlist[0] == "D":
            # Calculationresult=文字の後に続く数(int)
            Calculationresult = NumberOfDigits(TAGlist)
            DisposeHai[0].append(copy.deepcopy(Calculationresult))
            MostRecent = Calculationresult
        if TAGlist[0] == "E":
            Calculationresult = NumberOfDigits(TAGlist)
            DisposeHai[1].append(copy.deepcopy(Calculationresult))
            MostRecent = Calculationresult
        if TAGlist[0] == "F":
            Calculationresult = NumberOfDigits(TAGlist)
            DisposeHai[2].append(copy.deepcopy(Calculationresult))
            MostRecent = Calculationresult
        if TAGlist[0] == "G":
            Calculationresult = NumberOfDigits(TAGlist)
            DisposeHai[3].append(copy.deepcopy(Calculationresult))
            MostRecent = Calculationresult

        # T～W引き牌

        if TAGlist[0] == "T":
            Calculationresult = NumberOfDigits(TAGlist)
            DrawHai[0].append(copy.deepcopy(Calculationresult))
            MostDraw=0
        if TAGlist[0] == "U":
            Calculationresult = NumberOfDigits(TAGlist)
            DrawHai[1].append(copy.deepcopy(Calculationresult))
            MostDraw=1
        if TAGlist[0] == "V":
            Calculationresult = NumberOfDigits(TAGlist)
            DrawHai[2].append(copy.deepcopy(Calculationresult))
            MostDraw=2
        if TAGlist[0] == "W":
            Calculationresult = NumberOfDigits(TAGlist)
            DrawHai[3].append(copy.deepcopy(Calculationresult))
            MostDraw=3
        # Nのとき（副露）のとき引き牌へ設定する
        if TAGlist[0] == "N":
            Ndata = N[NumberOfDigitsN(TAGlist)]
            who = int(Ndata["who"])
            # こっから適当
            mensigawari=0
            if not (len(data)-1)==i:
                tuginote=data[i+1]
            else:
                tuginote="non"
            tuginoteList=[]
            if not tuginote=="non":
                for i2 in tuginote:
                    tuginoteList.append(copy.deepcopy(i2))
                if tuginoteList[0]=="T":
                    mensigawari=0
                elif tuginoteList[0]=="U":
                    mensigawari=1
                elif tuginoteList[0]=="V":
                    mensigawari=2
                elif tuginoteList[0]=="W":
                    mensigawari=3
                else:
                    mensigawari=-1
            else:
                mensigawari=-1
            # ここまで
            # 自分で自分のをカンしたら
            if MostDraw==who:
                # もしカンが四枚なら
                if mensigawari==who:
                    DisposeHai[who].append(-1)
            # ほかの人のをカンしたら
            else:
                DrawHai[who].append(copy.deepcopy(MostRecent))
                # もしカンが四枚なら
                if mensigawari==who:
                    DisposeHai[who].append(-1)
                MostDraw = who

    return DisposeHai,DrawHai


# ファイル名を入れる
def FileAnalysis(x):
    # ファイル名
    Parse=x
    tree=ET.parse(Parse)
    # XMLを取得
    root = tree.getroot()
    # データを試合ごとに分ける,X=帰ってきた全データ[data,N,hai0,hai1,hai2,hai3]
    X=DivideGame(root)
    data=X[0]
    N=X[1]
    hai0=X[2]
    hai1=X[3]
    hai2=X[4]
    hai3=X[5]
    # 引き牌、捨て牌の配列[試合数][参加人数]とする配列
    AllDisposeData=[]
    AllDrawData=[]
    # dataを一人目から四人目までに分ける
    for i in range(len(data)):
        x=abandoned(data[i], N[i])
        AllDisposeData.append(copy.deepcopy(x[0]))
        AllDrawData.append(copy.deepcopy(x[1]))
    return hai0,hai1,hai2,hai3,AllDisposeData,AllDrawData


# 画像データ作成,一試合ごと

def ImageCreation(x):
    # 2Dのデータ
    TwoDimensionsdata=[]
    OneDisposeData=x
    # 累積データ
    AccumulationData=[]
    data=[[0 for i in range(34)]for i2 in range(34)]
    if len(OneDisposeData)>=2:
        AccumulationData.append(copy.deepcopy(OneDisposeData[0]))
        # 初回はスキップ
        FirstTime=0
        for i in OneDisposeData:
            if i>=0:
                if FirstTime==1:
                    for i2 in AccumulationData:
                        data[i2][i] = data[i2][i]+1
                    TwoDimensionsdata.append(copy.deepcopy(data))

                    AccumulationData.append(i)
                else:
                    FirstTime=1
        return TwoDimensionsdata

    else:
        return "non"

# ラベルの計算
def LabelCalculation(x,y,z):
    hai=x
    Dispose=y
    Draw=z
    Allhai=[]
    FirstTime=0
    if len(Dispose)>=2:
        # Dispose>DrawのためDispose
        for i in range(len(Dispose)):
            hai.append(copy.deepcopy(Draw[i]))
            if Dispose[i]>=0:
                hai.remove(Dispose[i])
            if FirstTime==1:
                # print("hai:"+str(hai)+","+"Draw:"+str(Draw[i])+",Dispose:"+str(Dispose[i]))
                lavel=[0 for i in range(34)]
                for i2 in hai:
                    lavel[i2]=lavel[i2]+1
                Allhai.append(copy.deepcopy(lavel))
            else:
                FirstTime=1
        return Allhai
    else:
        return "non"


def dev3d(x):
    hairetu=x
    for i in range(len(hairetu)):
        for i2 in range(34):
            for i3 in range(34):
                hairetu[i][i2][i3]=hairetu[i][i2][i3]/8
    return hairetu

def dev2d(x):
    hairetu=x
    for i in range(len(hairetu)):
        for i2 in range(34):
            hairetu[i][i2]=hairetu[i][i2]/8
    return hairetu

# main
# x=[hai0,hai1,hai2,hai3,AllDisposeData,AllDrawData]
def mainSplict(x):
    tree=x
    execution=FileAnalysis(tree)
    ImageData=[]
    LabelData=[]
    Allhai0=execution[0]
    Allhai1=execution[1]
    Allhai2=execution[2]
    Allhai3=execution[3]
    FinallDisposeData=execution[4]
    FinallDrawData=execution[5]

    for OnegameDiposeData in FinallDisposeData:
        for i in OnegameDiposeData:
            x=ImageCreation(i)
            if not x=="non":
                x=dev3d(x)
                ImageData.extend(copy.deepcopy(x))


    for i in range(len(FinallDisposeData)):
        Onegamehai0=Allhai0[i]
        Onegamehai1=Allhai1[i]
        Onegamehai2=Allhai2[i]
        Onegamehai3=Allhai3[i]
        Onegamehai=[Onegamehai0,Onegamehai1,Onegamehai2,Onegamehai3]
        OnegameDipose=FinallDisposeData[i]
        OnegameDraw=FinallDrawData[i]
        for i2 in range(4):
            x=LabelCalculation(Onegamehai[i2],OnegameDipose[i2],OnegameDraw[i2])
            if not x=="non":
                x=dev2d(x)
                LabelData.extend(copy.deepcopy(x))
    return zip(ImageData,LabelData)





path="D:/麻雀データ/"
files = os.listdir(path)
files=["2019"]
print("DatasetMaker起動")
filesNumber=0
DatasetPath=[]
DatasetPathNumber=0
for i in files:
    start = time.time()
    filesNumber=filesNumber+1
    files2 = os.listdir(path+i)
    allfiles2Number=len(files2)
    files2Number=0
    print("ファイル名："+str(i)+"      解析中")
    print("進行状況")
    print("残り時間")
    print("全体残り時間")
    for i2 in files2:
        sys.stdout.write("\033[1A\033[2K\033[1A\033[2K\033[1A\033[2K\033[1A\033[2K")
        sys.stdout.flush()
        files2Number=files2Number+1
        print(path+i+"/"+i2)
        print(str(files2Number/allfiles2Number*100)+"%完了")
        process_time = time.time() - start
        average=process_time/files2Number
        print("残り「"+i+"」処理推測時間："+str(int((average*(allfiles2Number-files2Number))/60))+"分")
        print("データセット作成残り時間推測："+str(int((average*(allfiles2Number-files2Number)/60)+(average*allfiles2Number)*(len(files)-filesNumber)/60))+"分")
        x=mainSplict(path+i+"/"+i2)
        for (data,label) in x:
            np.save('D:\\CNNmahjongImageData\\'+str(DatasetPathNumber), np.array(data))
            np.save('D:\\CNNmahjongLabels\\'+str(DatasetPathNumber), np.array(label))
            DatasetPath.append(DatasetPathNumber)
            DatasetPathNumber=DatasetPathNumber+1


print("DatasetMaker・finish")
long=DatasetPathNumber
for i in range(2):
    print()
print("入力2Dデータ数＝"+str(DatasetPathNumber))

