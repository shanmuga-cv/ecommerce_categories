import json


class CategoryNode:
    def __init__(self, category_name: str, link: str, website: str, parent: 'CategoryNode'):
        self.category_name = category_name
        self.link = link
        self.children = {}
        self.website = website
        self.parent = parent

    @property
    def category_hierarchy(self):
        if self.parent is None:
            return []
        else:
            return self.parent.category_hierarchy + [self.category_name]

    def add(self, category_tree, url, website):
        node = self.get_or_create_path(category_tree)
        node.link = url
        node.website = website

    def get_or_create_path(self, path):
        if len(path)==0:
            return self
        node = self.children.get(path[0])
        if node is None:
            node = CategoryNode(category_name=path[0], link=None, website=None, parent=self)
            self.children[path[0]] = node
        return node.get_or_create_path(path[1:])

    def get_path(self, path):
        if len(path)==0:
            return self
        node = self.children[path[0]]
        return node.get_path(path[1:])


    def __str__(self):
        child_items = self.children.values()
        child_str = ", ".join(str(item) for item in child_items)
        return f"{{{self.category_name}: {{{child_str}}}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def parse(cls, file_name):
        with open(file_name) as fin:
            category_tree_records = json.load(fin)
        tree = CategoryNode("", None, None, None)
        for record in category_tree_records:
            tree.add(**record)
        return tree

    def traverse(self):
        for x in self.children.values():
            yield x
            yield from x.traverse()

    def traverse_leaf_nodes(self):
        return (x for x in self.traverse() if len(x.children) == 0)