import pathlib
import typing as tp

# type: ignore


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    ref_file = gitdir / ref
    with ref_file.open("w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with (gitdir / refname).open() as f:
            return f.read().strip()
    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    with (gitdir / "HEAD").open() as f:
        return ref_resolve(gitdir, get_ref(gitdir)[1])


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    try:
        get_ref(gitdir)
    except IndexError:
        return True
    return False


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with (gitdir / "HEAD").open() as f:
        return f.read().strip().split()[1]
