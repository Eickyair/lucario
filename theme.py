"""
theme.py
Tema oscuro "Tokyo City" para matplotlib y seaborn.

Uso:
    use_tokyo()  # aplica el estilo globalmente
    reset_theme()  # restaura los rcParams por defecto
"""

from matplotlib import rcParams, rcdefaults, pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cycler import cycler
import seaborn as sns

# Paleta principal inspirada en "Tokyo city" (neones sobre fondo oscuro)
tokyo_palette = [
    "#00e5ff",  # cian eléctrico
    "#ff3d81",  # rosa neón
    "#7c4dff",  # violeta brillante
    "#00ffa3",  # verde menta neón
    "#ffd166",  # ámbar suave
    "#5be7ff",  # celeste claro
]

# Colores de fondo / texto
_bg = "#0b0f1a"        # fondo principal (muy oscuro)
_axes_bg = "#0f1724"   # fondo de ejes ligeramente contrastado
_grid = "#172133"      # color de cuadrícula sutil
_text = "#e6f0ff"      # color de texto claro
_dim = "#9aa7bf"       # texto secundario / ticks

# Ciclo de color para matplotlib
_color_cycle = cycler("color", tokyo_palette)

# Colormap para mapas de calor / imshow (degradado neón)
tokyo_cmap = LinearSegmentedColormap.from_list(
    "tokyo_cmap",
    [
        "#06080c",
        "#001f2d",
        "#004d66",
        "#00e5ff",
        "#7c4dff",
        "#ff3d81",
        "#ffd166",
    ],
    N=256,
)


def _build_rc():
    """Construye el diccionario de rcParams para el tema."""
    return {
        # Figura y ejes
        "figure.facecolor": _bg,
        "axes.facecolor": _axes_bg,
        "axes.edgecolor": _grid,
        "axes.labelcolor": _text,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlesize": 22,
        "axes.labelsize": 15,
        "axes.prop_cycle": _color_cycle,
        # Grid y líneas
        "grid.color": _grid,
        "grid.linestyle": "-",
        "grid.linewidth": 0.6,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        # Texto y ticks
        "text.color": _text,
        "xtick.color": _dim,
        "ytick.color": _dim,
        "xtick.direction": "out",
        "ytick.direction": "out",
        # Legend
        "legend.facecolor": "#0d1320",
        "legend.edgecolor": _grid,
        "legend.frameon": True,
        "legend.fontsize": 13,
        # Figure spacing
        "figure.autolayout": True,
        # Image interpolation
        "image.cmap": "tokyo_cmap",
        # Savefig defaults
        "savefig.facecolor": _bg,
        "savefig.edgecolor": _bg,
    }


def use_tokyo():
    """
    Aplica el tema Tokyo City globalmente para matplotlib y seaborn.
    """
    rc = _build_rc()
    
    # Registrar el colormap personalizado
    plt.colormaps.register(cmap=tokyo_cmap, name="tokyo_cmap")
    
    # Aplicar configuración de matplotlib
    rcParams.update(rc)
    
    # Aplicar tema de seaborn
    sns.set_theme(
        style="darkgrid",
        palette=tokyo_palette,
        rc={
            "axes.facecolor": _axes_bg,
            "grid.color": _grid,
            **rc
        }
    )


def reset_theme():
    """
    Restaura los rcParams originales de matplotlib y el estilo de seaborn.
    """
    rcdefaults()
    sns.reset_defaults()