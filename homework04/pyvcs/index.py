import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object

# type: ignore


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        # PUT YOUR CODE HERE
        head = struct.pack(
            "!LLLLLLLLLL20sH",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        name_bytes = self.name.encode()
        packed_head = head + name_bytes + b"\x00" * (8 - (62 + len(name_bytes)) % 8)
        return packed_head

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # PUT YOUR CODE HERE
        head = struct.unpack("!LLLLLLLLLL20sH", data[:62])
        n_bytes = data[62:]
        n_bytes = n_bytes[: n_bytes.find(b"\x00")]
        return GitIndexEntry(
            ctime_n=head[0],
            ctime_s=head[1],
            mtime_n=head[2],
            mtime_s=head[3],
            dev=head[4],
            ino=head[5] & 0xFFFFFFFFF,
            mode=head[6],
            gid=head[7],
            uid=head[8],
            size=head[9],
            sha1=head[10],
            flags=head[11],
            name=n_bytes.decode("ascii"),
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    index = gitdir / "index"
    if not index.exists():
        return []
    with index.open("rb") as f:
        data = f.read()
    result = []
    header = data[:12]
    main_content = data[12:]
    main_content_copy = main_content
    for _ in range(struct.unpack(">I", header[8:])[0]):
        end_of_entry = len(main_content_copy) - 1
        for j in range(63, len(main_content_copy), 8):
            if main_content_copy[j] == 0:
                end_of_entry = j
                break
        result += [GitIndexEntry.unpack(main_content_copy[: end_of_entry + 1])]
        if len(main_content_copy) > end_of_entry:
            main_content_copy = main_content_copy[end_of_entry + 1 :]
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    signature = b"DIRC"
    version = 2
    result_index = struct.pack("!4sLL", signature, version, len(entries))
    for gie in entries:
        result_index += gie.pack()
    f = open(str(gitdir / "index"), "wb")
    f.write(result_index + hashlib.sha1(result_index).digest())
    f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    entries = read_index(gitdir)
    if details:
        for entry in entries:
            print(f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}")
    else:
        for entry in entries:
            print(entry.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    entries = read_index(gitdir)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        stats = os.stat(path)
        hash = hash_object(data, "blob", write=True)
        entries.append(
            GitIndexEntry(
                ctime_s=int(stats.st_ctime),
                ctime_n=0,
                mtime_s=int(stats.st_mtime),
                mtime_n=0,
                dev=stats.st_dev,
                ino=stats.st_ino,
                mode=stats.st_mode,
                uid=stats.st_uid,
                gid=stats.st_gid,
                size=stats.st_size,
                sha1=bytes.fromhex(hash),
                flags=len(path.name),
                name=str(path),
            )
        )
    if write:
        write_index(gitdir, sorted(entries, key=lambda x: x.name))
