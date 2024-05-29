# Libraries to import
import pygame  # The Pygame library, used for game development
import sys  # Contains systems functions
import os  # Operating system interaction
import random  # Library with random number generation
import time  # Time functions

# Start Pygame & Mixer
pygame.init()
pygame.mixer.init()

# Window Settings
pygame.display.set_caption('Higher or Lower')
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)
screen_width = 1280
screen_height = 720
display_screen = pygame.display.set_mode((screen_width, screen_height))
splash_start_time = 0
splash_end_time = 2

# Sound Files
sound_files = {
    'main': (os.path.join("sounds", "Main.wav")),  # Change to Main2.wav for alternate music
    'menu': (os.path.join("sounds", "Rule.wav")),
    'game': (os.path.join("sounds", "Game.wav")),  # Change to Game2.wav for alternate music
    'card': (os.path.join("sounds", "Card.wav")),
}
sounds = {name: pygame.mixer.Sound(path) for name, path in sound_files.items()}
sounds['main'].set_volume(0.1)
sounds['menu'].set_volume(0.2)
sounds['game'].set_volume(0.2)
sounds['card'].set_volume(0.1)


# Stop Sound
def stop_all_sounds():
    for sound in sounds.values():
        sound.stop()


# Image Loading
def load_image(image_path):
    return pygame.image.load(image_path).convert_alpha()  # Load and convert to include per-pixel alpha values


# Background Images
backgrounds = {
    'launch': load_image('backgrounds/Launch.png'),
    'menu': load_image('backgrounds/Menu.png'),
    'game': load_image('backgrounds/Game.png'),
    'rules': load_image('backgrounds/Rules.png'),
    'cards': load_image('backgrounds/Cards.png')
}


# Button Images
buttons = {
    'start': load_image('button/Start.png'),
    'start_hover': load_image('button/Start_Hover.png'),
    'menu': load_image('button/Menu.png'),
    'menu_hover': load_image('button/Menu_Hover.png'),
    'exit': load_image('button/Exit.png'),
    'exit_hover': load_image('button/Exit_Hover.png'),
    'exit_menu': load_image('button/Exit_2.png'),
    'exit_menu_hover': load_image('button/Exit_Hover_2.png'),
    'rules': load_image('button/Rules.png'),
    'rules_hover': load_image('button/Rules_Hover.png'),
    'rules_menu': load_image('button/Menu_2.png'),
    'rules_menu_hover': load_image('button/Menu_2_Hover.png'),
    'higher': load_image('button/Higher.png'),
    'higher_hover': load_image('button/Higher_Hover.png'),
    'lower': load_image('button/Lower.png'),
    'lower_hover': load_image('button/Lower_Hover.png'),
    'card': load_image('button/Cards.png'),
    'card_hover': load_image('button/Cards_Hover.png'),
    'card_rules': load_image('button/Rules_2.png'),
    'cards_rules_hover': load_image('button/Rules_Hover_2.png')
}

# Player Score Labels
p1_score_label = load_image('P1 Points label.png')
p1_score_label_rect = p1_score_label.get_rect(center=(180, 340))  # Retrieves rectangular area with centre coordinates
p2_score_label = load_image('P2 Points label.png')
p2_score_label_rect = p2_score_label.get_rect(center=(180, 100))
P1_final_label = load_image('P1 FinalPoints label.png')
P1_final_label_rect = P1_final_label.get_rect(center=(1210, 475))
P2_final_label = load_image('P2 FinalPoints label.png')
P2_final_label_rect = P2_final_label.get_rect(center=(1200, 555))

