import sys
import os
from typing import Union

import battlesimulation
from battlesimulation import Context, SpaceFleet, Rocket

clear_command = 'cls' if os.name == 'nt' else 'clear'
previous_results_string = ""
clear_screen_flag = True
c = Context()
c._fleet_1.custom_name = "Fleet 1"
c._fleet_2.custom_name = "Fleet 2"
c._fleet_3.custom_name = "Fleet 3"

def clear_screen() -> None:
    """Clear command line and print previous saved results string."""

    if not battlesimulation._debug_printing:
        if clear_screen_flag:
            os.system(clear_command)
            print(previous_results_string)

#####################
# Strings for print #
#####################

def print_help() -> None:
    """Prints help when --help or -h is passed as argument."""

    text = "This is the module for making calculations for MMO Strategy Game Galaxy Online (https://galaxyonline.io)\n"
    text += f"version is {battlesimulation.__version__}\n\n"
    text += "Run python -m battlesimulation\n to launch module in interactive mode with menu.\n\nOr in your script.py use Context object:\n\n"
    text += "from battlesimulation import Context\n"
    text += "context = Context()\ncontext.help()\n\n"
    print(text)

def help_inside_main_menu() -> str:
    """Returns some explanation string."""

    text = "\n\nThis is the module for making calculations for MMO Strategy Game Galaxy Online (https://galaxyonline.io)\n"
    text += "Project page: https://github.com/fadedness/galaxy-online-battle-simulation\n"
    text += "There is a GUI wrapper for this module: https://github.com/fadedness/Galaxy-Online-Battle-Calculator\n\n"
    text += "You can use this module to analize your possibilities, casualties, costs; you can find possible good counters to incoming attacks on you.\n"
    text += "Use menu to navigate, setup and simulate.\n"
    text += "Anything left unset will be instatiated as default: empty Fleet, empty Planet, etc.\n"
    text += "Fleet 1 is considered always attacking the Fleet 2, which is defending Planet's surface. Fleet 3 is blockading or supporting Planet.\n"
    text += "If Planet is not set, consider it the same as a Space Battle.\n"
    text += "You can change what priorities (attack or defense) Fleets will use for calculations. Defaults are Fleet 1 attacking, 2 and 3 defending.\n\n"
    text += "Order of your actions:\n"
    text += "1. Set Fleets that as you need.\n"
    text += "1.a. That includes Spaceships, Module, priorities, accuracy type.\n"
    text += "2. Set a Planet if you need it:\n"
    text += "2.a. Set rockets on the Planet.\n"
    text += "2.b. Set buildings on the Planet (you can simplify that to just turrets).\n"
    text += "3. Choose Simulation and results will be printed.\n\n"
    return text

def some_short_explanation_string() -> str:
    """Short description of each Fleet's role in Simulation."""

    text = "\nAbout Objects that you're gonna set (but you don't have to set everything there is, only what you need):\n"
    text += "Fleet 1 is always attacking others. It uses attack priorities by default, but you can change that.\n"
    text += "Fleet 3 is the Fleet that is either already blockading the Planet (enemy to Planet) or is a Support Fleet (ally to Planet). "
    text += "But it is always enemy to Fleet 1.\n"
    text += "Fleet 2 is the defending Fleet, stationed on Planet's surface. "
    text += "Or if you don't set Planet - it will be the same as Space Battle with no Planet involved.\n"
    text += "Planet - if you set it, you need to specify planet type and size. "
    text += "Also you can specify sum of all Turrets levels on it, if you want to skip buildings setup.\n"
    text += "There can be Buildings and Rockets on the Planet. You can set'em up too. "
    text += "By the way, Rockets cannot be fired if there is no Turret building on the Planet.\n"
    return text

def main_menu_string() -> str:
    """Main menu string."""

    text = "\n\nChoose an action:\n"
    text += " 1. Setup Fleet 1.\n 2. Setup Fleet 2.\n 3. Setup Fleet 3.\n 4. Setup Planet.\n"
    text += " 5. Simulate Battle in set conditions.\n"
    text += " 6. Find Fleet 1 that will defeat set conditions (If you have set Fleet 1 up - it will be cleared).\n"
    text += " 7. Find amount of Valkyries needed to destroy Planetary defenses (Bombardment).\n\n"
    text += "10. Set Fleet's accuracy to \"range\" -> two Simulations will be made: one with minimum and one with maximum accuracy."
    text += "20. Print short description of each Fleet's role in Simulation.\n"
    text += "21. Print Game Objects.\n"
    text += "22. About.\n"
    text += "23. Toggle some debug prints, also disables clearing screen when debug print is enabled.\n"
    text += "24. Toggle clearing screen\n"
    text += "30. Clear all Game Objects.\n"
    text += "31. Clear previous results string.\n"
    text += " 0. Exit.\n\n"
    return text

