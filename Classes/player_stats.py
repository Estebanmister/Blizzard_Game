class PlayerStats:
    def __init__(self, hunger=20.0, thirst=20.0, sanity=50.0):
        """
        Creates a PlayerStats object with custom hunger, thirst and sanity.
        Default values are hunger:20, thirst:20, sanity:50

        :param hunger: (float) The player's hunger stat
        :param thirst: (float) The player's thirst stat
        :param sanity: (float) The player's sanity stat
        """

        self.__health = True

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

        :return: A dictionary, with each player stat listed in the form of stat_name:value
        """
        return {"health": self.__health, "hunger": self.__hunger, "thirst": self.__thirst, "sanity": self.__sanity}

    def check_stats_for_zero(self):
        """
        Checks if any of the player's stat (health, hunger, thirst or sanity) falls to or below zero

        :return: True if the any of the stat falls below or equal to zero, False otherwise.
        """
        if self.__sanity <= 0 or self.__thirst <= 0 or self.__hunger <= 0:
            return True
        return False

    def check_alive(self):
        """
        Check if the player is alive
        The function will also call the check_stats_for_zero function,
        which will set the player's health to false if any stat is zero


        :return: True if the player is alive (health = True), False otherwise.
        """
        if self.check_stats_for_zero():
            self.__health = False

        return self.__health