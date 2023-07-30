from unit import BaseUnit

class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1.2
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):

        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):

        if self.player.health_points <= 0 and self.enemy.health_points <= 0:
            self.battle_result = 'Ничья'
            return self._end_game()
        elif self.enemy.health_points <= 0:
            self.battle_result = 'Игрок выиграл битву'
            return self._end_game()
        elif self.player.health_points <= 0:
            self.battle_result = 'Игрок проиграл битву'
            return self._end_game()
        return None
    def _stamina_regeneration(self):

        for i in (self.player, self.enemy):
            i.stamina += self.STAMINA_PER_ROUND
            if i.stamina > i.unit_class.max_stamina:
                i.stamina = i.unit_class.max_stamina

    def next_turn(self):

        if self.game_is_running:
            enemy_result = self.enemy.hit(self.player)
            result = self._check_players_hp()
            if result is not None:
                return result
            self._stamina_regeneration()
            return enemy_result

    def _end_game(self):

        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):

        hit_result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f'{hit_result}<hr>{turn_result}'


    def player_use_skill(self):

        skill_result = self.player.use_skill(self.enemy)
        if skill_result == 'Навык использован' or skill_result == 'Недостаточно выносливости':
            return f'{skill_result}'
        turn_result = self.next_turn()
        return f'{skill_result}<hr>{turn_result}'

    def player_skip_turn(self):
        turn_result = self.next_turn()
        return f'{self.player.name} пропускает ход <hr>{turn_result}'