def module_and_bonuses_setup_menu_string(fleet_number: int) -> str:
    """Menu for setting up Module and Bonuses."""

    fleet = get_fleet_reference_from_number(fleet_number)

    text = f"\n{fleet.modules.filtered_str_short}\n\nSet Module to (+bonus% on level 100, Attack/Defense/Speed):\n"
    text += " 1. Disintegrator (+25%/0%/0%).\n 2. Afterburner (0%/0%/+50%)\n 3. Shield Booster (0%/+30%/0%).\n"
    text += " 4. Complex Bastion (+20%/+25%/0%).\n 5. Complex Luch (+20%/0%/+50%).\n"
    text += " 6. Complex Halo (0%/+25%/+50%).\n 7. Complex Guardian (+15%/+20%/+40%).\n"
    text += "30. Clear Module.\n"
    text += " 0. Back to Fleet's Menu.\n\n"
    return text

def fleet_setup_menu_string(fleet_number: int) -> str:
    """Menu for setting up Fleet."""

    fleet = get_fleet_reference_from_number(fleet_number)

    priorities_string = "attack" if fleet.attacking else "defense"
    accuracy_type_string = fleet.acc_type
    if fleet_number == 1:
        attack_type = " attack" if fleet.attack_planet else " blockade"
        attack_type = f", Type: {attack_type}."
    else:
        attack_type = "."
    text = f"\nYou don't have to set everything.\n\nCurrent {fleet.custom_name}:\n{fleet.filtered_str}\n{fleet.modules.filtered_str_short}\nPriorities: {priorities_string}{attack_type}\nAccuracy type: {accuracy_type_string}.\n"
    text += " 1. Add Hercules.\n 2. Add Loki.\n 3. Add Raptor.\n 4. Add Hornet.\n 5. Add Javelin.\n"
    text += " 6. Add Excalibur.\n 7. Add Valkyrie.\n 8. Add Titan.\n 9. Add Abaddon.\n"
    text += "10. Set Module.\n"
    text += "11. Toggle Priorities to use.\n"
    text += "12. Set accuracy type.\n"
    if fleet.custom_name == "Fleet 1":
        text += "13. Toggle type of attack Fleet 1 does (attacking or making a blockade).\n"
    text += "30. Clear all Spaceships in Fleet.\n"
    text += "0. Back to Main Menu.\n\n"
    return text

def planet_setup_menu_string() -> str:
    """Menu for setting up Planet."""

    text = f"\n{c._planet.filtered_str_full}\n"
    text += " 1. Set Planet type.\n 2. Set Planet size.\n 3. Set sum of all Turrets levels.\n"
    text += " 4. Set Buildings on the Planet.\n"
    text += " 5. Set Rockets on the Planet.\n"
    text += "30. Clear whole Planet.\n"
    text += " 0. Back to Main Menu.\n\n"
    return text

def buildings_setup_menu_string() -> str:
    """Menu for setting up Buildings."""

    text = "There are some restrictions to setting buildings:\nMax level is 30, Max space for Buildings is 25. "
    text += "If you try to add close to 25 buildings, then Command Center or free place for it is a must, as well as at least 3 Mines or 3 free places for Mines.\n"
    text += "Some buildings are limited to certain number of instances."
    text += f"\n{c._planet.buildings.filtered_pretty_str}\n\n"
    text += " 1. Add Command Center - max 1.\n"
    text += " 2. Add Mine - max 5.\n"
    text += " 3. Add Warehouse - max 21.\n"
    text += " 4. Add Trade Office - max 1.\n"
    text += " 5. Add Сosmodrome - max 9.\n"
    text += " 6. Add Spacecraft Plant - max 5.\n"
    text += " 7. Add Power Plant - max 1.\n"
    text += " 8. Add Detection Station - max 1.\n"
    text += " 9. Add Missile Turret - max 20.\n"
    text += "10. Add Shield Generator - max 1.\n"
    text += "30. Clear all buildings.\n"
    text += " 0. Back to Planet Menu.\n\n"
    return text

