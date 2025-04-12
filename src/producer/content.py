from faker import Faker
from mediaprovider import MediaContentProvider

class Content: 
    def __init__(self, id, title, type, episode, season, provider, genre, release_year, duration, language):
        """
        Initialize a Content object with the given attributes.  

        Args:   
            id (str): Unique identifier for the content.
            title (str): Title of the content.
            type (str): Type of content (e.g., movie, series).
            episode (int): Episode number (if applicable).
            season (int): Season number (if applicable).
            provider (str): Content provider or platform.
            genre (str): Genre of the content.
            release_year (int): Year of release.
            duration (int): Duration in minutes.
            language (str): Language of the content.
        """

        self.id = id
        self.title = title
        self.type = type
        self.episode = episode
        self.season = season
        self.provider = provider
        self.genre = genre
        self.release_year = release_year
        self.duration = duration
        self.language = language

    def as_dict(self):
        """
        Convert the Content object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Content object.
        """
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "episode": self.episode,
            "season": self.season,
            "provider": self.provider,
            "genre": self.genre,
            "release_year": self.release_year,
            "duration": self.duration,
            "language": self.language
        }


    @classmethod
    def generate_content_data(cls):

        f = Faker()
        f.add_provider(MediaContentProvider)

        while True:
            data = f.content()
            yield cls(id=f.uuid4(), **data)

     
