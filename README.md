 1、 Logical matrix establishment
 In the logical thinking of players, it usually includes their own clear attitude towards others and vague and predictive conjecture about the attitude between other players. Therefore, if you want to establish a reliable logical matrix, you can establish a high-dimensional 12 × 12 × 12 logical matrix logic (x, y, z) for each AI.
 Where, x represents the serial number of the matrix, y represents the serial number of the player, and z represents the serial number of the player being viewed. For example, logic (1, 2, 4) represents the opinion of the player with No. 1 on the player with No. 2 on the player with No. 4 [ four ] 
 At the same time, the identity cognition value of players with different identities is assigned. 2 is the identity cognition value of the villagers. If it is lower than 2, it is considered that they prefer the werewolf side. If it is higher than 2, it is considered that they prefer the priest player or expert player.
 1) The logical matrix of werewolf
 Since the werewolf knows the serial numbers of others on the werewolf side, after confirming his serial number i and the serial numbers of other teammates, he sets logic (i, i, werewolf) to 1 and the rest to 2.
 2) Villagers&#39; logic matrix
 Villagers could not know other information at first, so after confirming their serial number villager, they set logic (village,:,:) to 2
 3) The Logic Matrix of the Prophet
 The prophet only knows his/her identity, so after confirming his/her serial number, he/she can set logic (prophet, prophet, prophet) to 3.
 2、 A Mathematical Model for Obtaining Identity Decision Results from Logic Matrix
 As a complex language game, Werewolves Killing, in order to make the game AI choose more suitable players when voting for other players, it seems lack of thinking to take the maximum or minimum value in its corresponding line unilaterally, without taking into account the views of other players, which is also the reason why the logic matrix size is set to 12 × 12 × 12 above.
 After comparing various mathematical models, the author found that the entropy method was used to obtain the identification results, which was based on his own judgment and weighed the judgment of other players, so he chose it as a choice.
 Entropy method can be regarded as a method to evaluate the information density and measure the degree of dispersion.
 On this voting issue, it can put the undisputed candidates in AI&#39;s opinion at a higher priority. If they are good people and have a low identity recognition value, even if there is a candidate whose identity recognition value is low to the same level, they will still give priority to cast.
首先确定要进行身份判定的玩家序号(k)对应的逻辑矩阵logic(k,:, :), 然后计算每个玩家的看法在h玩家处的比重，即对应列logic(k,:,h)中的每一个数占该列总合的比重。设interim=logic(k,:, :)，
 Now take the inter m matrix as an example, where j represents row, h represents column, and represents the element of the j row and h column in the inter m matrix, that is, the view of player j on player h:
 Then calculate the entropy value of all columns and their difference coefficient d_h.
 Calculate the controversy weight w_h of player h in the eyes of player k.
〖w_h  =1-d〗 _（h）/∑ _(i=1)^12▒d_i 	(3.4)
 Finally, according to different situations, the scores will be sorted in ascending or descending order to get the identity determination results of the AI corresponding to player number k. For example, when it is used for good AI to select voting objects, the scores will be sorted in ascending order.
 The file corresponds to the ThinkSpeak function. If you are interested, you can use it according to the target.
 3、 Elimination logic
 AI cannot speak like human beings, so the format of speech is limited. In the above description of the game process, the player or AI can identify themselves when speaking. Otherwise, it will be the villagers by default. At present, jumping wolves is not supported. At most four players who think they are werewolves will be appointed,
 And the probability that a player is a wolf is given from the three suspicions of 0.3 (slightly suspicious), 0.7 (moderately suspicious) and 1 (highly suspicious) [ eight ] 
 At present, the speech format is set as that civilians jump from the crowd in most cases, and only when no one jumps from the prophet will there be a very low probability of jumping from the prophet to block the real prophet.
 Werewolves are more likely to jump when there is no werewolf team mate jumping the prophet, and only one of the werewolf teams will jump the prophet. A prophet may lead a prophet when no one is jumping, but has a small probability of dormancy when someone is already jumping.
 It should be noted that in this article&#39;s werewolf killing speech rules, players who jump the prophet can choose to give verification information, that is, number i is a wolf or number i is a good person.
 The self identified results will be stored in a 12 bit list identityList with zero initial values
 The verification information given by the player who thinks he is a prophet will be stored in the 5 × 12 × 2 identifyMatrix with the initial value of - 1, where the number of pages represents the game round and the number of lines represents the serial number of the person who jumped the prophet
 The first category represents the serial number of the player tested in the last round given by the player who jumped the prophet. The second column represents the identity of the player tested, with 2 villagers and 1 werewolf.
