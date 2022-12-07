from utils.read_txt_data import txt_to_str


class FileTree:
    def __init__(self, test=False):
        self.root = self.create_new_dir("/", parent=None)
        self.active_dir = self.root
        self.cmds = self.load_cmds(test=test)

    def create_new_dir(self, name, parent):
        return {"name": name, "children": [], "parent": parent, "type": "dir"}

    def create_new_file(self, name, parent, size):
        return {"name": name, "parent": parent, "size": size, "type": "file"}

    def load_cmds(self, test=False):
        if test:
            file = "data/07_test.txt"
        else:
            file = "data/07.txt"
        return txt_to_str(file).split("\n")

    def process_cmds(self):
        idx = 0
        while idx < len(self.cmds):
            cmd = self.cmds[idx]
            assert cmd.startswith("$")
            if cmd == "$ cd /":
                self.active_dir = self.root
            elif cmd == "$ cd ..":
                self.active_dir = self.active_dir["parent"]
            elif cmd.startswith("$ cd"):
                sub_folder = cmd.split(" ")[2]
                changed_folders = False
                for child in self.active_dir["children"]:
                    if child["name"] == sub_folder:
                        self.active_dir = child
                        changed_folders = True
                        break
                assert changed_folders == True
            elif cmd == "$ ls":
                idx += 1
                while idx < len(self.cmds) :
                    cmd = self.cmds[idx]
                    if cmd.startswith("$"):
                        idx -= 1
                        break
                    if cmd.startswith("dir"):
                        _, name = cmd.split(" ")
                        self.active_dir["children"].append(self.create_new_dir(name, self.active_dir))
                    else:
                        size, name = cmd.split(" ")
                        self.active_dir["children"].append(self.create_new_file(name, self.active_dir, int(size)))
                    idx += 1
            else:
                raise ValueError(cmd)
            idx += 1

    def get_total_sizes(self):
        def expand(node):
            total_size = 0
            for child in node["children"]:
                if child["type"] == "file":
                    total_size += child["size"]
                else:
                    sub_size = expand(child)
                    total_size += sub_size
            node["total_size"] = total_size
            return total_size

        expand(self.root)

    def get_first_answer(self):
        self.first_answer = 0
        def expand(node):
            if node["type"] == "dir":
                if node["total_size"] < 100000:
                    self.first_answer += node["total_size"]
                for child in node["children"]:
                    expand(child)

        expand(self.root)
        print(self.first_answer)


    def find_deletion_candidate(self, threshold):
        self.current_candidate = (None, 1000000000000)
        def expand(node):
            if node["type"] == "dir":
                dir_size = node["total_size"]
                if dir_size > threshold:
                    if dir_size < self.current_candidate[1]:
                        self.current_candidate = node, dir_size
                for child in node["children"]:
                    expand(child)
        expand(self.root)
        print(self.current_candidate[1])

def first():
    file_tree = FileTree(test=False)
    file_tree.process_cmds()
    file_tree.get_total_sizes()
    file_tree.get_first_answer()
    print("stop")

def second():
    file_tree = FileTree(test=False)
    file_tree.process_cmds()
    file_tree.get_total_sizes()

    total_space = 70000000
    used_space = file_tree.root["total_size"]
    free_space = total_space - used_space
    threshold = 30000000 - free_space
    file_tree.find_deletion_candidate(threshold)


if __name__ == "__main__":
    second()
