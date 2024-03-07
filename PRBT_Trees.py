from rich.tree import Tree
from rich.console import Console
from rich.style import Style
from rich import print as rprint
from pynput.keyboard import Key, Listener, Controller

class PRBT_Tree:
    def __init__(self, console: Console, map: dict[str, dict]) -> None:
        self.console = console
        self.tree = build_tree(map=map)
    
    def render(self) -> None:
        self.console.print(self.tree)

class PRBT_iTree(PRBT_Tree):
    def __init__(self, console: Console, map: dict[str, dict]) -> None:
        super().__init__(console, map)
        self.cursor = (0,)
        self.shift_pressed = False
        self.red = Style(color="red", bold=True)
        self.white = Style(color="white", bold=False)
    
    def render(self) -> None:
        self._highlight_location_else_no_style(self.cursor)
        self.console.clear()
        self.console.print(self.tree)
        self._highlight_location_else_no_style((-1,))
    
    def _highlight_location_else_no_style(self, location: tuple[int, ...]):
        def r_highlight_location_else_no_style(tree: Tree, index: int, location: tuple[int, ...], *old_indexes: tuple[int, ...]):
            if (*old_indexes, index) == location:
                tree.style = self.red
            else:
                tree.style = self.white
            for i, child in enumerate(tree.children):
                r_highlight_location_else_no_style(child, i, location, *old_indexes, index)
        
        r_highlight_location_else_no_style(self.tree, 0,location)
    
    def _get_node_at_location(self, location: tuple[int, ...]) -> (Tree | None):
        def r_get_node_at_location(tree: Tree, index: int, location: tuple[int, ...], *old_indexes: tuple[int, ...]) -> (Tree | None):
            if (*old_indexes, index) == location:
                return tree
            for i, child in enumerate(tree.children):
                if result:=r_get_node_at_location(child, i, location, *old_indexes, index):
                    return result
        
        return r_get_node_at_location(self.tree, 0, location)

    def up(self) -> None:
        if len(self.cursor) > 1:
            self.cursor = self.cursor[:-1]
    
    def deeper(self) -> None:
        potential_location = (*self.cursor, 0)
        if self._get_node_at_location(potential_location):
            self.cursor = potential_location
    
    def next(self) -> None:
        potential_location = (*self.cursor[:-1], self.cursor[-1] + 1)
        if self._get_node_at_location(potential_location):
            self.cursor = potential_location
    
    def previous(self) -> None:
        if self.cursor[-1] > 0:
            self.cursor = (*self.cursor[:-1], self.cursor[-1] - 1)
    
    def on_press(self, key: Key):
        try:
            if key.char.lower() in ['q']:
                return False
        except AttributeError:
            if key == Key.esc:
                return False
            elif key == Key.shift:
                self.shift_pressed = True
            if key == Key.up:
                self.previous()
                self.render()
            elif key == Key.down:
                self.next()
                self.render()
            elif key == Key.left:
                self.up()
                self.render()
            elif key == Key.right:
                self.deeper()
                self.render()
    
    def on_release(self, key: Key):
        if key == Key.shift:
            self.shift_pressed = False
    
    def interactive(self) -> None:
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                self.render()
                listener.join()
        except KeyboardInterrupt:
            return

def build_tree(map: dict[str, dict]) -> Tree:
    def r_build_tree(tree: Tree, sub_map: dict[str, dict]):
        for key in sub_map:
            child = tree.add(key)
            if sub_map[key]:
                r_build_tree(child, sub_map[key])
        return tree

    label = next(iter(map))
    tree = Tree(label)
    return r_build_tree(tree=tree, sub_map=map[label])

def create_atomic_path(map: Tree) -> None:
    def r_create_atomic_path(tree: Tree, index: int, *old_indexes: int) -> None:
        rprint(*old_indexes, index, tree.label)
        for i, child in enumerate(tree.children):
            r_create_atomic_path(child, i, *old_indexes, index)
    
    r_create_atomic_path(tree=map, index=0)

def PRBT_depth_first_traversal(tree: Tree) -> None:
    def r_PRBT_depth_first_traversal(tree: Tree):
        print(tree.label)
        for child in tree.children:
            r_PRBT_depth_first_traversal(child)
    
    r_PRBT_depth_first_traversal(tree)

def depth_first_traversal(tree: Tree) -> None:
    def r_depth_first_traversal(tree: Tree, level: int, index: int):
        rprint("  " * level, level, index, tree.label)
        for index, child in enumerate(tree.children):
            r_depth_first_traversal(child, level + 1, index) 

    r_depth_first_traversal(tree, 0, 0)


if __name__ == "__main__":
    data = {
        "How to start":{
            "Edition Using Keyboard":{
                "Move Between Topics With The Arrows":{},
                "Start Typing to Edit Text":{},
                "Press Ctrl/Meta+Enter to Add Child Topic":{}
            },
            "Edition Using Mouse":{
                "Double Click on a Topic to Edit the Text":{},
                "Double Click on the Canvas to Create Topics":{},
                "Drag and Drop Topics Position":{}
            },
            "Topic Properties":{
                "Multiple Text Styles":{
                    "Color":{},
                    "Styles":{},
                    "Type":{}
                },
                "Different Shapes":{},
                "Add Notes":{}
            },
            "Sharing":{
                "Invite Friends to Collaborate":{},
                "Embed in Blogs":{},
                "Publish your Mind map":{}
            }
        }
    }

    tree = build_tree(data)
    p = PRBT_iTree(Console(), data)
    p.interactive()

    # rprint(tree)
    # depth_first_traversal(tree)

    # rprint("--" * 10)
    # create_atomic_path(tree)

    # rprint("--" * 10)
    # tree = PRBT_iTree(Console(), data)
    # rprint(tree._get_node_at_location((0, 1, 2))) # Drag and Drop Topics Position

    # rprint("--" * 10)
    # PRBT_depth_first_traversal(tree.tree)


    # tree = Tree("Root")
    # child1 = tree.add("Child 1")
    # child2 = tree.add("Child 2")
    # child3 = tree.add("Child 3")
    # grandchild1 = child3.add("Grandchild 1")
    # grandchild2 = child3.add("Grandchild 2")
    # grandgrandchild1 = grandchild2.add("Grandgrandchild 1")
    # child4 = tree.add("Child 4")
    # grandchild3 = child4.add("Grandchild 3")


    # depth_first_traversal(tree)
