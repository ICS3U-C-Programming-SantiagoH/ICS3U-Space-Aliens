#!/usr/bin/env python3
# Created by: Santiago Hewett
# Date: Dec. 19,2023
# This program is a "Space Alien" game on pybadge



import stage
import ugame
import random
import time
import supervisor
import constants


def menu_scene():
    # This function is the code to create the main game scene

    # Image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Add text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text1.move(30, 10)
    text1.text("Santi Studios")
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # Set the background to the 0 image from the image bank
    # The size will be (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Create the stage for the background to show frames at 60 fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers, so the item shows up in order
    game.layers = text + [background]

    # Render the sprites
    # Render the game scene once per scene
    game.render_block()

    # A forever loop
    while True:
        # Get the user input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START != 0:
            game_scene()

        # Redraw the sprites
        game.tick()

def splash_scene():
    # This function is the code to create the main game scene

    # Sound to play
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # Image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Set the background to the 0 image from the image bank
    # The size will be (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Used this program to split the image into tiles:
    # https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png

    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # Create the stage for the background to show frames at 60 fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers, so the item shows up in order
    game.layers = [background]

    # Render the sprites
    # Render the game scene once per scene
    game.render_block()

    # A forever loop
    while True:
        # Wait for 2 seconds to go to the menu
        time.sleep(2.0)
        menu_scene()

def game_scene():
    # This function is the code to create the main game scene

    # Set score and display
    score = 0
    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text(f"Score: {score}")

    def show_alien():
        # Take the aliens that are off screen and puts them back on
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(
                    random.randint(
                        0 + constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

    # Image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Buttons that keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Sound to play
    pew_sound = open("pew.wav", "rb")
    boom_sound = open("boom.wav", "rb")
    crash_sound = open("crash.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Set the background to the 0 image from image bank
    # The size will be (10x8 tiles of size 16x16)
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(3, 14)
            background.tile(x_location, y_location, tile_picked)

    # A sprite that will update every frame with the background
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # List of aliens to have more than 1
    aliens = []

    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(
            image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        aliens.append(a_single_alien)

    # 1 alien on the screen
    show_alien()

    # Create a list for the laser to shoot
    lasers = []

    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(
            image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        lasers.append(a_single_laser)

    # Create the stage for the background to show
    # Frames at 60 fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers, so the items show up in order
    game.layers = [score_text] + lasers + [ship] + aliens + [background]

    # Render the sprites
    # Render the game scene once per scene
    game.render_block()

    # A forever loop
    while True:
        # Get the user input
        keys = ugame.buttons.get_pressed()

        # A button to shoot
        if keys & ugame.K_O != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_released"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        # B button, Start button, Select button, and directional buttons logic

        if keys & ugame.K_O != 0:
            pass

        if keys & ugame.K_START != 0:
            pass

        if keys & ugame.K_SELECT != 0:
            pass

        if keys & ugame.K_RIGHT:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)
            else:
                ship.move(0, ship.y)

        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 1, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)

        if keys & ugame.K_UP:
            if ship.y >= 0:
                ship.move(ship.x, ship.y - 1)
            else:
                ship.move(ship.x, 0)

        if keys & ugame.K_DOWN:
            if ship.y <= 120:
                ship.move(ship.x, ship.y + 1)
            else:
                ship.move(ship.x, 120)

        # Update the logic of the game
        # Play pew sound when button pressed
        if a_button == constants.button_state["button_just_pressed"]:
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # Each frame move lasers that have shot
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x, lasers[laser_number].y - constants.LASER_SPEED)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Each frame move aliens that have shot
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x, aliens[alien_number].y + constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    score -= 1
                    if score < 0:
                        score = 0
                    score_text.clear()
                    score_text.cursor(0, 0)
                    score_text.move(1, 1)
                    score_text.text(f"Score: {score}")

        # Within the same function, in the collision detection block
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        if stage.collide(lasers[laser_number].x, lasers[laser_number].y,
                                         lasers[laser_number].x + 16, lasers[laser_number].y + 16,
                                         aliens[alien_number].x, aliens[alien_number].y,
                                         aliens[alien_number].x + 16, aliens[alien_number].y + 16):
                            # Alien was hit
                            aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            score += 1
                            score_text.clear()
                            score_text.cursor(0, 0)
                            score_text.move(1, 1)
                            score_text.text(f"Score: {score}")
                            show_alien()
                            show_alien()

        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                if stage.collide(aliens[alien_number].x + 1, aliens[alien_number].y,
                                 aliens[alien_number].x + 15, aliens[alien_number].y + 15,
                                 ship.x, ship.y,
                                 ship.x + 15, ship.y + 15):
                    # When alien hits ship
                    sound.stop()
                    sound.play(crash_sound)
                    time.sleep(3.0)  # Remove the extra comma
                    game_over_scene(score)

        # Only refresh the sprite
        game.render_sprites(lasers + [ship] + aliens)
        game.tick()

def game_over_scene(final_score):
    # The game over function

    # Image bank
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Image 0 is background
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Text for background
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text1.move(22, 20)
    text1.text("Final score: {:0>2d}".format(final_score))
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    text3 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text3.move(32, 110)
    text3.text("PRESS SELECT")
    text.append(text3)

    # Create the stage for the background to show
    # Frames at 60 fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers, so the items show up in order
    game.layers = text + [background]

    # Render the sprites and background
    game.render_block()

    # Forever loop
    while True:
        # User input
        keys = ugame.buttons.get_pressed()

        # Check if the SELECT button is pressed
        if keys & ugame.K_SELECT != 0:
            # Reload the program (restart the game)
            supervisor.reload()

        # Update logic of the game and wait for refresh
        game.tick()

if __name__ == "__main__":
    splash_scene()

