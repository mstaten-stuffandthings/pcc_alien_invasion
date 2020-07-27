import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


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

        # Create and instance of GameStats
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
        self._check_bullet_alien_collisions()
    

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove collided objects
        collisions = pygame.sprite.groupcollide(self.bullets
                                               ,self.aliens
                                               ,False
                                               ,True
                                               )
        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien to get dimensions and calculate the 
            # number of aliens in a row
            # the spacing between aliens is width of an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width * 2)
        alien_count_x = available_space_x // (alien_width * 2)
        # Determine number of alien rows for the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height
                             - alien_height * 3
                             - ship_height)
        row_count_y = available_space_y // (alien_height * 2)
        
        # Create fleet of aliens
        for row_number in range(row_count_y):
            for alien_number in range(alien_count_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
            """Create an alien and add it to the row."""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + (alien_width * 2 * alien_number)
            alien.rect.x = alien.x
            alien.rect.y = alien_height + (alien_height * 2 * row_number)
            self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        """
        Check to see if fleet is at the edge, 
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens reaching the bottom of the screen
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            # Clear screen
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(1.0)
        else:
            self.stats.game_active = False
    

    def _check_aliens_bottom(self):
        """Check if an alien hsa reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as a ship collision
                self._ship_hit()
                break


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""    
        # Draw the screen
        self.screen.fill(self.settings.screen_background_color)
        # Put ship on top of the screen
        self.ship.blitme()
        # Draw each bullet in group using sprites method to the screen
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        # Draw alien to screen
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make and run a game instance
    ai = AlienInvasion()
    ai.run_game()

