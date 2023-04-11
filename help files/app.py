from flask import Flask, render_template, request, redirect, url_for
from base import Arena
from unit import PlayerUnit, EnemyUnit
from classes import unit_classes
from equipment import equipment

app = Flask(__name__)

heroes = {}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template("fight.html", heroes=heroes)

@app.route("/fight/hit")
def hit():

    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():

    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)



@app.route("/fight/pass-turn")
def pass_turn():

    if arena.game_is_running:
        result = arena.player_skip_turn()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)



@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():

    if request.method == 'GET':
        result = {
            "header": 'Выберите своего персонажа',  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    elif request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']
        heroes['player'] = PlayerUnit(name, unit_classes[unit_class], weapon, armor)
        return redirect(url_for("choose_enemy"), code=302)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():

    if request.method == 'GET':
        result = {
            "header": 'выберите персонажа противника',  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    elif request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon = request.form['weapon']
        armor = request.form['armor']
        heroes['enemy'] = EnemyUnit(name, unit_classes[unit_class], weapon, armor)
        return redirect(url_for("start_fight"), code=302)


if __name__ == "__main__":
    app.run()
