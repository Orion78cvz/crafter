# -*- coding: utf-8 -*-
"""
 クラフタースキル情報

 ここでは枠組みを提供し、実際の具体的なアクションはfactoryの方に記述する
"""
import logging

def normalize_iterable_params(dic, names):
    """
      リストとして処理される項目が単一値or無指定でも問題ないように
      dic中の指定アイテムをiterableに整頓する
    """
    for pn in names:
        obj = dic.get(pn, None)
        if not obj:
            dic[pn] = ()
        elif not hasattr(obj, "__iter__"):
            dic[pn] = (obj,)

#----
"""
 アクションスキル
"""
class ActionSkillInfo:
    """ アクションスキル情報 """
    def __init__(self, name, use_cp, use_durability, inc_progress, inc_quality, *, use_step = 1, **kwargs):
        #self.logger = logging.getLogger(__name__)
        #self.logger.addHandler(logging.NullHandler())
        
        self.name = name # スキル名称
        self.use_step = use_step # 消費ターン
        self.use_cp = use_cp # 消費CP
        self.use_durability = use_durability # 消費耐久
        self.inc_progress = inc_progress # 作業効率
        self.inc_quality = inc_quality # 品質効率
        self.params = kwargs.copy() #その他のパラメータ
        
        normalize_iterable_params(self.params, ('required_buffs', 'exclusive_buffs', 'adding_buffs', 'removing_buffs')) #TODO: 一旦addingだけBuffBaseインスタンスを投入することにしたがこの辺りは整理する

    def __str__(self):
        lines = [self.name, "消費CP:{0:>3d}, 消費耐久:{1:>3d} | 作業効率: {2:<4d}, 加工効率: {3:<4d}".format(self.use_cp, self.use_durability, self.inc_progress, self.inc_quality)]
        for pn, v in self.params.items():
            if v:
                lines.append("{}: {}".format(pn, str(v))) #TODO: buffの文字出力
        return "\n".join(lines)
        

#----
"""
 バフ
"""
class BuffBase:
    """ バフ情報の基底クラス """
    def __init__(self, name, trigger = None, nsteps = 1, *, amount = None, stackable = False):
        """
         [amount] 効果量 #INFO: バフにより扱いが異なる
         [nsteps] (初期)持続ターン数
         [trigger]
           'action': アクションの効果に影響(イノベ等)
           'state': アクション実行後のステートに影響(マニピ等)
           None: アクション発動条件など　効果はないが付与されていること自体に意味がある場合
         [stackable]
           同一名のバフがスタックするかどうか(インナークワイエットなどがTrue) #MEMO: 最大スタック数(int)としても良いか?
           Falseなら付与時に上書きされる想定
        """
        self.name = name
        self.trigger = trigger
        self.nsteps = nsteps
        self.amount = amount
        self.stackable = stackable

class ActionBuff(BuffBase):
    """
     アクションの効率に対するバフ
       [amount]  (CP消費減, 耐久消費減, 作業効率増, 品質効率増) それぞれ百分率、initには個別に名前付き引数で渡す
    """
    def __init__(self, name, nsteps = 1, *, cp = 0, durability = 0, progress = 0, quality = 0, stackable = False):
         super().__init__(name, 'action', nsteps, amount = (cp, durability, progress, quality), stackable = stackable)

    def accumulate_effect(self, total, state):
        """
          バフ効果を蓄積(加算)する
          ビエルゴや下地作業など効果量が変化するものはここの計算に入れる想定
          TODO: totalを変更するか返り値とするかは要検討(ひとまず直接変更する形にした)
        """
        total[0] = max(total[0], self.amount[0])
        total[1] = max(total[1], self.amount[1])
        total[2] = total[2] + self.amount[2]
        total[3] = total[3] + self.amount[3]

class StateBuff(BuffBase):
    """ アクション実行後に状態を操作するバフ """
    def __init__(self, name, effect_func, nsteps = 1, amount = None, stackable = False):
        super().__init__(name, 'state', nsteps, amount = amount, stackable = stackable)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        self.effect_func = effect_func

    def do_effect(self, state):
        self.logger.debug("<%s>", self.name)
        self.effect_func(state, self.amount)

    #---
    @classmethod
    def final_appraisal(cls, state, amount):
        """ 最終確認 """
        if state.req_progress <= 0:
            state.req_progress = 1

    @classmethod
    def manipulation(cls, state, amount):
        """ マニピュレーション """
        state.durability = state.durability + amount

#---
def main():
    print("test")
    

#----
if __name__ == "__main__":
    main()
