# name

crafter

## Overview

(WIP) FF14のクラフターマクロを試験する

## Requirement

- Python3

## Usage

(WIP)現状はシステムテストのみ

    % python state.py
    作業アクション効率100: 工数263進む, 加工アクション効率100: 品質325上昇
    耐久: 80  残り工数:   800 残り品質:  1200 (消費CP 0)
    --------
    マニピュレーション
    消費CP: 88, 消費耐久:  0 | 作業効率: 0   , 加工効率: 0
    adding_buffs: (<skill.StateBuff object at 0x000001BF4995C340>,)
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    耐久: 80  残り工数:   800 残り品質:  1200 (消費CP 88)
    [8] マニピュレーション 残ターン:8
    --------
    作業
    消費CP:  0, 消費耐久: 10 | 作業効率: 120 , 加工効率: 0
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    DEBUG:skill:<マニピュレーション>
    耐久: 75  残り工数:   485 残り品質:  1200 (消費CP 88)
    [7] マニピュレーション 残ターン:7
    --------
    作業
    消費CP:  0, 消費耐久: 10 | 作業効率: 120 , 加工効率: 0
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    DEBUG:skill:<マニピュレーション>
    耐久: 70  残り工数:   170 残り品質:  1200 (消費CP 88)
    [6] マニピュレーション 残ターン:6
    --------
    最終確認
    消費CP:  1, 消費耐久:  0 | 作業効率: 0   , 加工効率: 0
    adding_buffs: (<skill.StateBuff object at 0x000001BF4995C400>,)
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    DEBUG:skill:<マニピュレーション>
    耐久: 75  残り工数:   170 残り品質:  1200 (消費CP 89)
    [5] マニピュレーション 残ターン:5
    [5] 最終確認 残ターン:5
    --------
    作業
    消費CP:  0, 消費耐久: 10 | 作業効率: 120 , 加工効率: 0
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    DEBUG:skill:<マニピュレーション>
    DEBUG:skill:<最終確認>
    耐久: 70  残り工数:     1 残り品質:  1200 (消費CP 89)
    [4] マニピュレーション 残ターン:4
    [4] 最終確認 残ターン:4
    --------
    作業
    消費CP:  0, 消費耐久: 10 | 作業効率: 120 , 加工効率: 0
    ↓
    DEBUG:__main__:buffs: [0, 0, 100, 100]
    DEBUG:skill:<マニピュレーション>
    DEBUG:skill:<最終確認>
    耐久: 65  残り工数:     1 残り品質:  1200 (消費CP 89)
    [3] マニピュレーション 残ターン:3
    [3] 最終確認 残ターン:3

## Author

Orion78cvz (Okinawa Bunmei)

## Licence

This project is licensed under the terms of the MIT license.
