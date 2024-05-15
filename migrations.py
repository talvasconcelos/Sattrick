async def m001_initial(db):
    """
    Initial Fantasy League table.
    """
    await db.execute(
        """
        CREATE TABLE sattrick.league (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            country TEXT NOT NULL,
            wallet TEXT NOT NULL
        );
    """
    )

    await db.execute(
        """
        CREATE TABLE sattrick.division (
            id TEXT PRIMARY KEY,
            league TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            rank INTEGER NOT NULL UNIQUE
        );
    """
    )

    await db.execute(
        """
        CREATE TABLE sattrick.manager (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            team TEXT,
            wallet TEXT NOT NULL
        );
    """
    )

    await db.execute(
        """
        CREATE TABLE sattrick.team (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            default_formation TEXT NOT NULL,
            division TEXT NOT NULL
        );
    """
    )

    await db.execute(
        """
        CREATE TABLE sattrick.player (
            player_id TEXT PRIMARY KEY,
            nationality TEXT NOT NULL,
            dob TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            short_name TEXT NOT NULL,
            positions TEXT NOT NULL,
            fitness FLOAT NOT NULL,
            stamina FLOAT NOT NULL,
            form FLOAT NOT NULL,
            attributes TEXT NOT NULL,
            potential_skill INTEGER NOT NULL,
            preferred_foot TEXT NOT NULL,
            value FLOAT NOT NULL
        );
    """
    )
