# dungeon.py
# Esteban, Richard, Utkarsh, Sam
# June 9, 2022
last_id = []

def compare(scene, ID):
    """
    Find a specific scene on the fourth level graph, by recursively scanning all branching paths
    Efficiency : O(n) = 4^n
    :param scene: (Scene) where to start searching
    :param ID: (String) ID of scene to find
    :return: (Scene) or False
    """
    # Last id is a list of every ID we already looked at
    global last_id
    if scene is None:
        # If there is no actual scene, then no searching needs to be done
        return False

    if scene.ID in last_id:
        # If we have already searched this ID, then stop this branch of searching, or we will end in an
        # infinite loop
        return False
    last_id.append(scene.ID)
    if scene.ID == ID:
        # If our scene matches the ID, return it
        return scene
    elif not any(list(scene.linked_rooms.values())):
        # If we stumbled upon a dead end, then stop searching
        return False
    else:
        for room in scene.linked_rooms.values():
            # For every room linked to this one
            # Compare our ID again
            a = compare(room, ID)
            if a:
                return a
        return False


class Dungeon:
    def __init__(self, head=None):
        """
        Graph with four branches, that can loop back to each other, holds the current level the player is playing on.
        Load with data_loader.load_dungeon(), DO NOT USE MANUALLY.
        :param head = None: (Scene) Optional
        """
        self.head = head

    def get(self, ID):
        """
        Find and return a scene within the dungeon by its ID
        TODO: using this to obtain scenes is not advisable
        :param ID: (String)
        :return: (Scene) or False
        """
        global last_id
        last_id = []
        return compare(self.head, ID)
