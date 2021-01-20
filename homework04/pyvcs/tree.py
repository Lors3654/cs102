import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index  # type:ignore
from pyvcs.objects import hash_object  # type:ignore
from pyvcs.refs import resolve_head  # type:ignore
from pyvcs.refs import get_ref, is_detached, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    tree_content: tp.List[tp.Tuple[int, str, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    files = []
    for i in (gitdir.parent / dirname).glob("*"):
        files.append(str(i))
    for entry in index:
        if entry.name in files:
            tree_content.append((entry.mode, str(gitdir.parent / entry.name), entry.sha1))
        else:
            dir_name = entry.name.lstrip(dirname).split("/", 1)[0]
            if not dir_name in subtrees:
                subtrees[dir_name] = []
            subtrees[dir_name].append(entry)
    for name in subtrees:
        if dirname != "":
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], dirname + "/" + name)),
                )
            )
        else:
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], name)),
                )
            )
    tree_content.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2] for elem in tree_content
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    if author is None:
        author = "{} <{}>".format(os.environ["GIT_AUTHOR_NAME"], os.environ["GIT_AUTHOR_EMAIL"])
    assert isinstance(author, str)
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = "{} {}{:02}{:02}".format(
        timestamp,
        "+" if utc_offset > 0 else "-",
        abs(utc_offset) // 3600,
        (abs(utc_offset) // 60) % 60,
    )
    lines = ["tree " + tree]
    if parent:
        lines.append("parent " + parent)
    lines.append("author {} {}".format(author, author_time))
    lines.append("committer {} {}".format(author, author_time))
    lines.append("")
    lines.append(message)
    lines.append("")
    data = "\n".join(lines).encode()
    sha1 = hash_object(data, "commit", write=True)
    return sha1
