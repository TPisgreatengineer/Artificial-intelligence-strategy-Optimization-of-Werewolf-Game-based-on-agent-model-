from tkinter import E
import numpy as np
import random


def Limit(i):
    if abs(i) < 90:
        if i > 3:
            i = 3
        elif i < 1:
            i = 1
    else:
        i = 100 * i / abs(i)
    return i


def WerwolfLimit(i):
    if abs(i) < 90:
        if i > 3:
            i = 3
        elif i < 2:
            i = 2
    else:
        i = 100 * i / abs(i)
    return i


# 角色判定值
WERWOLF_VALUE = 1  # 狼人
VILLAGER_VALUE = 2  # 村民
PROPHET_VALUE = 3  # 预言家
HUNTER_VALUE = 2.1  # 猎人
WITCH_VALUE = 2.5  # 女巫
IDIOT_VALUE = 2.1  # 白痴

# 出局方式
GUN = 2.5  # 猎枪
WERWOLF = -2.5  # 狼人
POISON = 2  # 毒药
VOTING = 1  # 公投


# 定义类作为初始化游戏数据的方法
class Matrix:
    def __init__(self, headcount, isplayer):
        self.headcount = headcount
        self.isplayer = isplayer

    def InitMatrix(self):

        # 初始逻辑矩阵建立
        o_LogicMatrix = np.zeros((12, 12, 12))

        # 初始角色信息信息矩阵
        o_RoleInformationMatrix = np.zeros((12, 4))  # 第一列：身份 第二列：是否AI 第三列：死亡时间 第四列：死亡原因

        # 人物列表生成
        aliveList = list(range(0, 12))  # 存活人物列表，将会在之后更新

        # 自述身份列表
        identityList = 12 * [0]

        # 轮次发言矩阵
        speakMartrixGroup = np.zeros((15, 12, 12))

        # 真预言家探查列表
        beSeenList = 12 * [0]

        # 预言家指认列表
        temp = 288 * [-1]
        identifyMatrix = np.array(temp).reshape(12, 12, 2)

        totalList = list(range(0, 12))
        random.shuffle(totalList)
        # 狼人
        werwolfList = totalList[0:4]
        not_WerwolfList = list(set(totalList) - set(werwolfList))
        # 村民
        villagerList = totalList[4:11]
        not_VillagerList = list(set(totalList) - set(villagerList))
        # 预言家
        prophetList = totalList[11:12]
        not_ProphetList = list(set(totalList) - set(prophetList))

        # 狼人逻辑矩阵对初始逻辑矩阵进行覆盖
        for i in werwolfList:
            o_LogicMatrix[i] = np.full((12, 12), 2)
            o_RoleInformationMatrix[i, 0] = 1
            random.shuffle(not_WerwolfList)
            for j in werwolfList:
                o_LogicMatrix[i, i, j] = WERWOLF_VALUE
            for k in range(4):
                o_LogicMatrix[i, i, not_WerwolfList[k]] += random.uniform(0, 0.1)
        # 村民逻辑矩阵对初始逻辑矩阵进行覆盖
        for i in villagerList:
            o_LogicMatrix[i] = np.full((12, 12), 2)
            o_RoleInformationMatrix[i, 0] = 2
            random.shuffle(not_VillagerList)
            for k in range(4):
                o_LogicMatrix[i, i, not_VillagerList[k]] += random.uniform(-0.1, 0.1)
        # 预言家逻辑矩阵对初始逻辑矩阵进行覆盖
        for i in prophetList:
            o_LogicMatrix[i] = np.full((12, 12), 2)
            o_RoleInformationMatrix[i, 0] = 3
            o_LogicMatrix[i, i, i] = PROPHET_VALUE;
            random.shuffle(not_ProphetList)
            for k in range(4):
                o_LogicMatrix[i, i, not_ProphetList[k]] += random.uniform(-0.1, 0.1)

        return o_LogicMatrix, o_RoleInformationMatrix, werwolfList, villagerList, prophetList, aliveList, identityList, speakMartrixGroup, identifyMatrix, beSeenList

    def Thinkdeath(self, logicMatrix, werwolfList, villagerList, prophetList, speakMartrixGroup, identityList,
                   gameRound, killedRole, deathCause, identifyMatrix, beSeenList, K1, K2):
        if gameRound != 1 and killedRole != 13:
            if deathCause == 3:
                for i in range(12):
                    if i in villagerList:
                        logicMatrix[i, i, killedRole] = logicMatrix[i, i, killedRole] + 1
                        for j in range(gameRound - 2, gameRound - 1):
                            for n in range(12):
                                if n != i:
                                    if identityList[n] == 3 and speakMartrixGroup[j, n, killedRole] != 0:
                                        if abs(logicMatrix[i, i, n]) < 50:
                                            logicMatrix[i, i, n] = logicMatrix[i, i, n] - 0.15
                                            if identifyMatrix[j][n, 0] == killedRole and identifyMatrix[j][n, 1] == 1:
                                                for h in range(gameRound):
                                                    if identifyMatrix[h][n, 0] != -1:
                                                        if abs(logicMatrix[i, i, identifyMatrix[h][n, 0]]) < 50 and \
                                                                logicMatrix[i, i, identifyMatrix[h][n, 1]] == 1:
                                                            logicMatrix[i, i, identifyMatrix[h][n, 0]] = Limit(
                                                                logicMatrix[i, i, identifyMatrix[h][n, 0]] + 1)
                                                        if abs(logicMatrix[i, i, identifyMatrix[h][n, 0]]) < 50 and \
                                                                logicMatrix[i, i, identifyMatrix[h][n, 1]] != 1:
                                                            logicMatrix[i, i, identifyMatrix[h][n, 0]] = Limit(
                                                                logicMatrix[i, i, identifyMatrix[h][n, 0]] - 1)
                                    if speakMartrixGroup[j, n, killedRole] != 0:
                                        logicMatrix[i, i, n] = Limit(
                                            logicMatrix[i, i, n] - K1 * speakMartrixGroup[j, n, killedRole])
                                    if speakMartrixGroup[j, killedRole, n] != 0:
                                        logicMatrix[i, i, n] = Limit(
                                            logicMatrix[i, i, n] - K2 * speakMartrixGroup[j, killedRole, n])
                        for j in range(gameRound):
                            for n in range(12):
                                if n != i:
                                    if identifyMatrix[j, n, 0] == killedRole and identifyMatrix[j, n, 1] == 1:
                                        logicMatrix[i, i, n] = Limit(logicMatrix[i, i, n] - 2)
                                    if identifyMatrix[j, n, 0] == killedRole and identifyMatrix[j, n, 1] == 2:
                                        logicMatrix[i, i, n] = Limit(logicMatrix[i, i, n] + 2)
                    if i in prophetList:
                        for j in range(gameRound - 2, gameRound - 1):
                            for n in range(12):
                                if n != i and beSeenList[n] != True:
                                    if speakMartrixGroup[j, n, killedRole] != 0:
                                        logicMatrix[i, i, n] = Limit(
                                            logicMatrix[i, i, n] - K1 * speakMartrixGroup[j, n, killedRole])
                                    if speakMartrixGroup[j, killedRole, n] != 0:
                                        logicMatrix[i, i, n] = Limit(
                                            logicMatrix[i, i, n] - K2 * speakMartrixGroup[j, killedRole, n])

    def ThinkSpeak(self, logicMatrix, werwolfList, villagerList, prophetList, speakMatrix, identityList, beSeenList,
                   identifyMatrix, gameRound, A1, A2, A3, A4, A5, A6):
        for i in range(12):
            for j in range(12):
                if j != i:
                    if j in werwolfList:
                        judgement = 2 - logicMatrix[j, j, i]
                        for n in range(12):
                            if identityList[n] == 3 and n != j and logicMatrix[j, j, n] != 1:
                                if identifyMatrix[gameRound - 1, n, 0] in werwolfList and identifyMatrix[
                                    gameRound - 1, n, 1] == 1:
                                    logicMatrix[j, j, n] = 3
                                elif identifyMatrix[gameRound - 1][n, 0] not in werwolfList and \
                                        identifyMatrix[gameRound - 1][n, 1] != 1:
                                    logicMatrix[j, j, n] = 3
                                else:
                                    logicMatrix[j, j, n] = 2
                            if n not in werwolfList and speakMatrix[i, n] != 0 and logicMatrix[j, j, n] != 1:
                                logicMatrix[j, j, n] = WerwolfLimit(
                                    logicMatrix[j, j, n] + A1 * judgement * speakMatrix[i, n])
                                logicMatrix[j, i, n] = WerwolfLimit(logicMatrix[j, i, n] + A2 * speakMatrix[i, n])
                    if j in villagerList:
                        judgement = logicMatrix[j, j, i] - 2
                        for n in range(12):
                            if identityList[n] == 3 and n != j:
                                logicMatrix[j, j, n] = Limit(logicMatrix[j, j, n] + 0.5 * judgement)
                                logicMatrix[j, j, n] = Limit(logicMatrix[j, j, n] - 0.5 * judgement * speakMatrix[i, n])
                                if judgement > 2.5 and identifyMatrix[gameRound - 1][n, 1] != -1:
                                    logicMatrix[j, j, identifyMatrix[gameRound - 1][n, 0]] = \
                                    identifyMatrix[gameRound - 1][n, 1]
                            if n != j and speakMatrix[i, n] != 0:
                                logicMatrix[j, j, n] = Limit(logicMatrix[j, j, n] - A3 * judgement * speakMatrix[i, n])
                                logicMatrix[j, i, n] = Limit(logicMatrix[j, i, n] - A4 * speakMatrix[i, n])
                    if j in prophetList:
                        judgement = logicMatrix[j, j, i] - 2
                        for n in range(12):
                            if identityList[n] == 3 and n != j and beSeenList[n] != True:
                                logicMatrix[j, j, n] = 1
                            if n != j and speakMatrix[i, n] != 0 and beSeenList[n] != True:
                                logicMatrix[j, j, n] = Limit(logicMatrix[j, j, n] - A5 * judgement * speakMatrix[i, n])
                                logicMatrix[j, i, n] = Limit(logicMatrix[j, i, n] - A6 * speakMatrix[i, n])

    def WeedOut(self, logicMatrix, roleInformationMatrix, werwolfList, villagerList, prophetList, aliveList,
                weedOutRole, gameRound, deathCause):
        # 投票后对选中角色进行淘汰

        # 删除人物列表中对应元素
        if weedOutRole in werwolfList:
            werwolfList.remove(weedOutRole)
        if weedOutRole in villagerList:
            villagerList.remove(weedOutRole)
        if weedOutRole in prophetList:
            prophetList.remove(weedOutRole)
            # 更新逻辑矩阵,将淘汰人员威胁度降至最低
        for i in werwolfList:
            logicMatrix[i, i, weedOutRole] = -100
        for i in villagerList:
            logicMatrix[i, i, weedOutRole] = 100
        for i in prophetList:
            logicMatrix[i, i, weedOutRole] = 100
        # 更新存活角色列表
        aliveList.remove(weedOutRole)
        # 更新角色信息矩阵
        if deathCause == 1:  # 1代表被众人投杀
            roleInformationMatrix[weedOutRole, 2] = gameRound * 1
            roleInformationMatrix[weedOutRole, 3] = VOTING
        if deathCause == 2:  # 2代表被猎人枪杀
            roleInformationMatrix[weedOutRole, 2] = gameRound * 1
            roleInformationMatrix[weedOutRole, 3] = GUN
        if deathCause == 3:  # 3代表被狼人暗杀
            roleInformationMatrix[weedOutRole, 2] = gameRound * -1
            roleInformationMatrix[weedOutRole, 3] = WERWOLF
        if deathCause == 4:  # 4代表被女巫毒杀
            roleInformationMatrix[weedOutRole, 2] = gameRound * -1
            roleInformationMatrix[weedOutRole, 3] = POISON

