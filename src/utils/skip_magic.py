from IPython.core.magic import register_cell_magic

@register_cell_magic
def skip(line, cell):
    """A cell magic that skips execution of the cell body."""
    print("Skipped cell")