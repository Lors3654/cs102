import hashlib
import os
import pathlib
import re
import stat
import sys
import typing as tp
import zlib

# type: ignore
from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    header = (fmt + " " + str(len(data))).encode()
    full_data = header + b"\x00" + data
    hash_sum_data = hashlib.sha1(full_data).hexdigest()
    if write:
        path = repo_find()
        (path / "objects" / hash_sum_data[:2]).mkdir(exist_ok=True)
        with (path / "objects" / hash_sum_data[:2] / hash_sum_data[2:]).open("wb") as f:
            f.write(zlib.compress(full_data))
    return hash_sum_data


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    if 4 > len(obj_name) or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = repo_find() / "objects"
    obj_list = []
    for file in (objects / obj_name[:2]).glob("*"):
        cur_obj_name = file.parent.name + file.name
        if obj_name == cur_obj_name[: len(obj_name)]:
            obj_list.append(cur_obj_name)
    if not obj_list:
        raise Exception(f"Not a valid object name {obj_name}")
    return obj_list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    with (gitdir / "objects" / sha[:2] / sha[2:]).open("rb") as f:
        data = zlib.decompress(f.read())
    return data.split(b" ")[0].decode(), data.split(b"\00", maxsplit=1)[1]


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    i = 0
    entries = []
    for _ in range(1000):
        end = data.find(b"\x00", i)
        if end == -1:
            break
        mode_str, path = data[i:end].decode().split()
        mode = int(mode_str, 8)
        digest = data[end + 1 : end + 21]
        entries.append((mode, path, digest.hex()))
        i = end + 1 + 20
    return entries


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    fmt, data = read_object(obj_name, repo_find())
    if fmt == "blob" or fmt == "commit":
        print(data.decode())
    else:
        for i in read_tree(data):
            print(f"{i[0]:06}", "tree" if i[0] == 40000 else "blob", i[1] + "\t" + i[2])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    result: tp.Dict[str, tp.Any] = {"message": []}
    for i in map(lambda x: x.decode(), raw.split(b"\n")):
        if "tree" in i or "parent" in i or "author" in i or "committer" in i:
            name, val = i.split(" ", maxsplit=1)
            result[name] = val
        else:
            result["message"].append(i)
    return result
