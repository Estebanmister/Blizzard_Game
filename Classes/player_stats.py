# player_stats.py
# Esteban, Richard, Utkarsh, Sam
# June 13, 2022
from random import uniform
import csv

# PlayerStats object should be saved in player_stats variable to be accessed by other classes



class PlayerStats:

    @staticmethod
    def check_range(min_value, max_value):
        """
        If min_value is higher than max_value, the two will be switched,
        Negative input will default both to 0.1.
        :param min_value: (float) The minimum value
        :param max_value: (float) The maximum value
        :return: The checked min and max value
        """

        # Any value less than 0 will default both to 0.1
        if min_value < 0 or max_value < 0:
            min_value, max_value = 0.1, 0.1

        # if min>max, switch two around
        elif min_value > max_value:
            min_value, max_value = max_value, min_value

        return min_value, max_value

    def __init__(self, new_game=True, hunger=20.0, thirst=20.0, sanity=50.0, scene_id=None):
        """
        IMPORTANT: when creating this object, create it by passing the stat into Player
        Creates a PlayerStats object with scene_id, custom hunger, thirst and sanity
        Default values are hunger:20, thirst:20, sanity:50

        Let's run the game the hardcore way. The player gets sent directly back to the beginning on death (shouldn't be too hard).
        Remember to save the player stats on game exit. It will automatically load them on game start.
        scene_id does not need to be set now. Just call the update_scene_id() function whenever needed.
        :param new_game: (bool) True if starting a new game, False if continuing the previous game (load from file)
        :param scene_id: (string) the scene player is in on creation of the PlayerStats object. Does not need to be set right away
        :param hunger: (float) The player's hunger stat
        :param thirst: (float) The player's thirst stat
        :param sanity: (float) The player's sanity stat
        """

        # If starting a new game, initialize variables
        if new_game:
            self.__health = True
            self.__scene_id = scene_id

            # Default the first_scene_id to scene_id on load
            self.__first_scene_id = scene_id

            # Set to default value if input is invalid (less than or equal to 0)
            if hunger <= 0:
                self.__hunger = 20.0
            else:
                self.__hunger = hunger

            if thirst <= 0:
                self.__thirst = 20.0
            else:
                self.__thirst = thirst

            if sanity <= 0:
                self.__sanity = 50.0
            else:
                self.__sanity = sanity

            # We will need to save the player's initial stats in a file for later uses
            self.save_to_file("Player/initial_stats.csv")

        # Else, load from file
        else:
            self.read_file("Player/stats.csv")

        # Either case, we need to load the initial stats as a dict
        with open("Player/initial_stats.csv", 'r') as stats_dict:
            reader = csv.DictReader(stats_dict)
            self.stats_dict = next(reader)

    def save_to_file(self, filename="Player/stats.csv"):
        """
        Saves player stats to file
        :param filename: The file to save the stats to
        """

        # Set the header, save the values accordingly
        fields = ["health", "scene_id", "first_scene_id", "hunger", "thirst", "sanity"]
        stats = {"health": self.__health,
                 "scene_id": self.__scene_id,
                 "first_scene_id": self.__first_scene_id,
                 "hunger": round(self.__hunger, 3),
                 "thirst": round(self.__thirst, 3),
                 "sanity": round(self.__sanity, 3)}
        with open(filename, "w") as csvfile:
            write = csv.DictWriter(csvfile, fieldnames=fields)
            write.writeheader()
            write.writerow(stats)

    def read_file(self, filename):
        """
        Read player stats from csv file, set each variable in PlayerStats class accordingly
        :param filename: The file to load the stats from
        """

        # Open csv file, read in each value and assign it to the variable
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.__health = line["health"]
                self.__scene_id = line["scene_id"]
                self.__first_scene_id = line["first_scene_id"]
                self.__hunger = float(line["hunger"])
                self.__thirst = float(line["thirst"])
                self.__sanity = float(line["sanity"])

    def get_stats(self):
        """
        Get the player's stats, as a dictionary
        :return: A dictionary, with each player stat (health, scene_id, first_scene_id, hunger, thirst, sanity)
         listed in the form of stat_name:value, numerical values rounded to one decimal place
        """
        return {"health": self.__health,
                "scene_id": self.__scene_id,
                "first_scene_id": self.__first_scene_id,
                "hunger": round(self.__hunger, 1),
                "thirst": round(self.__thirst, 1),
                "sanity": round(self.__sanity, 1)}

    def check_stats_for_zero(self):
        """
        Checks if any of the player's stat (health, hunger, thirst or sanity) falls to or below zero
        :return: True if the any of the stat falls below or equal to zero, False otherwise
        """
        if self.__sanity <= 0 or self.__thirst <= 0 or self.__hunger <= 0:
            return True
        return False

    def check_alive(self):
        """
        Check if the player is alive
        The function will call the check_stats_for_zero function,
        which will set the player's health to False if any stat is zero
        (indicating the player is dead)
        If the player is dead (health = False), the player will be returned to the first scene
        by setting scene_id to first_scene_id. Since the game currently does not support recursive searching for a specific scene,
        the function will respawn the player and return False on call, if the player is dead.
        :return: The function will return False if player dies and respawn (although their health is set back to True).
        Otherwise it will return True (if the player is alive).
        """

        # Set the player's health to False if any stat is zero
        if self.check_stats_for_zero():
            self.__health = False

        # If player's health is False, return to first scene, change health to True
        if not self.__health:
            if self.__first_scene_id is not None:
                # Only send the player back to the first scene if the first scene is set
                self.__scene_id = self.__first_scene_id

            # Set health back to True
            self.__health = True

            # Load initial stat back in
            self.read_file("Player/initial_stats.csv")

            return False

        # Returns the player's health status (Always True)
        return self.__health

    def set_alive(self, alive):
        """
        Set the player's health status
        :param alive: (bool) True if player is alive, False if not.
        """

        self.__health = alive

    def reduce_hunger(self, min_value, max_value):
        """
        Reduce the player's hunger by random value within the min_value and max_value range,
        Set both equal to each other to reduce the hunger by a set value.
        If min_value is higher than max_value, the two will be switched,
        Negative input will default both to 0.1.
        :param min_value: (float) the minimum value to reduce hunger by
        :param max_value: (float) the maximum value to reduce hunger by
        """

        # Check the input
        min_value, max_value = self.check_range(min_value, max_value)

        # Subtract a random float (to 3 decimal point) between the min_value and max_value range from hunger
        self.__hunger -= round(uniform(min_value, max_value), 3)

    def reduce_thirst(self, min_value, max_value):
        """
        Reduce the player's thirst by random value within the min_value and max_value range,
        Set both equal to each other to reduce the thirst by a set value.
        If min_value is higher than max_value, the two will be switched,
        Negative input will default both to 0.1.
        :param min_value: (float) the minimum value to reduce thirst by
        :param max_value: (float) the maximum value to reduce thirst by
        """

        # Check the input
        min_value, max_value = self.check_range(min_value, max_value)

        # Subtract a random float (to 3 decimal point) between the min_value and max_value range from hunger
        self.__thirst -= round(uniform(min_value, max_value), 3)

    def reduce_sanity(self, min_value, max_value):
        """
        Reduce the player's sanity by random value within the min_value and max_value range,
        Set both equal to each other to reduce the sanity by a set value.
        If min_value is higher than max_value, the two will be switched,
        Negative input will default both to 0.1.
        :param min_value: (float) the minimum value to reduce sanity by
        :param max_value: (float) the maximum value to reduce sanity by
        """

        # Check the input
        min_value, max_value = self.check_range(min_value, max_value)

        # Subtract a random float (to 3 decimal point) between the min_value and max_value range from hunger
        self.__sanity -= round(uniform(min_value, max_value), 3)

    def add_hunger(self, value):
        """
        Adds an amount to the hunger
        value will not exceed default
        :param value: The amount being add to the hunger stat
        """
        max_hunger = float(self.stats_dict["hunger"])

        # if exceeds max, set to max, else add
        if self.__hunger + value > max_hunger:
            self.__hunger = max_hunger
        else:
            self.__hunger += value

    def add_thirst(self, value):
        """
        Adds an amount to the thirst
        value will not exceed default
        :param value: The amount being add to the thirst stat
        """
        max_thirst = float(self.stats_dict["thirst"])

        # if exceeds max, set to max, else add
        if self.__thirst + value > max_thirst:
            self.__thirst = max_thirst
        else:
            self.__thirst += value

    def add_sanity(self, value):
        """
        Adds an amount to the sanity
        value will not exceed default
        :param value: The amount being add to the sanity stat
        """

        max_sanity = float(self.stats_dict["sanity"])

        # if exceeds max, set to max, else add
        if self.__sanity + value > max_sanity:
            self.__sanity = max_sanity
        else:
            self.__sanity += value

    def get_current_scene_id(self):
        """
        :return: The scene the player is currently in
        """
        return self.__scene_id

    def get_first_scene_id(self):
        """
        :return: The scene the player was first in
        """
        return self.__first_scene_id

    def update_scene_id(self, ID):
        """
        Updates the scene_id with the new scene the player moves to
        If first_scene_id is None (haven't been set yet), it will be set to the current scene_id
        :param ID: The scene the player moves to.
        """

        self.__scene_id = ID

        # When updating scene_id, if first_scene_id is None, we assume that it is the first scene
        # Thus that will also be updated to match the current scene

        if self.__first_scene_id is None:
            self.__first_scene_id = self.__scene_id

# Test code
test = PlayerStats(True, 10, 10, 10)
test.set_alive(False)
print(test.check_alive())