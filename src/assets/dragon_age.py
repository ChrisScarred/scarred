from typing import Dict, Tuple
from statistics import mean
from math import floor


# dragon species and their average life expectancy
SPECIES = {
    "ice": 360,
    "lake": 575,
    "forest": 350,
    "lowlands": 400,
    "mountain": 200,
    "fire": 575
}
# age in years when dragons reach adulthood
DRAGON_ADULT = 1
# average human life expectancy
HUMAN_MEAN = 54
# age in years when humans reach adulthood
HUMAN_ADULT = 18

def get_dragon_age(_type: str, age: float, species_map: Dict[str, int] = SPECIES, human_mean: int = HUMAN_MEAN, human_adult: int = HUMAN_ADULT, dragon_adult: int = 1) -> Tuple[int, int]:
    if age < dragon_adult:
        return _float_to_time((age / dragon_adult) * human_adult)
    max_age = species_map.get(_type, mean(species_map.values()))
    lived_of_max = (age - dragon_adult) / max_age
    return _float_to_time(human_adult + lived_of_max * human_mean)

def _float_to_time(val: float) -> Tuple[int, int]:
    years = floor(val)
    months = round((val - years) * 12)
    return years, months

async def dragon_age_response(_type: str, age: int) -> str:
    y, m = get_dragon_age(_type, age)
    answer = ["Táto postava má"]
    if m == 0:
        answer.append("presne")
    if y == 1:
        answer.append(f"{y} rok")
    elif y > 1 and y < 5:
        answer.append(f"{y} roky")
    elif y >= 5:
        answer.append(f"{y} rokov")
    if m > 0:
        answer.append(f"a {m}")
        if m == 1:
            answer.append("mesiac")
        elif m < 5:
            answer.append("mesiace")
        else:
            answer.append("mesiacov")
    return " ".join(answer) + "."
