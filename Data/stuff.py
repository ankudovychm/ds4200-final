import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Create a rectangular figure (width > height) with a white background
fig, ax = plt.subplots(figsize=(6,3), facecolor='white')
ax.set_facecolor('white')
plt.axis('off')

# Initialize a Sankey with minimal spacing and no numeric formatting
sankey = Sankey(
    ax=ax,
    scale=1.0,       # scaling factor so the flows match our chosen values
    format='',       # no numeric labels
    gap=0.3          # spacing between flows
)

# Add a single Sankey diagram block:
# - One positive flow of 3.0 units coming in from the left
# - Three negative flows (1.2, 1.0, and 0.8) going out to the right
# - All orientations set to 0 (left to right)
sankey.add(
    flows=[3.0, -1.2, -1.0, -0.8],
    orientations=[0, 0, 0, 0],
    pathlengths=[1.0, 1.2, 1.2, 1.2],
    trunklength=1.5,
    facecolor='#A0FFBF',  # lighter green for the interior
    edgecolor='#1DB954',  # darker green for the edges
    linewidth=2,
    patchlabel=''          # no label text
)

# Finalize and remove any remaining text
diagrams = sankey.finish()
for diagram in diagrams:
    for txt in diagram.texts:
        txt.set_visible(False)    # hide default text
    diagram.patch.set_linewidth(2)

plt.tight_layout(pad=0)
plt.savefig("sankey.png", bbox_inches='tight', pad_inches=0, dpi=300, transparent=False)
plt.show()