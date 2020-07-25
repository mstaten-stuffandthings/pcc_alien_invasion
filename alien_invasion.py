import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width
            ,self.settings.screen_height)
            #,pygame.FULLSCREEN
            )
        pygame.display.set_caption(self.settings.caption)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()


    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Resond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to bullet sprite."""
        if (len(self.bullets)) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        # Get rid of bullets that have disappeared.
            # Python expects a list length used in a for loop 
            # to have a constant size so we need a copy of the list
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) 
            # terminal shows number of bullets on screen
            # decrements as they exit the top        


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""    
        # Draw the screen
        self.screen.fill(self.settings.screen_background_color)
        # Put ship on top of the screen
        self.ship.blitme()
        # Draw each bullet in group using sprites method to the screen
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make and run a game instance
    ai = AlienInvasion()
    ai.run_game()

