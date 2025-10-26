import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from pydantic import BaseModel
import asyncio
import aiohttp
def plot_distribution(pokemons_plot, var_name):
    colors = {'Débil': '#1f77b4', 'Fuerte': '#ff7f0e'}
    np.random.seed(1<<12)
    jitter = np.random.normal(0, 2, len(pokemons_plot))
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    for fuerte_val, alpha_val in [('Débil', 0.1), ('Fuerte', 0.7)]:
        data_subset = pokemons_plot[pokemons_plot['Fuerte'] == fuerte_val]
        jitter_subset = jitter[pokemons_plot['Fuerte'] == fuerte_val]
        axes[0].scatter(data_subset[var_name], jitter_subset, alpha=alpha_val, s=20,
                    label=fuerte_val, color=colors[fuerte_val])
    axes[0].set_title("Fuertes resaltados")
    axes[0].set_ylabel("")
    axes[0].set_yticks([])
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    for fuerte_val, alpha_val in [('Fuerte', 0.1), ('Débil', 0.7)]:
        data_subset = pokemons_plot[pokemons_plot['Fuerte'] == fuerte_val]
        jitter_subset = jitter[pokemons_plot['Fuerte'] == fuerte_val]
        axes[1].scatter(data_subset[var_name], jitter_subset, alpha=alpha_val, s=20,
                    label=fuerte_val, color=colors[fuerte_val])
    axes[1].set_title("Débiles resaltados")
    axes[1].set_ylabel("")
    axes[1].set_yticks([])
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    for fuerte_val in ['Débil', 'Fuerte']:
        data_subset = pokemons_plot[pokemons_plot['Fuerte'] == fuerte_val]
        jitter_subset = jitter[pokemons_plot['Fuerte'] == fuerte_val]
        axes[2].scatter(data_subset[var_name], jitter_subset, alpha=0.4, s=20,
                    label=fuerte_val, color=colors[fuerte_val])
    axes[2].set_title(f"Proyección de {var_name} de Pokémons")
    axes[2].set_xlabel(var_name)
    axes[2].set_ylabel("")
    axes[2].set_yticks([])
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.show()


class PokemonSchema(BaseModel):
    """
    Esquema para validar los datos adaptados de un Pokémon.
    """
    id: int
    name: str
    weight: int
    height: int
    base_experience: Optional[int]
    type_main: Optional[str]
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


def get_stat_value(stats:list[dict], stat_name: str) -> int:
    """
    Busca en la lista 'stats' el stat cuyo nombre sea stat_name y devuelve su 'base_stat'.
    Si no se encuentra, lanza ValueError.
    """
    for stat in stats:
        if stat.get('stat', {}).get('name') == stat_name:
            return stat.get('base_stat', -1)
    raise ValueError(f"Stat '{stat_name}' not found")


def adapt_pokemon_data(data):
    """
    Adapta el JSON de la API a un dict plano con las claves esperadas por el esquema.
    (No añade 'id' aquí; se añade en fetch_and_adapt).
    """
    return {
        "name": data.get("name"),
        "weight": data.get("weight"),
        "height": data.get("height"),
        "base_experience": data.get("base_experience"),
        "type_main": data.get("types")[0]["type"]["name"] if data.get("types") else None,
        "hp": get_stat_value(data.get("stats", []), "hp"),
        "attack": get_stat_value(data.get("stats", []), "attack"),
        "defense": get_stat_value(data.get("stats", []), "defense"),
        "special_attack": get_stat_value(data.get("stats", []), "special-attack"),
        "special_defense": get_stat_value(data.get("stats", []), "special-defense"),
        "speed": get_stat_value(data.get("stats", []), "speed"),
    }




async def get_pokemon_data(session, pokemon_id: int) -> Optional[dict]:
    """
    Recupera el JSON del endpoint de PokeAPI para el pokemon_id dado.
    Devuelve el dict JSON si la respuesta es 200, de lo contrario lanza ValueError.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        raise ValueError(f"Error fetching Pokemon {pokemon_id}: Status code {response.status}")

async def fetch_and_adapt_async(
        session,
        pokemon_id: int
    ) -> Optional[dict]:
    data = await get_pokemon_data(session, pokemon_id)
    adapted = adapt_pokemon_data(data)
    adapted["id"] = pokemon_id
    pokemon = PokemonSchema(**adapted)
    return pokemon.model_dump()


async def fetch_all_pokemons():
    """
    Obtiene todos los Pokémon
    """
    ids = range(1, 1011)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_adapt_async(session, pokemon_id) for pokemon_id in ids]
        results = await asyncio.gather(*tasks)
    # Filtrar resultados None
    valid_results = [result for result in results if result is not None]
    return valid_results