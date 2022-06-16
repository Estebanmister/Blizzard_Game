
def compare(scene, ID):
    """
    Find a specific scene on the fourth level linked list, by recursively scanning all branching paths
    :param scene: (Scene) where to start searching
    :param ID: (String) ID of scene to find
    :return: (Scene) or False
    """
    if scene is None:
        return False
    if scene.ID == ID:
        return scene
    elif not any(list(scene.linked_rooms.values())):
        return False
    else:
        for room in scene.linked_rooms.values():
            a = compare(room, ID)
            if a:
                return a
        return False


class Dungeon:
    def __init__(self, head=None):
        """
        Four level branching linked list, holds the current level the player is playing on.
        Load with data_loader.load_dungeon(), DO NOT USE MANUALLY.
        :param head = None: (Scene) Optional
        """
        self.head = head

    def get(self, ID):
        """
        Find and return a scene within the dungeon by its ID
        :param ID: (String)
        :return: (Scene) or False
        """
        return compare(self.head, ID)
