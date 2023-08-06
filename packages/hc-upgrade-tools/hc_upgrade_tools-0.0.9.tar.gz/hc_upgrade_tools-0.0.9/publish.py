import os


if __name__=="__main__":
    # check if current git work tree is clean and has no untracked files
    # if yes, checkout to release branch else exit
    if not os.system("git diff --quiet && git diff --cached --quiet"):
        # if release and dev on the same commit, exit
        if os.system("git rev-parse --abbrev-ref HEAD") == "release":
            print("release branch is on the same commit as dev branch, exit")
            exit(1)

        # checkout to release branch
        os.system("git checkout release")
        # merge dev branch to release branch
        os.system("git merge dev")
        # if merge success, push release branch to remote
        if not os.system("git diff --quiet && git diff --cached --quiet"):
            # read the latest tag
            latest_tag = os.popen("git describe --abbrev=0 --tags").read()
            # get the latest tag version
            latest_tag_version = latest_tag.split("v")[1]
            # increase the latest tag version
            latest_tag_version = latest_tag_version.split(".")
            latest_tag_version[-1] = str(int(latest_tag_version[-1]) + 1)
            latest_tag_version = ".".join(latest_tag_version)
            # create new tag
            os.system(f"git tag v{latest_tag_version}")
            # push tag to remote
            os.system(f"git push origin v{latest_tag_version}")
            # push release branch to remote
            os.system("git push origin release")
            # run tox -e publish -- --repository pypi
            os.system("tox -e build && tox -e publish -- --repository pypi")

            if not os.system("git diff --quiet && git diff --cached --quiet"):
                os.system("git checkout dev")

        else:
            # abort merge
            os.system("git merge --abort")

    else:
        # exit
        print("git work tree is not clean, please commit and push your changes first")
        exit(1)
