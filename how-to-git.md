# Git commands:
### Make sure you have all the most recent versions of all remote branches
```shell script
git fetch --all
```
### Create new branch from the origin/test branch
```shell script
git checkout -b yourbranchname origin/test
```
### (Make your changes...And when you're done):
### Add all your changes to be Staged for commit
```shell script
git add -A
```
### Commit all your changes
```shell script
git commit -m "message"
```
### Make sure you have all the most recent versions of all remote branches *again*
```shell script
git fetch --all
```
### Pull aka merge in all the most recent changes that others might have made to origin/test
```shell script
git merge origin/test
```
### Push to remote
```shell script
git push -u origin yourbranchname
```
### DONE

# Or... VS Code buttons:
### Make sure you have all the most recent versions of all remote branches
Git area 3-dots > Pull, Push > Fetch From All Remotes
### Create new branch from the origin/test branch
Git area 3-dots > Branch > Create Branch From > (input new branch name) > (select origin/test)
### (Make your changes...And when you're done):
### Add all your changes to be Staged for commit
Git area (+ all items in Changes so they move to Staged Changes)
### Commit all your changes
Git area (input a message in the top of git area) > (click the check mark in the top area next to Staged Changes)
### Make sure you have all the most recent versions of all remote branches *again*
Git area 3-dots > Pull, Push > Fetch From All Remotes
### Pull aka merge in all the most recent changes that others might have made to origin/test
Git area 3-dots > Branch > Merge Branch... > (select origin/test)
### Push to remote
Git area 3-dots > Pull, Push > Push To ... > (select origin)
### DONE
