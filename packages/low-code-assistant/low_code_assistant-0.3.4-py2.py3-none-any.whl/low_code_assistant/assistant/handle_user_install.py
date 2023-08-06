import os
import pathlib
import site

from low_code_assistant.domino_api import get_domino_api


def in_user_install_mode():
    return __file__.startswith(site.getuserbase())


def symlink_solara_assets():
    prefix = site.getuserbase()

    src = prefix + "/share/solara/cdn"
    dst = pathlib.Path(prefix + "/share/jupyter/nbextensions/_solara")
    dst.mkdir(exist_ok=True, parents=True)
    dst_cdn = dst / "cdn"
    if not dst_cdn.exists():
        os.symlink(src, dst_cdn)


def write_requirements_txt():
    file = pathlib.Path("requirements.txt")
    content = "https://vve589t3tspu.s3.us-west-2.amazonaws.com/1/low_code_assistant-latest-py2.py3-none-any.whl\n"
    if file.exists():
        old_content = file.read_text()
        if "low_code_assistant" not in old_content:
            file.write_text(old_content + "\n" + content)
            return True
    else:
        file.write_text(content)
        return True
    return False


if in_user_install_mode():
    symlink_solara_assets()
    if write_requirements_txt():
        get_domino_api().sync_files("requirements.txt added by low_code_assistant")
