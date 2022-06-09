
def compare(scene, ID):
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
        self.head = head

    def get(self, ID):
        return compare(self.head, ID)