def rockets_setup_menu_string() -> str:
    """Menu for setting up Rockets."""

    sticks = Rocket(1)
    cobra = Rocket(2)
    aurora = Rocket(3)
    x_ray = Rocket(4)
    text = f"\n{c._planet.rockets.filtered_str}\n"
    text += f" 1. Add Sticks-XL: {sticks.filtered_basic_str}\n"
    text += f" 2. Add Cobra: {cobra.filtered_basic_str}\n"
    text += f" 3. Add Aurora: {aurora.filtered_basic_str}\n"
    text += f" 4. Add X-Ray: {x_ray.filtered_basic_str}\n"
    text += "30. Clear all rockets.\n"
    text += " 0. Back to Planet Menu.\n\n"
    return text

#####################
# Helper functions  #
#####################

def get_fleet_reference_from_number(fleet_number: int) -> SpaceFleet:
    """Returns SpaceFleet reference for specified fleet number."""

    if fleet_number == 1:
        fleet = c._fleet_1
    elif fleet_number == 2:
        fleet = c._fleet_2
    else:
        fleet = c._fleet_3
    return fleet

def get_context_fleet_acc_reference_from_number(fleet_number: int):
    """Returns function reference to set acc_type for specified fleet number."""

    if fleet_number == 1:
        fleet_set_acc = c.set_fleet_1_acc_type
    elif fleet_number == 2:
        fleet_set_acc = c.set_fleet_2_acc_type
    else:
        fleet_set_acc = c.set_fleet_3_acc_type
    return fleet_set_acc

def clear_fleet(fleet_number: int) -> None:
    """Clears specified Fleet of all Spaceships."""

    fleet = get_fleet_reference_from_number(fleet_number)
    fleet.set_fleet([])

def clear_all() -> None:
    """Clear all Game Objects."""

    c.clear_fleet_1()
    c.clear_fleet_2()
    c.clear_fleet_3()
    c.reset_all_buildings()
    c.reset_rockets_to_zero()
    c.set_planet(1,0)

def clear_planet() -> None:
    """Clear Planet."""

    c.reset_all_buildings()
    c.reset_rockets_to_zero()
    c.set_planet(1,0)

def add_rocket(id: int, quantity: int) -> None:
    """Add specified Rocket to Planet."""

    if id == 0:
        c._planet.rockets.set_whole_array([])
    else:
        c._planet.rockets.set_item_of_array((id, quantity))

def add_building(id: int, level: int) -> bool:
    """Add specified Rocket to Planet."""

    if id == 0:
        c._planet.buildings._reinit()
        return True
    else:
        return c._planet.buildings.set_item_of_array((id, level))

def add_module(fleet_number: int, id: int, level: int) -> None:
    """Add specified Module to specified Fleet."""

    fleet = get_fleet_reference_from_number(fleet_number)
    if id == 0:
        fleet.set_module_params(0,0,0)
    else:
        fleet.modules.set_module_by_id(id, level)

def add_spaceship(fleet_number: int, id: int, quantity: int) -> None:
    """Adds specified Spaceship to specified Fleet."""

    fleet = get_fleet_reference_from_number(fleet_number)
    fleet.set_item_of_array((id, quantity))

def set_accuracy_type(fleet_number: int, acc_input: str) -> bool:
    """Set specified accuracy to specified Fleet."""

    fleet_set_acc = get_context_fleet_acc_reference_from_number(fleet_number)
    if acc_input == "1":
        fleet_set_acc("min")
    elif acc_input == "2":
        fleet_set_acc("max")
    elif acc_input == "3":
        fleet_set_acc("random")
    elif acc_input == "4":
        fleet_set_acc("range_min")
    elif acc_input == "5":
        fleet_set_acc("range_max")
    else:
        return False
    return True

def toggle_priorities_and_return_string(fleet_number: int) -> str:
    """Toggles specified Fleet's priorities and returns string for print."""

    fleet = get_fleet_reference_from_number(fleet_number)
    fleet.attacking = not fleet.attacking
    return "attack" if fleet.attacking else "defense"

#####################
# While loop menus  #
#####################

def manage_setup_of_rockets() -> None:
    """While loop for setting up Rockets."""

    input_text = "Enter: "
    while True:
        clear_screen()
        print(rockets_setup_menu_string())
        user_input = input(input_text)
        if user_input == "0":
            break
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                c.reset_rockets_to_zero()
                input_text = "Rockets werre cleared.\n\nEnter: "
        elif user_input in ("1","2","3","4"):
            quantity_input = input("\nEnter quantity of Rockets: ")
            if quantity_input.isdecimal and 0 <= int(quantity_input):
                add_rocket(int(user_input), int(quantity_input))
                result = True
            else:
                result = False
            input_text = "Rocket was%sadded.\n\nEnter: " % (" " if result else " not ")

