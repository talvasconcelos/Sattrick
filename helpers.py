from typing import List, Optional, Union, Tuple
from datetime import datetime, date, timedelta
import uuid
import random
from loguru import logger

from .player_attributes import (
    Positions,
    OffensiveAttributes,
    PhysicalAttributes,
    DefensiveAttributes,
    IntelligenceAttributes,
    GkAttributes,
    PlayerAttributes,
    PreferredFoot,
)
from .player_models import Player, PlayerTeam
from .models import Team
from abc import ABC, abstractmethod
from .name_generator import team_name, player_name
from .resources.names import NAMES


FORMATION_STRINGS = [
    "3-4-3",
    "3-5-2",
    "3-6-1",
    "4-4-2",
    "4-3-3",
    "4-5-1",
    "5-4-1",
    "5-3-2",
]


class Generator(ABC):
    @abstractmethod
    def generate(self, *args):
        pass


class GeneratePlayerError(Exception):
    pass


class PlayerAttributeGenerator(Generator):
    def __init__(self, max_skill_lvl):
        self.max_skill_lvl = max_skill_lvl

    def generate_skill_values(self, mu: int, sigma: int) -> int:
        value = random.gauss(mu, sigma)
        value = min(value, 99)
        value = max(value, 25)
        return int(value)

    def generate_offensive_attributes(self, mu: int, sigma: int) -> OffensiveAttributes:
        return OffensiveAttributes(
            **{
                attr: self.generate_skill_values(mu, sigma)
                for attr in OffensiveAttributes.__annotations__
            }
        )

    def generate_defensive_attributes(self, mu: int, sigma: int) -> DefensiveAttributes:
        return DefensiveAttributes(
            **{
                attr: self.generate_skill_values(mu, sigma)
                for attr in DefensiveAttributes.__annotations__
            }
        )

    def generate_physical_attributes(self, mu: int, sigma: int) -> PhysicalAttributes:
        return PhysicalAttributes(
            **{
                attr: self.generate_skill_values(mu, sigma)
                for attr in PhysicalAttributes.__annotations__
            }
        )

    def generate_intelligence_attributes(
        self, mu: int, sigma: int
    ) -> IntelligenceAttributes:
        return IntelligenceAttributes(
            **{
                attr: self.generate_skill_values(mu, sigma)
                for attr in IntelligenceAttributes.__annotations__
            }
        )

    def generate_gk_attributes(self, mu: int, sigma: int) -> GkAttributes:
        return GkAttributes(
            **{
                attr: self.generate_skill_values(mu, sigma)
                for attr in GkAttributes.__annotations__
            }
        )

    def get_gk_attributes(self, mu: int, sigma: int) -> PlayerAttributes:
        gk = self.generate_gk_attributes(mu, sigma)
        offensive = self.generate_offensive_attributes(35, 10)
        defensive = self.generate_defensive_attributes(mu, sigma)
        physical = self.generate_physical_attributes(mu, sigma)
        intelligence = self.generate_intelligence_attributes(mu, sigma)
        return PlayerAttributes(
            offensive=offensive,
            physical=physical,
            defensive=defensive,
            intelligence=intelligence,
            gk=gk,
        )

    def get_df_attributes(self, mu: int, sigma: int) -> PlayerAttributes:
        gk = self.generate_gk_attributes(35, 10)
        offensive = self.generate_offensive_attributes(45, 10)
        defensive = self.generate_defensive_attributes(mu, sigma)
        physical = self.generate_physical_attributes(mu, sigma)
        intelligence = self.generate_intelligence_attributes(mu, sigma)
        return PlayerAttributes(
            offensive=offensive,
            physical=physical,
            defensive=defensive,
            intelligence=intelligence,
            gk=gk,
        )

    def get_mf_attributes(self, mu: int, sigma: int) -> PlayerAttributes:
        gk = self.generate_gk_attributes(35, 10)
        offensive = self.generate_offensive_attributes(50, 20)
        defensive = self.generate_defensive_attributes(mu, sigma)
        physical = self.generate_physical_attributes(mu, sigma)
        intelligence = self.generate_intelligence_attributes(mu, sigma)
        return PlayerAttributes(
            offensive=offensive,
            physical=physical,
            defensive=defensive,
            intelligence=intelligence,
            gk=gk,
        )

    def get_fw_attributes(self, mu: int, sigma: int) -> PlayerAttributes:
        gk = self.generate_gk_attributes(35, 10)
        offensive = self.generate_offensive_attributes(mu, sigma)
        defensive = self.generate_defensive_attributes(45, 10)
        physical = self.generate_physical_attributes(mu, sigma)
        intelligence = self.generate_intelligence_attributes(mu, sigma)
        return PlayerAttributes(
            offensive=offensive,
            physical=physical,
            defensive=defensive,
            intelligence=intelligence,
            gk=gk,
        )

    def generate(
        self, positions: list[Positions], mu: int = 50, sigma: int = 20
    ) -> PlayerAttributes:
        if mu is None:
            mu = 50

        if sigma is None:
            sigma = 20

        match positions[0]:
            case Positions.GK:
                attributes = self.get_gk_attributes(mu, sigma)
            case Positions.DF:
                attributes = self.get_df_attributes(mu, sigma)
            case Positions.MF:
                attributes = self.get_mf_attributes(mu, sigma)
            case Positions.FW:
                attributes = self.get_fw_attributes(mu, sigma)

        return attributes


