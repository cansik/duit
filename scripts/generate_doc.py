import os
import re
import shutil
from pathlib import Path
from typing import Union, List, Optional

import pdoc
import pdoc.web
from markupsafe import Markup


def generate_doc(package_name: str,
                 package_version: str,
                 package_url: Optional[str],
                 required_packages: List[str],
                 output_path: Union[str, os.PathLike],
                 package_paths: List[Union[str, os.PathLike]],
                 extra_asset_path: Union[str, os.PathLike] = "doc"):
    output_path = Path(output_path)
    extra_asset_path = Path(extra_asset_path)

    print(required_packages)

    # clean doc dir
    if output_path.exists():
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # configure pdoc
    pdoc.render.configure(
        footer_text=f"{package_name} v{package_version}",
        logo_link=package_url,
        template_directory=extra_asset_path.joinpath("theme")
    )

    # add additional filters
    def remove_identifier(value: Markup):
        regex = r"(<a\s*href=\".*#\w*\">)(.*\.)([A-Z].*)(</a>)"
        subst = "\\1\\3\\4"
        result = re.sub(regex, subst, value, 0, re.MULTILINE)
        return Markup(result)

    pdoc.render.env.filters["remove_identifier"] = remove_identifier

    # generate pdoc
    pdoc.pdoc(*package_paths, output_directory=output_path)

    # copy doc content
    shutil.copytree(extra_asset_path, output_path.joinpath(extra_asset_path.name))
