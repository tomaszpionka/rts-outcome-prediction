Jupytext resync after manual notebook execution

Problem: You re-ran .ipynb in Jupyter, which updated cell outputs/metadata. Now the .py (source) and .ipynb (sibling) are out of sync, and the jupytext pre-commit hook blocks.

Fix (30 seconds):

# 1. Re-sync: jupytext picks the newer file and updates the other
source .venv/bin/activate && poetry run jupytext --sync <path_to_.py_file>

# 2. Re-stage both files
git add <path_to_.py_file> <path_to_.ipynb_file>

# 3. Commit normally
git commit -F .github/tmp/commit.txt

Bulk version (all notebooks at once):

source .venv/bin/activate && \
find sandbox -name "*.py" -path "*/01_exploration/*" | \
xargs poetry run jupytext --sync

# Then stage everything
git add sandbox/

Key detail: jupytext --sync compares timestamps. If .ipynb is newer (you just ran it), it updates .py from .ipynb. If .py is newer (Claude edited it), it updates .ipynb from .py. Either way, after sync both files agree and the hook
passes.