class PlayerGenerator(Generator):
    def __init__(
        self,
        today: Union[datetime, date] = date.today(),
        max_age: int = 35,
        min_age: int = 16,
        max_skill_lvl: int = 99,
    ):
        if min_age > max_age:
            raise GeneratePlayerError(
                "Minimum age must not be greater than maximum age!"
            )

        self.players_obj: List[Player] = []
        self.nationalities = self._get_nationalities()
        self.names = self._get_names()

        year = timedelta(seconds=31556952)  # definition of a Gregorian calendar date
        self.today = today
        self.max_age = max_age * year
        self.min_age = min_age * year
        self.max_skill_lvl = max_skill_lvl

    @staticmethod
    def _get_nationalities():
        return [d["region"] for d in NAMES]
        # with open(NAMES_FILE, "r", encoding="utf-8") as fp:
        #     data = json.load(fp)
        #     return [d["region"] for d in data]

    @staticmethod
    def _get_names():
        return NAMES
        # with open(NAMES_FILE, "r", encoding="utf-8") as fp:
        #     return json.load(fp)

    def _get_names_from_region(self, region: str):
        for reg in self.names:
            return reg if reg["region"] == region else random.choice(self.names)

    def generate_id(self):
        return str(uuid.uuid4())

    def generate_nationality(self, nat: Optional[str]) -> str:
        """
        Returns the player's nationality. If you define a nationality for any reason,
        you should get this nationality here.
        """
        return nat or random.choice(self.nationalities)

    def generate_dob(self):
        """
        Generates the player's date of birth
        """
        # get a random date between 16 and 35 years ago
        return self.today - timedelta(days=random.randint(16 * 365, 35 * 365))
        # return datetime.combine(
        #     self.today - timedelta(days=random.randint(16 * 365, 35 * 365)),
        #     datetime.min.time(),
        # )

    def generate_name(self, region: Optional[str]) -> Tuple[str, str, str]:
        if region is None:
            region = random.choice(self.nationalities)
        name = player_name.name()
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[-1]
        # names = self._get_names_from_region(region)
        # first_name = random.choice(names["male"]).encode('utf-8')
        # last_name = random.choice(names["surnames"]).encode('utf-8')
        short_name = f"{last_name}"
        return first_name, last_name, short_name

    def generate_potential_skill(
        self, skill: PlayerAttributes, positions: list[Positions], age: int
    ) -> int:
        """
        Generates the player's potential skill.
        """
        age_diff = int((self.max_age.days * 365.25) - age)
        age_diff = max(age_diff, 0)
        ovr = skill.get_overall(positions[0])

        if age_diff == 0:
            potential = ovr
        else:
            potential = ovr + random.randint(0, 20)
            potential = min(potential, 99)
        return potential

    def generate_positions(
        self, desired_pos: Optional[list[Positions]]
    ) -> list[Positions]:
        if desired_pos:
            return desired_pos
        positions = list(Positions)
        return random.choices(positions)

    @staticmethod
    def generate_preferred_foot() -> PreferredFoot:
        return random.choice(list(PreferredFoot))

    def generate_player_value(
        self, skill: int, age: int, potential_skill: int
    ) -> float:
        """
        Should return how much a player's worth.
        """
        age_diff = int((self.max_age.days * 365.25) - age)
        age_diff = max(age_diff, 0)
        pot_skill = potential_skill
        base_value = 1000
        logger.info(f"Age: {age}")
        logger.info(f"Age diff: {age_diff}")
        return base_value + (age_diff * 100) + (skill * 50) + (pot_skill * 10)

    def get_players_dictionaries(self) -> List[dict]:
        if not self.players_obj:
            raise GeneratePlayerError("Players objects were not generated!")
        return [player.dict() for player in self.players_obj]

    def generate_player_form(self) -> float:
        return round(random.random() * 100, 2)

    def generate_player_fitness(self) -> float:
        return round(random.random(), 2)

    def generate_player(
        self,
        region: Optional[str] = None,
        mu: int = 50,
        sigma: int = 20,
        desired_pos: Optional[List[Positions]] = None,
    ) -> Player:
        attr_gen = PlayerAttributeGenerator(self.max_skill_lvl)
        player_id = self.generate_id()
        nationality = self.generate_nationality(region)
        first_name, last_name, short_name = self.generate_name(region)
        dob = self.generate_dob()
        age = int((self.today - dob).days * 0.0027379070)
        positions = self.generate_positions(desired_pos)
        preferred_foot = self.generate_preferred_foot()
        attributes = attr_gen.generate(positions, mu, sigma)
        potential_skill = self.generate_potential_skill(attributes, positions, age)
        value = self.generate_player_value(
            attributes.get_overall(positions[0]),
            age,
            potential_skill,
        )
        form = self.generate_player_form()
        fitness = self.generate_player_fitness()

        # logger.debug(f"player Age and DOB: {age} - {dob}")

        return Player(
            player_id=player_id,
            nationality=nationality,
            dob=str(dob),
            first_name=first_name,
            last_name=last_name,
            short_name=short_name,
            positions=positions,
            fitness=fitness,
            stamina=100.0,  # This is set to a default value of 100.0
            form=form,
            attributes=attributes,
            potential_skill=potential_skill,
            preferred_foot=preferred_foot,
            value=value,
        )

        # return Player(
        #     player_id,
        #     nationality,
        #     dob,
        #     first_name,
        #     last_name,
        #     short_name,
        #     positions,
        #     fitness,
        #     100.0,
        #     form,
        #     attributes,
        #     potential_skill,
        #     preferred_foot,
        #     value,
        # )

    def generate(
        self,
        amount: int,
        region: Optional[str] = None,
        desired_pos: Optional[List[Positions]] = None,
    ):
        self.players_obj = [
            self.generate_player(region, desired_pos=desired_pos) for _ in range(amount)
        ]


