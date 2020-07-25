class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize game settings."""
        # Screen settings
        self.caption = "Alien Invasion"
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_background_color = (230, 230, 230)
        
        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

