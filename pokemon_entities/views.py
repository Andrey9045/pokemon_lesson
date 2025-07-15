import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    ) 
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)

def show_all_pokemons(request):
    current_time = localtime()
    pokemons = PokemonEntity.objects.filter(
    appeared_at__lte=current_time,
    disappeared_at__gte=current_time
)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemons:
        pokemon = pokemon_entity.pokemon
        relative_image_path = pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL
        image_url = request.build_absolute_uri(relative_image_path)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    pokemons_on_page = []
    for pokemon_entity in pokemons:
        pokemon = pokemon_entity.pokemon
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    relative_image_path = requested_pokemon.photo.url if requested_pokemon.photo else DEFAULT_IMAGE_URL
    image_url = request.build_absolute_uri(relative_image_path)

    if requested_pokemon.evolution:
        evo_prev_img = requested_pokemon.evolution.photo.url if requested_pokemon.evolution.photo else DEFAULT_IMAGE_URL
        evo_prev_title = requested_pokemon.evolution.title
    else:
        evo_prev_img = None
        evo_prev_title = None

    evo = requested_pokemon.evolves_into.first()
    if evo:
        evo_next_img = evo.photo.url if evo.photo else DEFAULT_IMAGE_URL
        evo_next_title = evo.title
    else:
        evo_next_img = None
        evo_next_title = None

    pokemon_data = {
       'title': requested_pokemon.title,
       'img_url': image_url,
       'description': requested_pokemon.description,
       'jap_name': requested_pokemon.jap_name,
       'eng_name': requested_pokemon.eng_name,
       'prev_evolution': requested_pokemon.evolution,  # Передаем объект
       'prev_image_url': evo_prev_img,
       'next_evolution': evo,  # Передаем объект
       'next_image_url': evo_next_img,
   }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_data['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
