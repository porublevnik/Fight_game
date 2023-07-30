from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional
from constants import *
from equipment import equipment

class BaseUnit(ABC):

    def __init__(self, name: str, unit_class: UnitClass, weapon: str, armor: str):

        self.name = name
        self.unit_class = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon = equipment.get_weapon(weapon_name=weapon)
        self.armor: Armor = equipment.get_armor(armor_name=armor)
        self._is_skill_used: bool = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> float:

        self.stamina -= self.weapon.stamina_per_hit
        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina -= target.armor.stamina_per_turn
            damage_reduction = target.armor.defence * target.unit_class.armor
        else:
            damage_reduction = 0
        damage = self.weapon.get_total_damage() * self.unit_class.attack - damage_reduction
        damage = 0 if damage < 0 else damage

        return round(damage, 1)

    def get_damage(self, damage: float) -> Optional[float]:
        damage = round(damage, 1)
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:

        pass

    def use_skill(self, target: BaseUnit) -> str:

        if self._is_skill_used:
            return 'Навык использован'
        elif self.stamina < self.unit_class.skill.stamina:
            return 'Недостаточно выносливости'
        else:
            result = self.unit_class.skill.use(user=self, target=target)
            self._is_skill_used = True
        return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        # TODO результат функции должен возвращать следующие строки:
        damage = self._count_damage(target)
        if damage > 0:
            target.get_damage(damage)
            return (f"{self.name} используя {self.weapon.name} пробивает "
                    f"{target.armor.name} соперника и наносит {damage} урона.")
        else:
            return (f"{self.name} используя {self.weapon.name} наносит удар, "
                    f"но {target.armor.name} cоперника его останавливает.")



class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:

        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(1, 100) <= CHANCE_TO_USE_SKILL:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        else:
            if self.stamina < self.weapon.stamina_per_hit:
                return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

            damage = self._count_damage(target)
            target.get_damage(damage)

            if damage > 0:
                return (f"{self.name} используя {self.weapon.name} пробивает "
                        f"{target.armor.name} и наносит Вам {damage} урона.")
            else:
                return (f"{self.name} используя {self.weapon.name} наносит удар, "
                        f"но Ваш(а) {target.armor.name} его останавливает.")



