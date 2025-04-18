from faker import Faker
from faker.providers import BaseProvider


class MediaContentProvider(BaseProvider):
    
    content_types = ['Movie', 'TV Show', 'Documentary', 'Animation', 'Short Film'
                    , 'Mini-series', 'Reality Show']
    
    content_providers = [
        'Netflix', 'Hulu', 'Amazon Prime Video', 'Disney+', 'HBO Max', 
        'Apple TV+', 'YouTube', 'Vimeo', 'Peacock', 'Paramount+'
    ]

    language = ['en', 'es', 'fr']

    duration = {
        'Movie': [90, 120],
        'TV Show': [20, 60],
        'Documentary': [30, 90],
        'Animation': [30, 120],
        'Short Film': [5, 30],
        'Mini-series': [60, 120],
        'Reality Show': [20, 60]
    }

    seasons ={
        'Movie': -1,
        'TV Show': [1, 15],
        'Documentary': -1,
        'Animation': -1,
        'Short Film': -1,
        'Mini-series': [1, 5],
        'Reality Show': [1, 20]
    }

    genres = ['Action', 'Drama', 'Comedy', 'Thriller', 'Horror', 'Action-comedy',
             'Romantic', 'Science Fiction', 'Fantasy', 'Mystery', 'Adventure',
             'Documentary', 'Animation', 'Family', 'Musical', 'Biography']
    

    title_formats = [
        "The {noun} of {noun}",
        "{adjective} {noun}",
        "The {adjective} {noun}",
        "{noun} {verb}",
        "{proper_noun}'s {noun}",
        "{verb} the {noun}",
        "The {number} {noun}s",
        "{adjective} {noun}s",
        "{noun}: {proper_noun}",
        "The {noun} in the {noun}",
        "{adjective} {noun}: {proper_noun}",
        "{noun} {preposition} {noun}"
    ]
    
    # Word lists for title generation
    nouns = ["House", "Story", "Life", "World", "Game", "Night", "Day", "King", "Queen", 
             "Castle", "Empire", "Journey", "Road", "Secret", "Dream", "Shadow", "Light",
             "Mountain", "River", "Ocean", "Star", "Planet", "Hero", "Legend", "Myth"]
    
    adjectives = ["Dark", "Bright", "Silent", "Loud", "Ancient", "Modern", "Wild", "Quiet",
                  "Hidden", "Lost", "Eternal", "Broken", "Perfect", "Golden", "Silver", 
                  "Crystal", "Frozen", "Burning", "Sacred", "Magical", "Mysterious"]
    
    verbs = ["Run", "Hide", "Seek", "Find", "Love", "Hate", "Build", "Destroy", "Create",
             "Begin", "End", "Rise", "Fall", "Fight", "Surrender", "Remember", "Forget"]
    
    proper_nouns = ["Avalon", "Elysium", "Atlantis", "Gotham", "Olympus", "Eden",
                    "Alexandria", "Shangri-La", "Valhalla", "Camelot", "Narnia"]
    
    prepositions = ["of", "in", "under", "beyond", "through", "without", "between", "beneath"]
    

    def generate_title(self):
        """
        Generate a random title for the content using predefined formats and word lists.
        
        """
        template = self.random_element(self.title_formats)

        title = template 
        if '{noun}' in title:
            title = title.replace('{noun}', self.random_element(self.nouns), 1)
            if '{noun}' in title:
                title = title.replace('{noun}', self.random_element(self.nouns), 1)
        
        if '{adjective}' in title:
            title = title.replace('{adjective}', self.random_element(self.adjectives), 1)

        if '{verb}' in title:
            title = title.replace('{verb}', self.random_element(self.verbs), 1)
        
        if '{proper_noun}' in title:
            title = title.replace('{proper_noun}', self.random_element(self.proper_nouns), 1)

        if '{preposition}' in title:
            title = title.replace('{preposition}', self.random_element(self.prepositions), 1)
                     
        return title
    
    def generate_media_type(self):
        """
        Generate a random media type from the predefined list.
        
        """
        return self.random_element(self.content_types) 
    
    def generate_season_episode(self, content_type):
        """
        Generate a random season and episode number based on the content type.
        
        Args:
            content_type (str): The type of content (e.g., Movie, TV Show).
        
        Returns:
            tuple: A tuple containing the season and episode number.
        """
        if content_type in  ['Movie', 'Documentary', 'Animation', 'Short Film']:
            return -1, -1
        else:
            seasons = self.random_int(*self.seasons[content_type])
            episodes = self.random_int(*self.seasons[content_type])
            return seasons, episodes
        
    def generate_duration(self, content_type):
        """
        Generate a random duration based on the content type.
        
        Args:
            content_type (str): The type of content (e.g., Movie, TV Show).
        
        Returns:
            int: The duration in minutes.
        """
        return self.random_int(*self.duration[content_type])
    
    def generate_language(self):
        """
        Generate a random language from the predefined list.
        
        """
        return self.random_element(self.language)
    
    def generate_content_provider(self):
        """
        Generate a random content provider from the predefined list.
        
        """
        return self.random_element(self.content_providers)
    
    def generate_genre(self):
        """
        Generate a random genre from the predefined list.
        
        """
        return self.random_element(self.genres)
    
    def generate_release_year(self):
        """
        Generate a random release year from the predefined range.
        
        """
        return self.random_element(range(2000, 2025))
    
    def content(self):
        """
        Generate a dictionary containing random media content data.
        
        Returns:
            dict: A dictionary with media content data.
        """
        content_type = self.generate_media_type()
        seasons, episodes = self.generate_season_episode(content_type)
        duration = self.generate_duration(content_type)
        language = self.generate_language()
        content_provider = self.generate_content_provider()
        genre = self.generate_genre()
        release_year = self.generate_release_year()
        title = self.generate_title()

        return {
            'title': title,
            'type': content_type,
            'season': seasons,
            'episode': episodes,
            'duration': duration,
            'language': language,
            'provider': content_provider,
            'genre': genre,
            'release_year': release_year
        }
    

