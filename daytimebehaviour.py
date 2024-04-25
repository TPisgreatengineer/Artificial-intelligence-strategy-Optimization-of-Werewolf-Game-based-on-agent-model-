
import numpy as np
import random
import math

MILDSUSPECT = 0.3
MEDIUMSUSPECT = 0.7
SERIOUSSUSPECT = 1

WEIGHT = 0.6


class DayTime:
    def __init__(self):
        self.deathCause_Voting = 1
        self.deathCause_Gun = 2

    def Speak(self, logicMatrix, werwolfList, villagerList, prophetList, aliveList, identityList, identifyMatrix,
              gameRound, beSeenList):
        identityList = [0] * 12
        werwolfIntoProphet = False
        speakMatrix = np.zeros((12, 12))  # 创建发言矩阵
        for i in range(12):
            if i in werwolfList:  # 狼人发言
                speakflag = 0
                # 报身份
                if identityList[i] != 3:
                    if 3 in identityList and werwolfIntoProphet == False and 0.3 < random.random():
                        identityList[i] = 3
                        werwolfIntoProphet = True
                    elif 3 not in identityList and werwolfIntoProphet == False and 0.7 < random.random():
                        identityList[i] = 3
                        werwolfIntoProphet = True
                    else:
                        identityList[i] = 2
                else:
                    identityList[i] = 3
                # 对其他人身份表示猜测
                if identityList[i] == 3:  # 预言家进行额外指认
                    if random.random() > 0.3:
                        for j in werwolfList:
                            if j != i and j not in identifyMatrix[:, i, 0]:
                                identifyMatrix[gameRound - 1, i, 0] = j
                                identifyMatrix[gameRound - 1, i, 1] = 2
                                break
                    else:
                        for j in list(set(aliveList) - set(werwolfList)):
                            if j not in identifyMatrix[:, i, 0]:
                                identifyMatrix[gameRound - 1, i, 0] = j
                                identifyMatrix[gameRound - 1, i, 1] = 1
                                break

                sortList = list(np.sort(logicMatrix[i, i]))
                if (len(aliveList) >= 5):
                    maxSuspect = sortList[-4]
                else:
                    maxSuspect = sortList[-(int(len(sortList) - 1))]
                speakList = list(set(list(np.where(logicMatrix[i, i] >= maxSuspect)[0])) & set(
                    list(np.where(logicMatrix[i, i] >= 2))[0]))
                random.shuffle(speakList)
                for j in speakList:
                    if (logicMatrix[i, i, j] <= 2.3):
                        speakMatrix[i, j] = MILDSUSPECT
                    if (2.3 <= logicMatrix[i, i, j] < 2.7):
                        speakMatrix[i, j] = MEDIUMSUSPECT
                    if (logicMatrix[i, i, j] > 2.7):
                        speakMatrix[i, j] = SERIOUSSUSPECT
                    speakflag += 1
                    if (speakflag == 4):
                        break
            if i in villagerList:  # 村民发言
                speakflag = 0
                # 报身份
                if identityList[i] != 3:
                    if 3 not in identityList and random.random() < 0.05:
                        identityList[i] = 3
                    else:
                        identityList[i] = 2
                else:
                    identityList[i] = 3
                sortList = list(np.sort(logicMatrix[i, i]))
                if (len(aliveList) >= 5):
                    maxSuspect = sortList[3]
                else:
                    maxSuspect = sortList[int(len(sortList) - 1)]
                speakList = list(set(list(np.where(logicMatrix[i, i] <= maxSuspect)[0])) & set(
                    list(np.where(logicMatrix[i, i] < 2))[0]))
                if identityList[i] == 3:  # 预言家进行额外指认
                    if random.random() > 0.3:
                        for j in speakList:
                            if j not in identifyMatrix[:, i, 0]:
                                identifyMatrix[gameRound - 1, i, 0] = j
                                identifyMatrix[gameRound - 1, i, 1] = 1
                                break
                # 对其他人身份表示猜测
                random.shuffle(speakList)
                for j in speakList:
                    if (logicMatrix[i, i, j] >= 1.7):
                        speakMatrix[i, j] = MILDSUSPECT
                    if (1.3 <= logicMatrix[i, i, j] < 1.7):
                        speakMatrix[i, j] = MEDIUMSUSPECT
                    if (logicMatrix[i, i, j] < 1.3):
                        speakMatrix[i, j] = SERIOUSSUSPECT
                    speakflag += 1
                    if (speakflag == 4):
                        break
            if i in prophetList:  # 预言家发言
                speakflag = 0
                # 报身份
                if identityList[i] != 3:
                    if 3 not in identityList:
                        identityList[i] = 3
                    elif 3 in identityList and random.random() <= 0.7:
                        identityList[i] = 3
                    else:
                        identityList[i] = 2
                else:
                    identityList[i] = 3
                if identityList[i] == 3:  # 预言家进行额外指认
                    if random.random() > 0.3:
                        for j in aliveList:
                            if j not in identifyMatrix[:, i, 0] and beSeenList[j] == True:
                                identifyMatrix[gameRound - 1, i, 0] = j
                                identifyMatrix[gameRound - 1, i, 1] = 1
                                break

                # 对其他人身份表示猜测
                sortList = list(np.sort(logicMatrix[i, i]))
                if (len(aliveList) >= 5):
                    maxSuspect = sortList[3]
                else:
                    maxSuspect = sortList[int(len(sortList) - 1)]
                speakList = list(set(list(np.where(logicMatrix[i, i] <= maxSuspect)[0])) & set(
                    list(np.where(logicMatrix[i, i] < 2))[0]))
                random.shuffle(speakList)
                for j in speakList:
                    if (logicMatrix[i, i, j] >= 1.7):
                        speakMatrix[i, j] = MILDSUSPECT
                    if (1.3 <= logicMatrix[i, i, j] < 1.7):
                        speakMatrix[i, j] = MEDIUMSUSPECT
                    if (logicMatrix[i, i, j] < 1.3):
                        speakMatrix[i, j] = SERIOUSSUSPECT
                    speakflag += 1
                    if (speakflag == 4):
                        break
        return speakMatrix, identityList

    def Vote(self, logicMatrix, werwolfList, villagerList, prophetList, aliveList):
        # 投票行为
        weedOutList = [0] * 12  # 创建淘汰矩阵
        voteMatrix = np.zeros((12, 2))  # 重置投票矩阵
        # 村民
        for i in range(12):
            if i in villagerList:
                # 熵值法算法计算过程
                total = 0
                timer = 0
                pList = 12 * [0]
                eList = 12 * [0]
                dList = 12 * [0]
                wList = 12 * [0]
                for j in range(12):
                    sum1 = 0
                    sum2 = 0
                    for k in range(12):
                        if abs(logicMatrix[i, k, j]) > 5:
                            sum1 = sum1 + 2
                        else:
                            sum1 = sum1 + logicMatrix[i, k, j]
                    for p in range(12):
                        if abs(logicMatrix[i, p, j]) > 5:
                            Pij = 2 / sum1
                        else:
                            Pij = logicMatrix[i, p, j] / sum1
                        pList[p] = Pij
                    for l in range(12):
                        sum2 = sum2 + pList[l] * math.log(pList[l], math.e)
                    eList[timer] = -WEIGHT * sum2
                    dList[timer] = 1 - eList[timer]
                    timer = timer + 1
                for n in range(12):
                    total = total + dList[n]
                for m in range(12):
                    wList[m] = 1 - dList[m] / total
                # 以熵值法计算值为比例系数计算投票矩阵
                voteList = 12 * [0]
                for j in range(12):
                    voteList[j] = logicMatrix[i, i, j] * wList[j]
                choice = np.where(voteList == np.min(voteList))
                if len(choice[0]) == 1:
                    voteMatrix[i, 0] = choice[0][0]
                    if logicMatrix[i, i, choice[0][0]] < 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                elif choice[0][0] == 1:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    voteMatrix[i, 1] = True
                elif (random.random() > 0.2 or len(villagerList) + len(prophetList) == 1) and choice[0][0] < 2:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    if logicMatrix[i, i, choice[0][0]] < 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                else:
                    voteMatrix[i, 1] = False
                if voteMatrix[i, 1] == True and voteMatrix[i, 0] not in aliveList:
                    print(aliveList, voteMatrix[i, 0])
                    print(logicMatrix[i, i])
                    print("村民投票列表")
                    print(voteList)
                # 预言家
            if i in prophetList:
                # 熵值法算法计算过程
                total = 0
                timer = 0
                pList = 12 * [0]
                eList = 12 * [0]
                dList = 12 * [0]
                wList = 12 * [0]
                for j in range(12):
                    sum1 = 0
                    sum2 = 0
                    for k in range(12):
                        if abs(logicMatrix[i, k, j]) > 5:
                            sum1 = sum1 + 2
                        else:
                            sum1 = sum1 + logicMatrix[i, k, j]
                    for p in range(12):
                        if abs(logicMatrix[i, p, j]) > 5:
                            Pij = 2 / sum1
                        else:
                            Pij = logicMatrix[i, p, j] / sum1
                        pList[p] = Pij
                    for l in range(12):
                        sum2 = sum2 + pList[l] * math.log(pList[l], math.e)
                    eList[timer] = -WEIGHT * sum2
                    dList[timer] = 1 - eList[timer]
                    timer = timer + 1
                for n in range(12):
                    total = total + dList[n]
                for m in range(12):
                    wList[m] = 1 - dList[m] / total
                # 以熵值法计算值为比例系数计算投票矩阵
                voteList = 12 * [0]
                for j in range(12):
                    voteList[j] = logicMatrix[i, i, j] * wList[j]
                choice = np.where(voteList == np.min(voteList))
                if len(choice[0]) == 1:
                    voteMatrix[i, 0] = choice[0][0]
                    if logicMatrix[i, i, choice[0][0]] < 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                elif choice[0][0] == 1:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    voteMatrix[i, 1] = True
                elif (random.random() > 0.2 or len(villagerList) + len(prophetList) == 1) and choice[0][0] != 1:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    if logicMatrix[i, i, choice[0][0]] < 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                else:
                    voteMatrix[i, 1] = False

                if voteMatrix[i, 1] == True and voteMatrix[i, 0] not in aliveList:
                    print(aliveList, voteMatrix[i, 0])
                    print("预言家投票列表")
                    print(voteList)
                # 狼人
            if i in werwolfList:
                # 熵值法算法计算过程
                total = 0
                timer = 0
                pList = 12 * [0]
                eList = 12 * [0]
                dList = 12 * [0]
                wList = 12 * [0]
                for j in range(12):
                    sum1 = 0
                    sum2 = 0
                    for k in range(12):
                        if abs(logicMatrix[i, k, j]) > 5:
                            sum1 = sum1 + 2
                        else:
                            sum1 = sum1 + logicMatrix[i, k, j]
                    for p in range(12):
                        if abs(logicMatrix[i, p, j]) > 5:
                            Pij = 2 / sum1
                        else:
                            Pij = logicMatrix[i, p, j] / sum1
                        pList[p] = Pij
                    for l in range(12):
                        sum2 = sum2 + pList[l] * math.log(pList[l], math.e)
                    eList[timer] = -WEIGHT * sum2
                    dList[timer] = 1 - eList[timer]
                    timer = timer + 1
                for n in range(12):
                    total = total + dList[n]
                for m in range(12):
                    wList[m] = 1 - dList[m] / total
                # 以熵值法计算值为比例系数计算投票矩阵
                voteList = 12 * [0]
                for j in range(12):
                    voteList[j] = logicMatrix[i, i, j] * wList[j]
                choice = np.where(voteList == np.max(voteList))
                if len(choice[0]) == 1:
                    voteMatrix[i, 0] = choice[0][0]
                    if logicMatrix[i, i, choice[0][0]] >= 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                elif choice[0][0] == 3:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    voteMatrix[i, 1] = True
                elif (random.random() > 0.2 or len(werwolfList) == 1) and choice[0][0] != 3:
                    voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                    if logicMatrix[i, i, choice[0][0]] >= 2:
                        voteMatrix[i, 1] = True
                    else:
                        voteMatrix[i, 1] = False
                else:
                    voteMatrix[i, 1] = False

                if voteMatrix[i, 1] == True and voteMatrix[i, 0] not in aliveList:
                    print(aliveList, voteMatrix[i, 0])
                    print("狼人投票列表")
                    print(voteList)
        # 投票后对选中角色进行淘汰
        for i in range(12):
            if voteMatrix[i, 1] == True:
                weedOutList[int(voteMatrix[i, 0])] += 1
        # print("投票列表",weedOutList)
        if all(i is 0 for i in weedOutList):
            # print("无人流放")
            weedOutRole = 13
        else:
            weedOutRole = weedOutList.index(max(weedOutList))

        print("投票矩阵")
        print(voteMatrix)
        # 重置投票矩阵
        voteMatrix = np.zeros((12, 2))

        return weedOutRole, self.deathCause_Voting