# Player Indicators
font = pygame.font.Font(None, 36)  # Choose font and size
player_indicator = font.render("Player 1", True, (255, 255, 255))
player_indicator_rect = player_indicator.get_rect(midtop=(screen_width // 2.1, 547))

# Game Logic
current_state = 'Splash'  # Program will always begin with the splash screen
run_once = True  # Flag that sets the initial logic to only run once
current_player = 1  # The currently active player
p1_correct = 0  # The number of correct guesses by the player
p2_correct = 0
p1_drawn = 0  # The number of cards given to player
p2_drawn = 0
p1_x_offset = 0  # X offset for the drawing on screen of cards
p2_x_offset = 0
p1_last_card = 0  # Value of the previous card that guess is based on
p2_last_card = 0
p1_card_value = 0  # Value of the new card revealed after a guess
p2_card_value = 0
p1_wins = 0  # Number of rounds a player has won
p2_wins = 0

card_images = {}  # Dictionary for storing of card images
suits = ['c', 'd', 'h', 's']  # Card suits
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']  # Card ranks


# Button Interactivity
class Button:
    def __init__(self, x, y, image, highlight, unclick):
        self.image = image  # Give image to the Button
        self.rect = self.image.get_rect()  # Gets button rectangle area
        self.rect.center = (x, y)  # The positioning of the button centre
        self.click = False  # Will track the click of the button
        self.highlight = highlight  # The image when the button is highlighted
        self.unclick = unclick  # The default image of the button
        self.play_once = 0  # Button animation flag

    def draw(self):
        pos = pygame.mouse.get_pos()  # Returns mouse position
        action = False  # Set to false for tracking button click

        match self.rect.collidepoint(pos):  # Checks position of mouse cursor is in button's area
            case True:  # Mouse over button
                self.image = self.highlight  # Sets the button image to highlight
                if self.play_once == 0:  # Looks to see if animation has not been played
                    self.play_once = 1   # Indicates animation has been played
                if pygame.mouse.get_pressed()[0] == 1 and not self.click:  # Looks for left mouse button click
                    action = True  # Register the button as being pressed
                    self.click = True  # Click flag is true
                elif pygame.mouse.get_pressed()[0] == 0:  # Checks if left mouse button has not been pressed
                    self.click = False  # Reset button click flag

            case False:
                self.image = self.unclick  # Sets button image to default
                self.play_once = 0  # Resets highlight animation flag

        display_screen.blit(self.image, (self.rect.x, self.rect.y))  # Draw the button in specified position

        return action


# Button Positioning
button_draw = {
    'higher': Button(520, 660, buttons['higher'], buttons['higher_hover'], buttons['higher']),
    'lower': Button(730, 660, buttons['lower'], buttons['lower_hover'], buttons['lower']),
    'start_menu': Button(995, 660, buttons['menu'], buttons['menu_hover'], buttons['menu']),
    'exit': Button(1185, 660, buttons['exit'], buttons['exit_hover'], buttons['exit']),
    'start': Button(630, 210, buttons['start'], buttons['start_hover'], buttons['start']),
    'rules': Button(630, 410, buttons['rules'], buttons['rules_hover'], buttons['rules']),
    'rules_menu': Button(995, 660, buttons['rules_menu'], buttons['rules_menu_hover'], buttons['rules_menu']),
    'exit_menu': Button(630, 610, buttons['exit_menu'], buttons['exit_menu_hover'], buttons['exit_menu']),
    'card_rules': Button(180, 660, buttons['card_rules'], buttons['cards_rules_hover'], buttons['card_rules']),
    'card_value': Button(330, 660, buttons['card'], buttons['card_hover'], buttons['card'])
}


# New Game - First time game is launched
def new_game():
    global p1_drawn
    global p2_drawn
    global current_player
    global p1_correct
    global p2_correct
    global p1_x_offset
    global p2_x_offset
    global p1_last_card
    global p2_last_card
    global p1_card_value
    global p2_card_value
    global run_once

    # Resets the game variables
    p1_drawn = 0
    p2_drawn = 0
    current_player = 1
    p1_correct = 0
    p2_correct = 0
    p1_x_offset = 0
    p2_x_offset = 0
    p1_last_card = 0
    p2_last_card = 0
    p1_card_value = 0
    p2_card_value = 0
    display_screen.blit(backgrounds['game'], (0, 0))
    run_once = False


# Reset Game - If the game is exited to menu then returned to
def reset_game_state():
    global p1_drawn, p2_drawn, current_player, p1_correct
    global p2_correct, p1_x_offset, p2_x_offset, p1_last_card, p2_last_card
    global p1_card_value, p2_card_value, p1_wins, p2_wins, run_once

    # Reset all game variables
    p1_drawn = 0
    p2_drawn = 0
    current_player = 1
    p1_correct = 0
    p2_correct = 0
    p1_x_offset = 0
    p2_x_offset = 0
    p1_last_card = 0
    p2_last_card = 0
    p1_card_value = 0
    p2_card_value = 0
    p1_wins = 0
    p2_wins = 0
    run_once = True


# Round End
def round_end_():
    global current_player
    global p1_correct
    global p2_correct
    global p1_x_offset
    global p2_x_offset
    global p1_last_card
    global p2_last_card
    global p1_card_value
    global p2_card_value
    global run_once

    current_player = 1
    p1_correct = 0
    p2_correct = 0
    p1_x_offset = 0
    p2_x_offset = 0
    p1_last_card = 0
    p2_last_card = 0
    p1_card_value = 0
    p2_card_value = 0
    run_once = True


# Win Condition
def win_condition(p1_correct, p2_correct):
    global p1_wins
    global p2_wins

    match p1_correct > p2_correct:  # Player 1 had more correct guesses
        case True:
            p1_wins += 1  # Add 1 to Player 1 total
            new_game()
        case False:
            match p1_correct < p2_correct:  # Player 2 had more correct guesses
                case True:
                    p2_wins += 1  # Add 1 to Player 2 total
                    new_game()
                case False:  # If the guesses were equal
                    new_game()


# Higher Guesses
def check_high(last_card, card_value):
    global current_player
    global p1_correct
    global p2_correct
    global p1_drawn
    global p2_drawn

    # Updates scores dependant on the guess
    new_score = card_value
    old_score = last_card

    match current_player:
        case 1:
            if new_score > old_score:
                p1_correct += 1
                p1_drawn += 1
                return new_score
            elif new_score == old_score:
                p1_drawn += 1
                return new_score
            else:
                p1_drawn += 1
                return new_score

        case 2:
            if new_score > old_score:
                p2_correct += 1
                p2_drawn += 1
                return new_score
            elif new_score == old_score:
                p2_drawn += 1
                return new_score
            else:
                p2_drawn += 1
                return new_score


# Lower Guesses
def check_low(last_card, card_value):
    global current_player
    global p1_correct
    global p2_correct
    global p1_drawn
    global p2_drawn

    # Updates scores dependant on the guess
    new_score = card_value
    old_score = last_card

    match current_player:
        case 1:
            if new_score < old_score:
                p1_correct += 1
                p1_drawn += 1
                return new_score
            elif new_score == old_score:
                p1_drawn += 1
                return new_score
            else:
                p1_drawn += 1
                return new_score

        case 2:
            if new_score < old_score:
                p2_correct += 1
                p2_drawn += 1
                return new_score
            elif new_score == old_score:
                p2_drawn += 1
                return new_score
            else:
                p2_drawn += 1
                return new_score


# Card Values
def card_score(card_value):
    global p1_card_value
    global p2_card_value

    # Retrieves rank and suit from the card key
    rank, suit = card_value

    if current_player == 1:
        p1_card_value = int(rank)
    else:
        p2_card_value = int(rank)


# Card Behaviour
def draw_card(x_offset):
    global current_player
    global p1_card_value
    global p2_card_value

    # Chooses a random card key
    card_key = random.choice(list(card_images.keys()))

    # Sets space between each card
    space_between_cards = 40

    # Sets the positions for both players
    p1_initial_x = 235
    p1_initial_y = 372
    p2_initial_x = 235
    p2_initial_y = 144

    # Draws a card for the player
    if current_player == 1:
        display_screen.blit(card_images[card_key], (p1_initial_x + x_offset, p1_initial_y))
        x_offset = space_between_cards
        card_score(card_key)  # Determines what the card score is
        card_images.pop(card_key)  # Will remove this card from the deck now it is drawn
        p1_card_value = int(card_key[0])  # Update current card value

    elif current_player == 2:
        display_screen.blit(card_images[card_key], (p2_initial_x + x_offset, p2_initial_y))
        x_offset = space_between_cards
        pygame.display.update()
        card_score(card_key)
        card_images.pop(card_key)
        p2_card_value = int(card_key[0])

    return x_offset


# Main Program
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Define the splash state
    if current_state == 'Splash':
        if splash_start_time == 0:
            splash_start_time = time.time()

        # Display the background image
        display_screen.blit(backgrounds['launch'], (0, 0))

        # Checks the elapsed time
        if time.time() - splash_start_time >= splash_end_time:
            current_state = 'Menu'  # Transition to the menu state

    # Define the menu state
    if current_state == 'Menu':
        display_screen.blit(backgrounds['menu'], (0, 0))
        if not pygame.mixer.music.get_busy():
            sounds['main'].play(loops=-1)

        if button_draw['rules'].draw():
            current_state = 'Rules'
            stop_all_sounds()
            sounds['menu'].play(loops=-1)

        if button_draw['exit_menu'].draw():
            sys.exit()

        if button_draw['start'].draw():
            current_state = 'Game'
            stop_all_sounds()

    if current_state == 'Rules':
        display_screen.blit(backgrounds['rules'], (0, 0))
        if not pygame.mixer.music.get_busy():
            sounds['menu'].play(loops=-1)

        if button_draw['card_value'].draw():
            current_state = 'CardValue'
            stop_all_sounds()
            sounds['card'].play(loops=-1)

        if button_draw['rules_menu'].draw():
            current_state = 'Menu'
            stop_all_sounds()

    if current_state == 'CardValue':
        display_screen.blit(backgrounds['cards'], (0, 0))
        if not pygame.mixer.music.get_busy():
            sounds['card'].play(loops=-1)

        if button_draw['rules_menu'].draw():
            current_state = 'Menu'
            stop_all_sounds()
            sounds['main'].play(loops=-1)

        if button_draw['card_rules'].draw():
            current_state = 'Rules'
            stop_all_sounds()
            sounds['menu'].play(loops=-1)

    if current_state == 'Game':
        if not pygame.mixer.music.get_busy():
            sounds['game'].play(loops=-1)

        # If the deck is empty it will load card images
        if len(card_images) == 0:
            for suit in suits:
                for rank in ranks:
                    image_path = os.path.join("cards", f"{suit}{rank}.png")
                    original_image = pygame.image.load(image_path)
                    scaled_image = pygame.transform.scale(original_image, (110, 135))
                    card_images[(rank, suit)] = scaled_image

        card_key, card_value = random.choice(list(card_images.items()))

        # Shows the score and final score text on the screen
        score = pygame.font.Font('scribble.ttf', 50)
        final_score = pygame.font.Font('scribble.ttf', 35)
        p1_scoreText = score.render(str(p1_correct), True, 'Black')
        p1_ScoreRect = p1_scoreText.get_rect(center=(185, 360))
        p2_scoreText = score.render(str(p2_correct), True, 'Black')
        p2_ScoreRect = p2_scoreText.get_rect(center=(185, 120))
        p1_finalText = final_score.render(str(p1_wins), True, 'Black')
        p1_finalRect = p1_finalText.get_rect(center=(1210, 478))
        p2_finalText = final_score.render(str(p2_wins), True, 'Black')
        p2_finalRect = p2_finalText.get_rect(center=(1200, 558))

        # Display options for the player indicators
        if current_player == 1:
            player_indicator = font.render("Currently Active: Player 1", True, (243, 200, 117, 255))
        else:
            player_indicator = font.render("Currently Active: Player 2", True, (159, 227, 185, 255))

        # Display the new player indicator
        display_screen.blit(player_indicator, player_indicator_rect)

        # On first run the game is initialized
        if run_once:
            display_screen.blit(backgrounds['game'], (0, 0))
            p1_x_offset += draw_card(p1_x_offset)
            p1_last_card = p1_card_value
            current_player = 2
            p2_x_offset += draw_card(p2_x_offset)
            p2_last_card = p2_card_value
            current_player = 1
            run_once = False

        # Button interaction on click
        if button_draw['start_menu'].draw():
            current_state = 'Menu'  # Change game state to Menu
            stop_all_sounds()
            reset_game_state()

        # Exit game on click
        if button_draw['exit'].draw():
            sys.exit()

        # When player two receives twelve cards, check the win condition
        if p2_drawn == 12:
            time.sleep(2)  # Pause for 2 seconds
            win_condition(p1_correct, p2_correct)
            round_end_()  # End of the round, reset everything except win totals

        # When higher button is selected
        if button_draw['higher'].draw():
            if current_player == 1:
                p1_x_offset += draw_card(p1_x_offset)
                p1_last_card = check_high(p1_last_card, p1_card_value)
            elif current_player == 2:
                p2_x_offset += draw_card(p2_x_offset)
                p2_last_card = check_high(p2_last_card, p2_card_value)

            if p1_drawn == 12:
                current_player = 2

        # When lower button is selected
        if button_draw['lower'].draw():
            if current_player == 1:
                p1_x_offset += draw_card(p1_x_offset)
                p1_last_card = check_low(p1_last_card, p1_card_value)
            elif current_player == 2:
                p2_x_offset += draw_card(p2_x_offset)
                p2_last_card = check_low(p2_last_card, p2_card_value)

            if p1_drawn == 12:
                current_player = 2

        # Displays the score labels and final scores
        display_screen.blit(p1_score_label, p1_score_label_rect)
        display_screen.blit(p1_scoreText, p1_ScoreRect)
        display_screen.blit(p2_score_label, p2_score_label_rect)
        display_screen.blit(p2_scoreText, p2_ScoreRect)
        display_screen.blit(P1_final_label, P1_final_label_rect)
        display_screen.blit(p1_finalText, p1_finalRect)
        display_screen.blit(P2_final_label, P2_final_label_rect)
        display_screen.blit(p2_finalText, p2_finalRect)

    pygame.display.update()
