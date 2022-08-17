# -*- coding: utf-8 -*-
"""
 進行状態を処理する
"""
import logging
import skillfactory

class PlayerPerformance:
    """ プレイヤーの能力値 (効率100あたりの工数、品質進行)"""
    def __init__(self, base_progress, base_quality): #, cp):
        self.progress = base_progress
        self.quality = base_quality
        #self.max_cp = cp #ひとまず使わないので

    def __str__(self):
        return "作業アクション効率100: 工数{0}進む, 加工アクション効率100: 品質{1}上昇".format(self.progress, self.quality)


class CraftingState:
    """ 現在の進行状態 """
    def __init__(self, init_durability, req_progress, req_quality, base_performance):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        self.finished = 0

        self.base_performance = base_performance

        # MEMO: 初期値と現在値分けた方がよいかも
        self.total_cp = 0
        self.durability = init_durability
        self.req_progress = req_progress
        self.req_quality = req_quality

        self.buffs = {} # バフ名称: [BuffBaseのインスタンス, 残りターン数(int), スタック数] #TODO: インスタンス変数にすればよいかも

    def __str__(self):
        lines = []
        lines.append("耐久: {0:<3d} 残り工数: {1:>5d} 残り品質: {2:>5d} (消費CP {3})".format(self.durability, self.req_progress, self.req_quality, self.total_cp))
        for bn, v in self.buffs.items():
            lines.append("[{0}] {1} 残ターン:{2}".format(v[1], bn, v[1]))
        if self.is_finished():
            lines.append("__完成__" if self.is_succeeded() else "__失敗__")
        return "\n".join(lines)

    #---
    def is_finished(self):
        return self.finished != 0
    def is_succeeded(self):
        return self.finished > 0
    def is_failed(self):
        return self.finished < 0
    def is_quality_completed(self):
        return self.req_quality <= 0

    def is_buff_valid(self, buffname):
        """
          指定のバフがかかった状態か判定
        """
        if buffname in self.buffs: return True #TODO: 残りターンはチェックしていない
        return False

    def is_skill_available(self, skill):
        """
          スキルが使用可能かどうかチェック
        """
        for bf in skill.params['required_buffs']:
            if not self.is_buff_valid(bf): return False
        for bf in skill.params['exclusive_buffs']:
            if self.is_buff_valid(bf): return False
        return True

    def calc_action_buffs(self):
        ret = [0, 0, 100, 100] #cp, d, p, q
        for bf in self.buffs.values():
            if bf[0].trigger != 'action': continue
            bf[0].accumulate_effect(ret, self)
        return ret

    def proc_state_buffs(self):
        for bf in self.buffs.values():
            if bf[0].trigger != 'state': continue
            bf[0].do_effect(self)

    def exec_step(self, skill): #TODO: 長いので整理する
        if self.is_finished(): raise RuntimeError("job is already finished")
        # 行程を進める
        ab = self.calc_action_buffs()
        self.logger.debug("buffs: %s", str(ab))
        self.total_cp = max(self.total_cp + skill.use_cp * (100 - ab[0]) // 100, 0)
        self.durability = self.durability - skill.use_durability * (100 - ab[1]) //100
        self.req_progress = self.req_progress - self.base_performance.progress * skill.inc_progress * ab[2] //10000
        self.req_quality = self.req_quality - self.base_performance.quality * skill.inc_quality * ab[3] //10000

        # 失敗判定
        if self.req_progress > 0 and self.durability <= 0: # 失敗
            self.finished = -1
            return #バフの処理は行わずに終了する

        #バフ処理(ターン経過、解除、付与)
        if skill.use_step > 0:
            self.proc_state_buffs()
            
            dl = []
            for bn in self.buffs.keys():
                bf = self.buffs[bn]
                bf[1] = bf[1] - 1 # skill.use_step?
                if bf[1] <= 0: dl.append(bn)
            for d in dl: del self.buffs[d]

        for bn in skill.params['removing_buffs']:
            if bn in self.buffs:
                del self.buffs[bn]
        for bf in skill.params['adding_buffs']:
            if not bf.name in self.buffs or not bf.stackable:
                self.buffs[bf.name] = [bf, bf.nsteps, 1]
            else:
                self.buffs[bf.name][1] = bf.nsteps
                sn = self.buffs[bf.name][2] + 1
                #TODO: スタック上限チェック
                self.buffs[bf.name][2] = sn

        # 完成判定
        if self.req_progress <= 0:
            self.finished = 1
            return

#---
def test(state, timeline):
    print(state)
    for sn in timeline:
        print("--------")
        act = skillfactory.ActionFactory.create(sn)
        print(act)
        print("↓")
        state.exec_step(act)
        print(state)

def sample1():
    player = PlayerPerformance(263, 325)
    state = CraftingState(80, 6000, 1200, player)
    print(player)
    timeline = ["作業", "模範作業", "ヴェネレーション", "模範作業", "作業", "作業", "作業", "作業", "作業"]
    test(state, timeline)
    assert state.is_failed()

def sample2():
    player = PlayerPerformance(263, 325)
    state = CraftingState(80, 6000, 1200, player)
    print(player)
    timeline = ["長期倹約", "作業", "模範作業", "ヴェネレーション", "模範作業", "作業", "作業", "作業", "作業", "作業"]
    test(state, timeline)
    assert not state.is_finished()

def sample3():
    player = PlayerPerformance(263, 325)
    state = CraftingState(80, 800, 1200, player)
    print(player)
    timeline = ["マニピュレーション", "作業", "作業", "最終確認", "作業", "作業"]
    test(state, timeline)
    assert not state.is_finished()
    assert state.durability == 80 - 10 * 4 + 5 * 5


def main():
    logging.basicConfig(level = logging.DEBUG)

    sample3()

#----
if __name__ == "__main__":
    main()
