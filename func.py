import tree_sitter
from tree_sitter import Language, Parser
from pathlib import Path
import csv
from collections import deque

DATA_PATH = "./dataset"
LANG_PATH = "./tree-sitter-javascript"
TARGET_PATH = "./build/my-languages.so"


def parse_code(data_path=DATA_PATH, lang_path=LANG_PATH, target_path=TARGET_PATH):
    Language.build_library(
        TARGET_PATH,
        [LANG_PATH]
    )
    JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
    parser = Parser()
    parser.set_language(JS_LANGUAGE)
    data = Path(DATA_PATH)

    tokens = []

    for file in data.iterdir():
        parser = Parser()
        parser.set_language(JS_LANGUAGE)
        # test on manual100.tsv (to reduce time)
        # if file.suffix == ".tsv":
        if file.name == 'manual100.tsv':

            with open(str(file)) as code:
                code_tsv = csv.reader(code, delimiter="\t")

                for line in code_tsv:
                    # maybe "class Test {" + line[0] + " }" ???
                    tree = parser.parse(bytes(line[0], "utf8"))
                    root_node = tree.root_node
                    tokens.append(get_tokens(root_node))
    return tokens


# get tokens from AST-tree
def get_tokens(root: tree_sitter.Node) -> list:
    list_nodes = deque([root])
    leaves = []

    while list_nodes:
        node = list_nodes.popleft()
        if not node.children:
            leaves.append(node.type)

        for children in node.children:
            if children:
                list_nodes.append(children)
    return leaves
