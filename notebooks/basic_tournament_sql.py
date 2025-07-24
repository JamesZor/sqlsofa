import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import sofascrape.schemas.general as pydanticschema
from sofascrape.general import TournamentProcessScraper  # type: ignore
from sqlmodel import (  # type: ignore
    Field,
    Relationship,
    Session,
    SQLModel,
    create_engine,
    select,
)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

########################################
### Schema for sql Model
########################################


class Sport(SQLModel, table=True):  # type: ignore
    __tablename__ = "sports"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    categories: List["Category"] = Relationship(back_populates="sport")


class Category(SQLModel, table=True):  # type: ignore
    __tablename__ = "categories"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    sport_id: int = Field(foreign_key="sports.id")

    created_at: datetime = Field(default_factory=datetime.now)

    sport: Sport = Relationship(back_populates="categories")
    tournaments: List["Tournament"] = Relationship(back_populates="category")


class Tournament(SQLModel, table=True):  # type: ignore
    __tablename__ = "tournaments"

    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)

    category_id: int = Field(foreign_key="categories.id")

    # Add timestamps for tracking
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    category: Category = Relationship(back_populates="tournaments")


########################################
### utils functions
########################################


def convert_tournamet_to_sqlmodel(
    tournament: pydanticschema.TournamentData,
) -> Optional[Tuple[Sport, Category, Tournament]]:
    if tournament is None:
        logger.warning(f"tournament is none, can't process. {repr(tournament)}.")
        return None

    try:
        t = tournament.tournament
    except Exception as e:
        logger.warning(f"No 'tournament' field in supplied var, {repr(tournament)}.")
        return None

    # Create Sport object
    sport = Sport(
        id=t.category.sport.id, name=t.category.sport.name, slug=t.category.sport.slug
    )

    # Create Category object
    category = Category(
        id=t.category.id,
        name=t.category.name,
        slug=t.category.slug,
        sport_id=t.category.sport.id,
    )

    # Create Tournament object
    tournament = Tournament(
        id=t.id, name=t.name, slug=t.slug, category_id=t.category.id
    )
    return sport, category, tournament


########################################
### load/save
########################################
class NoteBookUtil:
    def __init__(self, dir_name: str = "example_data"):
        self.data_dir = Path(dir_name)

    def save(self, tournaments_details, filename="tournaments_data.pkl"):
        """Save tournament data using pickle"""
        filepath = self.data_dir / filename

        with open(filepath, "wb") as f:
            pickle.dump(tournaments_details, f)

        print(f"✅ Saved tournament data to {filepath}")
        print(
            f"📊 Saved {len([t for t in tournaments_details.tournaments if t is not None])} tournaments"
        )

    def load(self, filename: str = "tournaments_data.pkl"):
        """Load tournament data using pickle"""
        filepath = self.data_dir / filename

        if not filepath.exists():
            print(f"❌ File {filepath} not found!")
            return None

        with open(filepath, "rb") as f:
            tournaments_details = pickle.load(f)

        print(f"✅ Loaded tournament data from {filepath}")
        print(
            f"📊 Loaded {len([t for t in tournaments_details.tournaments if t is not None])} tournaments"
        )

        return tournaments_details


########################################
### sql engine
########################################


def push_to_sql(sport: Sport, category: Category, tournament: Tournament):
    with Session(engine) as session:
        # 1. Handle Sport (get or create)
        existing_sport = session.get(Sport, sport.id)
        if not existing_sport:
            session.add(sport)
            session.commit()  # Commit to get the ID
            session.refresh(sport)
            print(f"Added sport: {sport.name}")
        else:
            # Update existing sport if needed
            existing_sport.name = sport.name
            existing_sport.slug = sport.slug
            sport = existing_sport  # Use existing for relationships

        # 2. Handle Category (get or create)
        existing_category = session.get(Category, category.id)
        if not existing_category:
            session.add(category)
            session.commit()
            session.refresh(category)
            print(f"Added category: {category.name}")
        else:
            # Update existing category
            existing_category.name = category.name
            existing_category.slug = category.slug
            existing_category.sport_id = category.sport_id
            category = existing_category

        # 3. Handle Tournament (get or create)
        existing_tournament = session.get(Tournament, tournament.id)
        if not existing_tournament:
            session.add(tournament)
            print(f"Added tournament: {tournament.name}")
        else:
            # Update existing tournament
            existing_tournament.name = tournament.name
            existing_tournament.slug = tournament.slug
            existing_tournament.category_id = tournament.category_id
            existing_tournament.updated_at = datetime.now()
            print(f"Updated tournament: {tournament.name}")

    session.commit()


########################################
### main
########################################

if __name__ == "__main__":
    nbu = NoteBookUtil()
    tournament_data = nbu.load()
    tournament_data = [x for x in tournament_data.tournaments if x.data is not None]

    print(len(tournament_data))

    # check loaded data
    for t in tournament_data:
        if t is not None:
            print(t.data)

            s1 = convert_tournamet_to_sqlmodel(t.data)
            print(s1)

    # Load into the test sql
    DATABASE_URL = "postgresql://test_user:test@localhost:5432/tournament_db"
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

    sport, category, tournament = convert_tournamet_to_sqlmodel(tournament_data[0].data)

    push_to_sql(sport, category, tournament)
