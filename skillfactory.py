# -*- coding: utf-8 -*-
"""
 クラフタースキル Factory
"""
import logging
import skill

"""
 アクション Factory
"""
#TODO: name周りの設計が適当になっているので整理する

class ActionFactory:
    actions = {"作業": lambda: ActionFactory.create_basic_synthesis(0, 120),
              "模範作業": lambda: ActionFactory.create_basic_synthesis(7, 150),
              "ヴェネレーション": lambda: ActionFactory.create_only_giving_buff("ヴェネレーション", 18),
              "倹約": lambda: ActionFactory.create_only_giving_buff("倹約", 56),
              "長期倹約": lambda: ActionFactory.create_only_giving_buff("長期倹約", 98),
              "最終確認": lambda: ActionFactory.create_only_giving_buff("最終確認", 1),
              "マニピュレーション": lambda: ActionFactory.create_only_giving_buff("マニピュレーション", 88),
              }

    @classmethod
    def create(cls, name):
        cf = ActionFactory.actions.get(name, None)
        return cf()
    
    #---
    @classmethod
    def create_basic_synthesis(cls, cp, eff):
        return skill.ActionSkillInfo("作業", cp, 10, eff, 0)

    @classmethod
    def create_only_giving_buff(cls, name, cp):
        bf = BuffFactory.create(name)
        return skill.ActionSkillInfo(name, cp, 0, 0, 0, adding_buffs = (bf,))


"""
 バフ Factory
"""
class BuffFactory:
    buffnames_action = {"ヴェネレーション": lambda: BuffFactory.create_veneration(),
                        "倹約": lambda: BuffFactory.create_wastenot(4),
                        "長期倹約": lambda: BuffFactory.create_wastenot(8),
                        "最終確認": lambda: skill.StateBuff("最終確認", skill.StateBuff.final_appraisal, 5, None),
                        "マニピュレーション": lambda: skill.StateBuff("マニピュレーション", skill.StateBuff.manipulation, 8, 5),
                        }
    buffnames_state = {}

    @classmethod
    def create(cls, name):
        cf = BuffFactory.buffnames_action.get(name, None) or BuffFactory.buffnames_state.get(name, None)
        return cf()
    
    #---
    @classmethod
    def create_veneration(cls):
        return skill.ActionBuff("ヴェネレーション", 4, progress = 50, stackable = False)

    @classmethod
    def create_wastenot(cls, nsteps):
        return skill.ActionBuff("倹約", nsteps, durability = 50, stackable = False)



#---
def main():
    logging.basicConfig(level = logging.DEBUG)

    for n in ActionFactory.actions.keys():
        ac = ActionFactory.create(n)
        print(ac)

#----
if __name__ == "__main__":
    main()
