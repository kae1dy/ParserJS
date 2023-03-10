import tree_sitter
from tree_sitter import Language, Parser
from collections import deque

LANG_PATH = "./tree-sitter-java"
TARGET_PATH = "./build/my-languages.so"

Language.build_library(
    TARGET_PATH,
    [LANG_PATH]
)

JAVA_LANGUAGE = Language(TARGET_PATH, 'java')
parser = Parser()
parser.set_language(JAVA_LANGUAGE)


def parse_code(data_list: list):
    tokens = []

    for line in data_list:
        tree = parser.parse(bytes("class Test {" + line + " }", "utf8"))
        root_node = tree.root_node
        tokens.append(get_tokens(root_node))
    return tokens


# get tokens from AST-tree
def get_tokens(root: tree_sitter.Node) -> list:
    list_nodes = deque([root])
    leaves = []

    while list_nodes:
        node = list_nodes.popleft()
        if node.has_error:
            continue

        if not node.children:
            leaves.append(node.text)

        for children in node.children:
            if children:
                list_nodes.append(children)
    return leaves
