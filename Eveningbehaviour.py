import numpy as np
import random


class Evening:
    def __init__(self):
        self.deathCause_Werwolf = 3
        self.deathCause_Poison = 4

    def Seer(self, logicMatrix, werwolfList, villagerList, prophetList, beSeenList):  # 夜晚预言家查看阶段
        for i in prophetList:
            choiceList = list(logicMatrix[i, i])
            ChoiceListSorted = sorted(choiceList)
            for j in range(12):
                if beSeenList[j] != True:
                    beSeenValue = ChoiceListSorted[j]
                    break
            for n in range(12):
                if choiceList[n] == beSeenValue:
                    beSeen = n
                    break

            if beSeen in werwolfList:
                logicMatrix[i, i, beSeen] = 1
                beSeenList[beSeen] = True
            if beSeen in villagerList:
                logicMatrix[i, i, beSeen] = 2
                beSeenList[beSeen] = True
            print(beSeenList)
            print("预言家查看了", n, "其身份是", logicMatrix[i, i, beSeen])

    def Kill(self, logicMatrix, werwolfList):
        weedOutList = [0] * 12  # 创建淘汰矩阵
        voteMatrix = np.zeros((12, 4))  # 重置投票矩阵
        # 夜晚狼人猎杀阶段
        for i in werwolfList:
            choice = np.where(logicMatrix[i, i] == np.max(logicMatrix[i, i]))
            if len(choice[0]) == 1:
                voteMatrix[i, 0] = choice[0][0]
                if logicMatrix[i, i, choice[0][0]] >= 2:
                    voteMatrix[i, 1] = True
                else:
                    voteMatrix[i, 1] = False
            elif choice[0][0] == 3:
                voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                voteMatrix[i, 1] = True
            elif (random.random() > 0.2 or len(werwolfList)) and choice[0][0] != 1:
                voteMatrix[i, 0] = choice[0][random.randint(0, len(choice[0]) - 1)]
                if logicMatrix[i, i, choice[0][0]] >= 2:
                    voteMatrix[i, 1] = True
                else:
                    voteMatrix[i, 1] = False
            else:
                voteMatrix[i, 1] = False
        # 投票后对选中角色进行
        for i in range(12):
            if voteMatrix[i, 1] == True:
                weedOutList[int(voteMatrix[i, 0])] += 1
        if all(i is 0 for i in weedOutList):
            # print("这是一个平安夜")
            killedRole = 13
        else:
            killedRole = weedOutList.index(max(weedOutList))
        # print("狼人投票:",weedOutList)

        return killedRole, self.deathCause_Werwolf