def manage_setup_of_buildings() -> None:
    """While loop for setting up Buildings."""

    input_text = "Enter: "
    while True:
        clear_screen()
        print(buildings_setup_menu_string())
        user_input = input(input_text)
        if user_input == "0":
            break
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                c.reset_all_buildings()
                input_text = "Buildings werre cleared.\n\nEnter: "
        elif user_input in ("1","2","3","4","5","6","7","8","9","10"):
            level_input = input("\nEnter level of building from 0 to 30. Press Enter for default level 30.\n\nEnter: ")
            if level_input.isdecimal or level_input == "":
                if level_input == "":
                    level_input = 30
                level_input = int(level_input)
                if level_input < 0 or level_input > 30:
                    level_input = 30
                result = add_building(int(user_input), level_input)
            else:
                result = False
            input_text = "Building was%sadded.\n\nEnter: " % (" " if result else " not ")

def manage_setup_of_planet() -> None:
    """While loop for setting up Planet."""

    input_text = "Enter: "
    while True:
        clear_screen()
        print(planet_setup_menu_string())
        user_input = input(input_text)
        if user_input == "0":
            break
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                clear_planet()
                input_text = "Planet was cleared.\n\nEnter: "
        elif user_input == "5":
            manage_setup_of_rockets()
        elif user_input == "4":
            manage_setup_of_buildings()
        elif user_input == "3":
            string = "\nAttention! If you set Turrets level here, "
            string += "Turrets in buildings will be ignored. "
            string += "Enter integer amount or empty string to disable.\n\nEnter: "
            turrets_level = input(string)
            if turrets_level == "":
                c._planet.set_simple_turrets_lvl(False)
                input_text = "Disabled.\n\nEnter: "
            elif turrets_level.isdecimal() and int(turrets_level) >= 0:
                c._planet.set_simple_turrets_lvl(int(turrets_level))
                input_text = "Turrets level was set.\n\nEnter: "
            else:
                input_text = "Invalid input.\n\nMenu, enter: "
        elif user_input == "2":
            string = "Enter amount of Mines (size) of the Planet: 3, 4 or 5. Enter: "
            mines_input = input(string)
            if mines_input in ("3","4","5"):
                c._planet.planet_size = int(mines_input) - 3
                input_text = "Size was set.\n\nEnter: "
        elif user_input == "1":
            string = "\nEnter Planet type: 1 - Torium, 2 - Wanadium, 3 - Ottarium. "
            string += "4 - Chromium, 5 - Kladium, 6 - Neodium, "
            string += "7 - Minterium.\n\nEnter: "
            type_input = input(string)
            if type_input in ("1","2","3","4","5","6","7"):
                c._planet.planet_type = int(type_input)
                input_text = "Type was set.\n\nEnter: "

def manage_setup_of_module(fleet_number: int) -> None:
    """While loop for setting up Module and Bonuses."""

    input_text = "Enter: "
    while True:
        clear_screen()
        print(module_and_bonuses_setup_menu_string(fleet_number))
        user_input = input(input_text)
        input_text = "Enter: "
        if user_input == "0":
            break
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                add_module(fleet_number,0,0)
                input_text = "Module was cleared.\n\nEnter: "
        elif user_input in ("1","2","3","4","5","6","7"):
            level_input = input("\nEnter level of Module (from 0 to 100; press Enter for default level 100).\n\nEnter: ")
            if level_input.isdecimal() or level_input == "":
                if level_input == "":
                    level_input = 100
                add_module(fleet_number, int(user_input), int(level_input))
                input_text = "Module set.\n\nEnter: "
            else:
                input_text = "Not an integer.\n\nMenu, enter: "

