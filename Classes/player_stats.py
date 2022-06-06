from random import uniform


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

    def __init__(self,scene_id, hunger=20.0, thirst=20.0, sanity=50.0):
        """
        Creates a PlayerStats object with sceneid, custom hunger, thirst and sanity
        Default values are hunger:20, thirst:20, sanity:50

        :param hunger: (float) The player's hunger stat
        :param thirst: (float) The player's thirst stat
        :param sanity: (float) The player's sanity stat
        """

        self.__health = True
        self.__scene_id = scene_id

        # Default the last_scene_id to scene_id on load
        self.__last_scene_id = scene_id

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

    def get_stats(self):
        """
        Get the player's stats, as a dictionary

        :return: A dictionary, with each player stat listed in the form of stat_name:value, to one decimal place
        """
        return {"health": round(self.__health, 1), "hunger": round(self.__hunger, 1), "thirst": round(self.__thirst, 1),
                "sanity": round(self.__sanity, )}

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
        The function will also call the check_stats_for_zero function,
        which will set the player's health to False if any stat is zero
        (indicating the player is dead)


        :return: True if the player is alive (health = True), False otherwise
        """

        # Set the player's health to False if any stat is zero
        if self.check_stats_for_zero():
            self.__health = False

        return self.__health

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

        :param value: The amount being add to the hunger stat
        """

        self.__hunger += value

    def add_thirst(self, value):
        """
        Adds an amount to the thirst

        :param value: The amount being add to the thirst stat
        """

        self.__thirst += value

    def add_sanity(self, value):
        """
        Adds an amount to the sanity

        :param value: The amount being add to the sanity stat
        """

        self.__sanity += value

    def get_current_scene_id(self):
        """
        :return: The scene the player is currently in
        """
        return self.__scene_id

    def get_last_scene_id(self):
        """
        :return: The scene the player was last in
        """
        return self.__last_scene_id


