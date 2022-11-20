from typing import Optional

import typer
import os

app = typer.Typer()

def call_r(function: str, args):
    cmd = f"Rscript -e \'{function}({', '.join(args)})\'"
    # print(cmd)
    os.system(cmd)

@app.command()
def install(
    package: str,
    gh: bool = typer.Option(False, help = "Install a package from GitHub."),
):
    package = f'"{package}"'
    if gh:
        call_r("devtools::install_github", [package])
    else:
        call_r("install.packages", [package])


@app.command()
def version(package: str):
    os.system(f"Rscript -e 'cat(packageDescription(\"{package}\", fields = \"Version\"), sep = \"\n\")'")

@app.command()
def upgrade(y: bool = typer.Option(False, help = "Don't ask before updating packages.")):
    if y:
        call_r("update.packages", ["ask = FALSE"])
    else:
        print("The following packages will be updated:\n")
        os.system("Rscript -e 'old.packages()[, c(3, 5)]'")
        update = input("Update these packages [y/n]? ")

        if update == "y" or update == "Y":
            call_r("update.packages", ["ask = FALSE"])
    

@app.command()
def remove(
    package: str,
    force: bool = typer.Option(..., prompt="Are you sure you want to remove the package?")
):
    package = f'"{package}"'
    if force:
        call_r("remove.packages", [package])
    else:
        print(f"Cancelled removal of {package}")