class TeamGenerator(Generator):
    """
    Teams are defined in a definition file.

    The definition file is a list of teams. However, teams do not contain a squad by default,
    and a squad should be generated for each team.
    """

    def __init__(
        self, country: str, division: str, season_start: date = date.today(), num_teams: int = 20
    ) -> None:
        self.season_start = season_start
        self.player_gen = PlayerGenerator()
        self.num_teams = num_teams
        self.country = country
        self.countries_list = self._get_countries()
        self.division = division

    @staticmethod
    def _get_countries() -> List[str]:
        return [d["region"] for d in NAMES]
        # with open(NAMES_FILE, "r", encoding="utf-8") as fp:
        #     data = json.load(fp)
        #     return [d["region"] for d in data]

    def _get_nationalities(
        self, country: str, countries: List
    ) -> Tuple[List[str], List[float]]:
        nationalities = []
        probabilities = []
        # native
        native: float = 0.85
        nationalities.append(country)
        probabilities.append(native)
        # foreigner
        foreigner: float = 1 - native
        coeff = int(foreigner / 0.05)
        mini_list = random.sample(countries, coeff)
        for ele in mini_list:
            nationalities.append(ele)
            probabilities.append(foreigner)

        return nationalities, probabilities

    def generate_player_team(
        self,
        mu: int,
        sigma: int,
        nationality: str,
        team_id: str,
        shirt_number: int,
        positions: List[Positions],
    ) -> PlayerTeam:
        player = self.player_gen.generate_player(nationality, mu, sigma, positions)
        return PlayerTeam(player=player, team=team_id, number=shirt_number)

    def generate_squad(self, team_id: str, country: str, squad_definition: dict, countries: List) -> List[PlayerTeam]:
        # Define needed positions more compactly with counts
        position_counts = {
            Positions.GK: 3,
            Positions.DF: 6,
            Positions.MF: 6,
            Positions.FW: 4
        }

        # Create a flat list of positions
        needed_positions = [pos for pos, count in position_counts.items() for _ in range(count)]

        # Generate unique shirt numbers
        shirt_numbers = random.sample(range(1, 100), len(needed_positions))

        # Retrieve mean and standard deviation for player generation
        mu, sigma = squad_definition["mu"], squad_definition["sigma"]

        # Retrieve nationalities and their probabilities based on country affinity
        nationalities, probabilities = self._get_nationalities(country, countries)

        # Generate players for each position
        return [
            self.generate_player_team(
                mu,
                sigma,
                random.choices(nationalities, probabilities)[0],
                team_id,
                shirt_numbers[i],
                [needed_positions[i]],
            )
            for i in range(len(needed_positions))
        ]

    def generate(self) -> Tuple[List[Team], List[PlayerTeam]]:
        clubs = []
        squads = []
        for _ in range(self.num_teams):
            club = {
                "id": str(uuid.uuid4()),
                "name": team_name.dwarf(),
                "country": self.country,
                "default_formation": random.choice(FORMATION_STRINGS),
                "division": self.division,
            }
            mu = random.randint(40, 60)
            sigma = random.randint(10, 25)
            squad = self.generate_squad(
                club["id"],
                club["country"],
                {"mu": mu, "sigma": sigma},
                self.countries_list,
            )
            squads.extend(squad)
            clubs.append(Team(**club))

        return clubs, squads
