from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    session.install(".[dev,test]")
    login_user_1 = "lndb login raspbear@gmx.de --password MmR4YuQEyb0yxu7dAwJZTjLzR1Az2lN4Q4IduDlO"  # noqa
    create_instance_1 = "lndb init --storage mydata --schema bionty,wetlab,bfx"  # noqa
    session.run(*(login_user_1.split(" ")))
    session.run(*(create_instance_1.split(" ")))
    session.run(
        "pytest",
        "-s",
        "--cov=lndb_hub",
        "--cov-append",
        "--cov-report=term-missing",
    )
    session.run("coverage", "xml")
    prefix = "." if Path("./lndocs").exists() else ".."
    session.install(f"{prefix}/lndocs")
    session.run("lndocs")
    session.run(
        "pytest",
        "-s",
        "--cov=lndb_hub",
        "--cov-append",
        "--cov-report=term-missing",
    )
