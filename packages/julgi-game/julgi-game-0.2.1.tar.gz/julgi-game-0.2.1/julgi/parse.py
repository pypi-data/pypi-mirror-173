from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from kopp import kopp

from .__version__ import __version__

if TYPE_CHECKING:
    from .classes import BattleData, BattleMetaData, PostBattleData


def parse_ko(data: dict[str, Any]) -> list[str]:
    result: list[str] = []

    # 1. 메타 데이터
    metadata: BattleMetaData = data["meta_data"]

    result.append(f"줄기 게임! '{metadata.user1.name}' vs '{metadata.user2.name}'")
    result.append(f"버전: {__version__}, 시드: {metadata.seed}")

    result.append("")

    # 유저 정보 출력
    user_info = (
        "[{name}] HP: {max_hp} / 공격력: {attack} / 마력: {magic} /"
        " 속도: {speed} / 능력: {ability} / 명중: {hit} / 극대: {critical}"
    )
    result.append(user_info.format(**asdict(metadata.user1)))
    result.append(user_info.format(**asdict(metadata.user2)))

    result.append("")

    # 2. 전투 데이터

    # 2-1. 스킬 사용
    use_skill = (
        "[{name}](은)는 '{skill}'(을)를 사용! {is_critical}"
        "[{other}]에게 {damage}{mark}의 피해를 입혔다! (남은 HP: {other_hp}/{other_max_hp})"
    )
    use_skill_evade = "[{name}](은)는 '{skill}'(을)를 사용! 그러나 [{other}](은)는 회피했다!"
    use_skill_heal = (
        "[{name}](은)는 '{skill}'(을)를 사용! {is_critical}"
        "[{name}](은)는 {heal}{mark}의 체력을 회복했다! (남은 HP: {user_hp}/{user_max_hp})"
    )

    # 2-2. 일반 공격
    attack = (
        "[{name}]의 공격! {is_critical}"
        "[{other}]에게 {damage}{mark}의 피해를 입혔다! (남은 HP: {other_hp}/{other_max_hp})"
    )
    attack_evade = "[{name}]의 공격! 그러나 [{other}](은)는 회피했다!"

    for bd in data["battle_data"]:
        bd: BattleData
        data_dict = {
            "name": bd.user,
            "other": bd.other,
            "user_hp": bd.user_hp,
            "user_max_hp": bd.user_max_hp,
            "other_hp": bd.other_hp,
            "other_max_hp": bd.other_max_hp,
            "skill": bd.skill.name if bd.skill is not None else None,
            "is_critical": "치명타! " if bd.is_critical else "",
            "mark": "!" if bd.is_critical else "",
            "damage": bd.damage,
            "heal": bd.heal_amount,
        }

        if bd.use_skill:
            if bd.use_heal:
                result.append(use_skill_heal.format(**data_dict))
            elif bd.is_hit:
                result.append(use_skill.format(**data_dict))
            else:
                result.append(use_skill_evade.format(**data_dict))

        else:
            if bd.is_hit:
                result.append(attack.format(**data_dict))
            else:
                result.append(attack_evade.format(**data_dict))

    result.append("")

    # 3. 전투 결과
    pd: PostBattleData = data["post_data"]

    battle_result = "[{name}] 승! ({turn}턴)"
    result.append(battle_result.format(name=pd.winner, turn=pd.turns))

    # '(은)는' 과 같은 종성 처리
    result = list(map(kopp, result))
    return result