def manage_setup_of_fleet(fleet_number: int) -> None:
    """While loop for setting up Fleet."""

    input_text = "Enter: "
    while True:
        clear_screen()
        print(fleet_setup_menu_string(fleet_number))
        user_input = input(input_text)
        input_text = "Enter: "
        if user_input == "0":
            break
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                clear_fleet(fleet_number)
                input_text = f"Fleet {fleet_number} was cleared.\n\nEnter: "
        elif user_input == "13" and fleet_number == 1:
            c._fleet_1.attack_planet = not c._fleet_1.attack_planet
            input_text = "Fleet is %s.\n\nEnter: " % ("attacking" if c._fleet_1.attack_planet else "making a blockade")
        elif user_input == "12":
            acc_input = input("\n\n1 - Min, 2 - Max, 3 - Random, 4 - \"Range Min\", 5 - \"Range Max\".\n\nEnter: ")
            result = set_accuracy_type(fleet_number, acc_input)
            input_text = "Accuracy was%sset.\n\nEnter: " % (" " if result else " not ")
        elif user_input == "11":
            priorities_string = toggle_priorities_and_return_string(fleet_number)
            input_text = f"Fleet's priorities are for {priorities_string}.\n\nEnter: "
        elif user_input == "10":
            manage_setup_of_module(fleet_number)
        elif user_input in ("1","2","3","4","5","6","7","8","9"):
            quantity_input = input("\nEnter quantity of Spaceships (must be int): ")
            if quantity_input.isdecimal():
                add_spaceship(fleet_number, int(user_input), int(quantity_input))
                input_text = "Spaceships added.\n\nEnter: "
            else:
                input_text = "Not an integer.\n\nMenu, enter: "

def manage_main_menu() -> None:
    """While loop for main menu."""

    global previous_results_string
    global clear_screen_flag
    input_text = "Enter: "
    while True:
        clear_screen()
        print(main_menu_string())
        user_input = input(input_text)
        input_text = "Enter: "
        if user_input == "0":
            print("Goodbye!")
            break
        elif user_input == "31":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                previous_results_string = ""
                input_text = "Previous results were cleared.\n\nEnter: "
        elif user_input == "30":
            confirm_input = input("Are you sure? y/n: ")
            if confirm_input.lower() == "y":
                clear_all()
                input_text = "All Game Objects were cleared.\n\nEnter: "
        elif user_input == "24":
            clear_screen_flag = not clear_screen_flag
            input_text = "Clearing screen is %s.\n\nEnter: " % ("enabled" if clear_screen_flag else "disabled")
        elif user_input == "23":
            battlesimulation._debug_printing = not battlesimulation._debug_printing
            input_text = "Additional info printing is %s.\n\nEnter: " % ("enabled" if battlesimulation._debug_printing else "disabled")
        elif user_input == "22":
            print(help_inside_main_menu())
            input("Press enter to continue.")
        elif user_input == "21":
            c.help_game_parameters()
            input("Press enter to continue.")
        elif user_input == "20":
            print(some_short_explanation_string())
            input("Press enter to continue.")
        elif user_input == "10":
            c.set_fleet_1_acc_type("range_max")
            c.set_fleet_2_acc_type("range_max")
            c.set_fleet_3_acc_type("range_max")
            input_text = "Ready for two Simulations.\n\nEnter: "
        elif user_input == "7":
            text = ""
            text += "\n\n#####################################################################################\n\n"
            text += c.old_simulate_bombardment()
            text += "\n\n#####################################################################################\n\n"
            previous_results_string += text
        elif user_input == "6":
            if c._fleet_1.is_populated:
                c.clear_fleet_1()
            c.simulate()
            text = ""
            text += "\n\n#####################################################################################\n\n"
            text += "Against targets:\n"
            if c._fleet_2.was_populated:
                text += f"{c._fleet_2.filtered_original_str}\n"
            if c._fleet_3.was_populated:
                text += f"{c._fleet_3.filtered_original_str}\n"
            text += f"{c._planet.filtered_str_full_original}\n"
            text += c._text_for_finding_suitable_fleets
            text += "\n\n#####################################################################################\n\n"
            previous_results_string += text
            c.set_fleet_1_acc_type("min")
            c.set_fleet_2_acc_type("min")
            c.set_fleet_3_acc_type("min")
        elif user_input == "5":
            c.simulate()
            if c._flag_to_make_context_branch:
                previous_results_string += c._print_combined_results()
                previous_results_string += c._print_pretty_ranges_text()
            else:
                previous_results_string += c._print_simulate_start()
                previous_results_string += c._print_simulate_end()
        elif user_input == "4":
            manage_setup_of_planet()
        elif user_input in ("1", "2", "3"):
            manage_setup_of_fleet(int(user_input))

def main() -> None:
    """Main entry point."""

    manage_main_menu()

if __name__ == "__main__":
    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        print_help()
        sys.exit(0)
    main()
